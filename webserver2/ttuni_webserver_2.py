#!/usr/bin/env python
import socket
import os
import utils

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 5000
WEB_SERVER_ROOT_DIR = "c:\\ttuni\\htdocs"

def generate_get_response(request_uri):
    if request_uri.endswith("/"): # access directory
        return utils.encode_http_response(404, {}, "Permission Denied")

    file_path = request_uri[1:] # remove / at the beginning
    full_file_path = os.path.join(WEB_SERVER_ROOT_DIR, file_path)

    if not os.path.exists(full_file_path):
        return utils.encode_http_response(404, {}, "File Not Found: {0}".format(full_file_path))

    with open(full_file_path, "r") as fp:
        content = fp.read()
        return utils.encode_http_response(200, {}, content)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((WEB_SERVER_HOST, WEB_SERVER_PORT))
    s.listen(5)
    print "server is listenning on {0}:{1}".format(WEB_SERVER_HOST, WEB_SERVER_PORT)
    while True:
        # accept connection
        client_sock, address = s.accept()
        print "received connection from {0}".format(address)
        # get http request
        #TODO: for demo purpose, should improve it
        raw_request = client_sock.recv(1024).decode("utf-8")
        if raw_request:
            print(raw_request)
            request_method, request_uri, _, _ = utils.parse_http_request(raw_request)
            if request_method.upper() == "GET":
                response = generate_get_response(request_uri)
            else:
                response = utils.encode_http_response(404, {}, "Invalid HTTP Method {0}".format(request_method))
            # send http response to client
            client_sock.send(response)
        # close connection
        client_sock.close()

if __name__=="__main__":
    main()
