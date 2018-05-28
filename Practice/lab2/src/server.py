import http.server
import socketserver
import socket
import sys
import glob
import os
import base64
import time
from pathlib import Path
from generated.protobuf.auth_data_pb2 import (
    AuthenticationRequest, AuthenticationRespose,
    UserData, AuthenticationState
)

root = os.getcwd()
ips_directory_path = "{root}/res/ips".format(root=root)
users_directory_path = "{root}/res/users".format(root=root)


def now():
    return int(time.time())


class AuthTCPServer(socketserver.TCPServer, socketserver.ThreadingMixIn):

    def verify_request(self, request, client_address):
        """Blocking banned users by ip address
        """
        print("Verification")
        user_ip_path = Path("{ip_path}/{ip_address}.data"
                            .format(ip_path=ips_directory_path,
                                    ip_address=client_address[0]))
        if not user_ip_path.exists():
            return True
        user_ip_file = ''
        try:
            user_ip_file = user_ip_path.open('rb')
            user_ip_data = user_ip_file.read()
            user_ip_file.close()
            authentication_state = AuthenticationState()
            authentication_state.ParseFromString(user_ip_data)
            if authentication_state.ban_expires < now():
                authentication_state.is_banned = False
                user_ip_file = user_ip_path.open('wb')
                user_ip_file.write(authentication_state.SerializeToString())
                user_ip_file.close()
            else:
                sys.stderr.write("BLOCKED: %s'\n" % (client_address[0]))
                return False
        except Exception as e:
            sys.stderr.write("VERIFICATION ERROR: %s - -  %s\n" %
                             (client_address[0],
                              "Error: %r" % e))
            return False
        finally:
            if user_ip_file:
                user_ip_file.close()
        return True


class AuthRequestHandler(socketserver.StreamRequestHandler):

    auth_timeout = 300
    ban_timeout = 300

    def handle(self):
        self.close_connection = 1
        self.handle_authorization()
        while not self.close_connection:
            self.handle_message()

        self.log_message("Connection closed")

    def handle_authorization(self):
        try:
            raw_request = self.rfile.read()
            auth_request = AuthenticationRequest()
            auth_request.ParseFromString(raw_request)
            self.log_message("Start authenticate user: %s",
                             auth_request.username)
            self.authenticate_user(auth_request)
        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return

    def handle_message(self):
        try:
            raw_request = self.rfile.read()
            self.log_message("Get %s", raw_request)
            self.close_connection = 1
        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return

    def log_error(self, format, *args):
        sys.stderr.write("ERROR: %s - -  %s\n" %
                         (self.client_address[0],
                          format % args))

    def log_message(self, format, *args):
        sys.stderr.write("INFO: %s - -  %s\n" %
                         (self.client_address[0],
                          format % args))

    def authenticate_user(self, auth_request):
        user_file = ''
        try:
            user_data_path = Path("{users_path}/{username}.data".format(
                users_path=users_directory_path,
                username=auth_request.username
            ))
            if not user_data_path.exists():
                self.log_error("No such user: {username}".format(
                    username=auth_request.username
                ))
                self.close_connection = 1
                return
            user_file = user_data_path.open(mode='rb')
            user_data = UserData()
            user_data.ParseFromString(user_file.read())
            user_file.close()
            user_file = user_data_path.open(mode='wb')
            if user_data.password == auth_request.password:
                user_data.auth_expires = now() + self.auth_timeout
                user_data.tries = 3
                user_file.write(user_data.SerializeToString())
                user_file.close()
                self.close_connection = 0
                self.log_message("Success authorization")
                return
            else:
                if user_data.tries <= 1:
                    user_data.tries = 3
                    user_file.write(user_data.SerializeToString())
                    user_file.close()
                    self.log_error("Unsuccessful authorization. User banned")
                    self.ban_user(auth_request)
                else:
                    user_data.tries -= 1
                    user_file.write(user_data.SerializeToString())
                    user_file.close()
                    self.log_error("Unsuccessful authorization. {tries} tries remain".format(
                        tries=user_data.tries
                    ))

        except Exception as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
        finally:
            if user_file:
                user_file.close()

    def ban_user(self, auth_request):
        authentication_state = AuthenticationState()
        authentication_state.is_banned = True
        authentication_state.ban_expires = now() + self.ban_timeout
        user_ip_file = ''
        try:
            user_ip_file = open("{ip_path}/{ip_address}.data"
                                .format(ip_path=ips_directory_path,
                                        ip_address=self.client_address[0]), 'wb')
            user_ip_file.write(authentication_state.SerializeToString())
        except Exception as e:
            self.log_error("Ban error %r", e)
        finally:
            if user_ip_file:
                user_ip_file.close()


PORT = 8000
httpd = AuthTCPServer(("", PORT), AuthRequestHandler)

print("serving at port: {port}".format(port=PORT))
httpd.serve_forever()
