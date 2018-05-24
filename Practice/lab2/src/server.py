import http.server
import socketserver
import socket
import sys
import glob
import os
import base64
from pathlib import Path
from generated.protobuf.auth_data_pb2 import AuthenticationRequest, AuthenticationRespose, UserData


class AuthTCPServer(socketserver.TCPServer):

    def verify_request(self, request, client_address):
        """Blocking banned users by ip address
        """
        return True


class AuthRequestHandler(socketserver.StreamRequestHandler):
    root = os.getcwd()
    ips_directory_path = "{root}/res/ips".format(root=root)
    users_directory_path = "{root}/res/users".format(root=root)

    def handle(self):
        self.close_connection = 1
        self.handle_authorization()
        while not self.close_connection:
            self.handle_authorization()

    def handle_authorization(self):
        try:
            raw_request = self.rfile.read()
            auth_request = AuthenticationRequest()
            auth_request.ParseFromString(raw_request)
            self.log_message("Start authenticate user: %s",
                             auth_request.username
                             )
            user_data_path = Path("{users_path}/{username}.data".format(
                users_path=self.users_directory_path,
                username=auth_request.username
            ))
            if not user_data_path.exists():
                self.log_error("No such user: {username}".format(
                    username=auth_request.username
                ))
                self.close_connection = 1
                return
            file = user_data_path.open(mode='rb')
            user_data = UserData()
            user_data.ParseFromString(file.read())
            if user_data.password == auth_request.password:
                self.log_message("Success authorization")
            else:
                self.log_error("Unsuccessful authorization")
        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return
        finally:
            if file:
                file.close()

    def log_error(self, format, *args):
        sys.stderr.write("ERROR: %s - -  %s\n" %
                         (self.client_address[0],
                          format % args))

    def log_message(self, format, *args):
        sys.stderr.write("INFO: %s - -  %s\n" %
                         (self.client_address[0],
                          format % args))


PORT = 8000
httpd = AuthTCPServer(("", PORT), AuthRequestHandler)

print("serving at port: {port}".format(port=PORT))
httpd.serve_forever()
