import sys
import os
import base64
from pathlib import Path
from generated.protobuf.auth_data_pb2 import UserData


username = input("Username: ")
password = input("Password: ")
encoded_password = base64.b64encode(password.encode())
user_file_path = Path("{root}/res/users/{username}.data".format(
    root=os.getcwd(),
    username=username
))
if user_file_path.exists():
    print("User already exists")
    exit(1)
user_data = UserData()
user_data.password = encoded_password
file = user_file_path.open(mode='wb')
file.write(user_data.SerializeToString())
file.close()
