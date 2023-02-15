
import sys
import socket
from threading import Thread

## 16進ダンプの実装
# ローカルとリモートのバケットを16進数とテキストでダンプしたものを表示する
def hexdump(src, length=16):
	result = []
	
	for i in range(0, len(src), length):
		s = src[i:i+length]
		hexa = ' '.join(['{:02X}'.format(x) for x in s])
		text = ''.join([chr(x) if x >= 32 and x < 127 else '.' for x in s])
		result.append('{:04X}   {}{}    {}'.format(i, hexa, ((length-len(s))*3)*' ', text))
	for s in result:
		print(s)

## データ受信処理の実装
# ローカルとリモートのsocketオブジェクトからデータの受信を処理し,そのbytesオブジェクトを返り値とする
def received_from(connection):
	buffer = b''
	connection.settimeout(2)

	try:
		recv_len = 1
		while recv_len:
			data = connection.recv(4096)
			buffer += data
			recv_len = len(data)
			if recv_len < 4096:
				break
	except:
		pass

	return buffer

## パケットの改ざん、改変の処理
# 必要に応じて以下に特定のパケットが来たら改ざんする処理を実装(現状なし)
def request_handler(buffer, peerName):
	# newbuffer = "{\"ip\":\""+peerName[0]+"\",\"port\":\""+str(peerName[1])+"\"}"
	# return buffer+newbuffer.encode()
	return buffer
 
def response_handler(buffer):
	return buffer

## プロキシハンドラーの実装
# プロキシサーバのメイン処理を行う関数
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
	remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remote_socket.connect((remote_host, remote_port))
	# print(client_socket, remote_host, remote_port, receive_first)
	# print(client_socket.getpeername()[0])


	if receive_first:
		remote_buffer = received_from(remote_socket)
		hexdump(remote_buffer)

		remote_buffer = response_handler(remote_buffer)

		if len(remote_buffer):
			print('[<==] Sending {} bytes to localhost.'.format(len(remote_buffer)))
			client_socket.send(remote_buffer)

	while True:
		local_buffer = received_from(client_socket)
		if len(local_buffer):
			print('[==>] Received {} bytes from localhost.'.format(len(local_buffer)))
			hexdump(local_buffer)
 
			local_buffer = request_handler(local_buffer, client_socket.getpeername())
			print(local_buffer)

			# client_socket.send(local_buffer)
 
			remote_socket.send(local_buffer)
			print('[==>] Sent to remote.')

		remote_buffer = received_from(remote_socket)

		if len(remote_buffer):
			print('[<==] Received {} bytes from remote.'.format(len(remote_buffer)))
			# hexdump(remote_buffer)
 
			remote_buffer = response_handler(remote_buffer)
			client_socket.send(remote_buffer)
			# print(remote_buffer)
 
			print('[<==] Sent to localhost.')

## サーバ処理の実装
# ローカルクライアントからの接続を待ち受ける関数
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind((local_host, local_port))
	except:
		print('[!!] Failed to listen on {}:{}'.format(local_host, local_port))
		print('Check for other listening sockets or correct permissions.')
		sys.exit(0)

	print('[*] Listening on {}:{}'.format(local_host, local_port))
	server.listen(5)

	while True:
		client_socket, addr = server.accept()
		print('[==>] Received incoming connection from {}:{}'.format(addr[0], addr[1]))
		proxy_thread = Thread(target=proxy_handler,
						args=[client_socket,remote_host, remote_port, receive_first])

		proxy_thread.start()

## メイン関数の実装
# receive_firstは先にパケットを受信するかどうかのフラグ
# Trueの場合は，サーバー側(このプログラム側)が先にバケットを受信する
# FTPサーバなどでは、TCPの3 Way Handshakeでコネクションが確立された時、サーバ側から最初にバナー情報などのパケットを送信するため、その場合は"True"を指定する
# Falseの場合はクライアントが先にバケットを送信する
def main():
	local_host = ""	#どっちも同じにする
	local_port = 8081

	remote_host = ""
	remote_port = 8080

	receive_first = False

	server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
	main()