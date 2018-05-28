import socket
import sys
import base64
from generated.protobuf.auth_data_pb2 import AuthenticationRequest


print("Please authorize")
username = input("Username: ")
password = input("Password: ")
encoded_password = base64.b64encode(password.encode())

sock = socket.socket()
sock.connect(('localhost', 8000))
request = AuthenticationRequest()
request.username = username
request.password = encoded_password
sock.send(request.SerializeToString())
