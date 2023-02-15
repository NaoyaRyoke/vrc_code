import http.server as s
from http.server import HTTPServer, CGIHTTPRequestHandler
import json
import requests
import schedule
import time
import datetime
import pyautogui
from screeninfo import get_monitors
from threading import Thread

# python D:\NaoChin\VrC\server.py

# ポート番号
PORT = 8080

# IPアドレス
HOST = ""

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
		print(body_json)
		if body_json != r"{}":
			baseX = body["Point"]["minX"]
			baseY = body["Point"]["minY"]
			width = body["Point"]["maxX"]-baseX
			height = body["Point"]["maxY"]-baseY
			x = width/2+baseX
			y = height/2+baseY
			MM = MouseMotion(selectMoniter, vrkSize)
			MM.movePointer(x, y)



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

class MouseMotion():
	def __init__(self, moniterNumber, vrkSize):
		self.moniters = get_monitors()
		self.moniter = self.moniters[moniterNumber]
		self.vrkSize = vrkSize

	def movePointer(self, _x, _y):
		x, y = self.setPoint(_x, _y)
		pyautogui.moveTo(x, y, 1)
	
	def setPoint(self, centerX, centerY):
		x = centerX * (self.moniter.width/self.vrkSize[0])+self.moniter.x
		y = centerX * (self.moniter.height/self.vrkSize[1])+self.moniter.y
		return (int(x), int(y))
	
	
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

def debug():
	x = y = 100
	MM = MouseMotion()
	MM.movePointer(x, y)
	return

if __name__ == '__main__':
	server_main()
	# debug()
