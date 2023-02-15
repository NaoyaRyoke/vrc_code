#
# file        pymain.py
# brief       Object Detection Sample Application (Python Version)
# author      Panasonic
# date        2020-09-01
# version     1.0
# Copyright    (C) COPYRIGHT 2020 Panasonic Corporation
#

import adam
import numpy as np
import cv2
import threading
import shutil
from AppPrefs import AppPrefs
from Response import Response
from ObjectDetection import ObjectDetection
from FileControl import FileControl
from HttpIF import HttpIF
from ConstDefine import ConstDefine




#################################
#		グローバル変数定義		#
#################################

image_callback_counter = 0		#画像取得コールバックカウンタ
loop = None				#イベントループオブジェクト

#############################
#		メソッド定義		#
#############################

#
# @brief	imageCallBack function
#  			画像取得コールバック関数
# @param img		[in] memoryview	画像データ
# @param clipInfo	[in] tuple		imgが切り出された座標（x:int,y:int,width:int,height:int）
# @param dateTime	[in] dateTime	画像データが取得された日時
#
def image_callback(img, clipInfo, dateTime):

	global image_callback_counter
	print ( ("===== image callback:%05d " % image_callback_counter) + dateTime.strftime("%F %T.%f") + " =====")

	# bytes型からndarray型へ変換(画像のフォーマットに)
	buf = np.frombuffer(img, dtype=np.uint8).reshape((clipInfo[3],clipInfo[2], 3))

	# 画像を保存
	filenameTmp = ConstDefine.IMAGE_FILE_PATH + "_"
	cv2.imwrite(filenameTmp, buf)
	shutil.move(filenameTmp, ConstDefine.IMAGE_FILE_PATH)

	#オブジェクト検出実行
	object_detection.detect_object(buf)

	#カウントアップ
	image_callback_counter += 1



#
# @brief	stopCallBack function
#  			アプリ停止コールバック関数
#
def stop_callback():
	global loop

	#ワーカースレッド停止
	httpif.set_exit_flag(True)

	print("===== stop callback =====")

	# adamEventloopオブジェクトを終了
	loop.exit()



#
# @brief	httpCallBack function
#  			HTTPコールバック関数
# @param reqType [in] 	int					リクエストタイプ
# @param reqData [in] 	bytes				リクエストデータ
# @return  				Tuplee(str, bytes)	ヘッダ情報, ボディ情報
#
def http_callback(reqType, reqData):

	# レスポンスオブジェクト
	resp = Response()
	if reqType == 0 :
		if reqData.decode() == "":
			# HTML形式でレスポンスを返す
			return resp.create_response_format(ConstDefine.HTML_FILE_PATH)
		else:
			#指定ファイル名へのパスを作成
			response_file_path = adam.AppDataDirPath + "/" + reqData.decode()
			#JavaScript形式でレスポンスを返す
			return resp.create_response_format(response_file_path)

	# 画像を重ね合わせ表示する場合
	elif reqType == 1 :
		return resp.create_response_format(ConstDefine.IMAGE_FILE_PATH)

	elif reqType == 5000 :
		# JSON形式でレスポンスを返す
		return resp.create_response_format(ConstDefine.JSON_FILE_PATH)

	else :
		# エラーレスポンスを返す
		return resp.response_error()







#
# @brief	startProcessing function
#  			プロセス開始関数
#
def start_processing():
	global loop

	#画像領域
	x = 0
	y = 0
	w = ConstDefine.RESO_LIST[appprefs.m_resolution][0]
	h = ConstDefine.RESO_LIST[appprefs.m_resolution][1]
	print("x=%d, y=%d, w=%d, h=%d, resolution=%d, frameRate_framenum=%d, frameRate_unittime=%d" % (x,y,w,h,appprefs.m_resolution,appprefs.m_framerate_framenum, appprefs.m_framerate_unittime))

	#adam.adamEventloopオブジェクト生成
	loop = adam.adamEventloop()

	#画像取得のイベントレシーバ生成
	imageReceiver = adam.createImageReceiver(image_callback, ConstDefine.RESO_LIST[appprefs.m_resolution], (x,y,w,h), (appprefs.m_framerate_framenum, appprefs.m_framerate_unittime), format=adam.FORMAT_BGR1)

	#adamEventloopオブジェクトにimageReceiverを追加する
	loop.add(imageReceiver)

	#adamEventloopオブジェクトを開始する
	loop.dispatch()

	#adamEventloopオブジェクトからimageReceiverを除く
	loop.remove(imageReceiver)

	del loop
	print("Finish: Process")


#
# @brief	main function
#  			メイン関数
#
if __name__ == '__main__':
	print("Start: Python thread")

	# アプリ初期環境設定
	#apppreftsを読み取るためのオブジェクト生成
	appprefs = AppPrefs()
	appprefs.load()

	#httpインターフェースオブジェクト
	httpif = HttpIF()

	#ワーカースレッド開始
	httpif.start()

	#オブジェクト検出クラスオブジェクト
	object_detection = ObjectDetection()

	#AdamAppに停止指示が来た時に呼び出すコールバックを指定する
	adam.setStopCallback(stop_callback)

	#AdamAppにHTTP通信が来た時に呼び出すコールバックを指定する
	adam.setHttpCallback(http_callback)

	#プロセス開始
	imageThread = threading.Thread(target=start_processing)
	imageThread.start()
	imageThread.join()

	print("Finish: Python thread")
