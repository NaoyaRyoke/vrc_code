import http.server as s
from http.server import HTTPServer, CGIHTTPRequestHandler
import json
import requests
import time
import datetime
from threading import Thread

# ポート番号
PORT = 8080

# IPアドレス
HOST = "10.13.15.2"

selectMoniter = 0
vrkSize = [640, 480]

# MM = MouseMotion()

# print(op.PersonParameter == {})
class Handler(CGIHTTPRequestHandler):
	# CGIを設置するディレクトリ
	cgi_directories = ["/cgi-bin"]

class ObjectDetectionHandler(s.BaseHTTPRequestHandler):
	def do_POST(self):

		# リクエスト取得
		# print(self.headers.get("HOST"))
		content_len  = int(self.headers.get("content-length"))
		# print(self.headers.values())
		# print(content_len)
		# print(requests.form.get("objectNum"))
		body = json.loads(self.rfile.read(content_len).decode('utf-8'))

		# レスポンス処理
		print(body)
		self.send_response(200)
		self.send_header('Content-type', 'application/json;charset=utf-8')
		self.end_headers()
		body_json = json.dumps(body, sort_keys=False, indent=4, ensure_ascii=True) 
		self.wfile.write(body_json.encode("utf-8"))

		# ここで受け取った値からの操作をしている
		# if body["class"] == 0:
		# 	for i in body["point"]:
		# 		self.MM.movePointer(i[0], i[1])
		# debug用はbaseX, 本番はminX

		#ここだけ変えたらいい
		print(body_json)
		if body_json != r"{}":
			SS = SendSignal()
			SS.device_control()
			time.sleep(3)



# class FunctionLP():
# 	def __init__(self):
# 		schedule.every(2).seconds.do(self.main)
# 		# schedule.every(2).minutes.do(self.main)
	
# 	def main(self):
# 		lp.main(op.PersonParameter)
	
# 	def loopJob(self):
# 		while True:
# 			schedule.run_pending()
# 			time.sleep(60)

	
class SendSignal():
    def __init__(self):
        # パラメーター（要書き換え）
        self.DEVICEID=""    #後で少し変える(どのデバイスを操作するか)
        self.ACCESS_TOKEN=""    #アクセストークン.ここは変えない
        self.API_BASE_URL=""  #ここも変えない
    
    # Send device control commandsコマンド（POST）
    def device_control(self):
        headers = {     #ここも基本変えない
            # ヘッダー
            'Content-Type': 'application/json; charset: utf8',
            'Authorization': self.ACCESS_TOKEN
        }
        url = self.API_BASE_URL + "/v1.0/devices/" + self.DEVICEID + "/commands"

        #操作内容(ここは要変更)
        body = {
        "command": "オフ",
        "parameter": "default",
        "commandType": "customize"
        }
        ddd = json.dumps(body)  #dict型をjsonに変換
        print(ddd) # 入力
        res = requests.post(url, data=ddd, headers=headers)
        print(res.text) # 結果

	
def server_main():
	# URLを表示
	# print("http://127.0.0.1:8080/")
	print("http://"+HOST+":"+str(PORT)+"/")

	# fl = FunctionLP()
	# flThread = Thread(target=fl.loopJob)
	# flThread.start()

	# サーバの起動
	httpd = HTTPServer((HOST, PORT), ObjectDetectionHandler)
	httpd.serve_forever()


if __name__ == '__main__':
	server_main()
	# debug()
