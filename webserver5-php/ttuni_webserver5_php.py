#!/usr/bin/env python
import socket
import os
import threading
import subprocess
import utils

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 5000
WEB_SERVER_ROOT_DIR = "c:\\TTUni\\htdocs"
PHP_DIR = "C:\\TTUni\\php"

def get_php_output(filepath):
    s = subprocess.Popen([os.path.join(PHP_DIR, "php.exe"), filepath], stdout=subprocess.PIPE)

    return s.stdout.read()

def generate_get_response(request_uri):
    if request_uri.endswith("/"): # access directory
        return utils.encode_http_response(404, {}, "Permission Denied")

    file_path = request_uri[1:] # remove / at the beginning
    full_file_path = os.path.join(WEB_SERVER_ROOT_DIR, file_path)

    if not os.path.exists(full_file_path):
        return utils.encode_http_response(404, {}, "File Not Found: {0}".format(full_file_path))

    if full_file_path.endswith(".php"):
        output = get_php_output(full_file_path)
        return utils.encode_http_response(200, {}, output)
    else:
        with open(full_file_path, "rb") as fp:
            content = fp.read()
            headers = { "Content-Type": "text/html;charset=utf-8" }
            return utils.encode_http_response(200, headers, content)

def client_handler(client_sock, address):
    print("received connection from {0}".format(address))

    # get http request
    raw_request = client_sock.recv(1024).decode("utf-8")

    if raw_request:
        print(raw_request)

        request_method, request_uri, request_body, _ = utils.parse_http_request(raw_request)

        if request_method.upper() == "GET":
            response = generate_get_response(request_uri)
        else:
            response = utils.encode_http_response(404, {}, "Invalid HTTP Method {0}".format(request_method))

        # send http response to client
        client_sock.send(response)

    # close connection
    client_sock.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((WEB_SERVER_HOST, WEB_SERVER_PORT))
s.listen(10)

print "server is listenning on {0}:{1}".format(WEB_SERVER_HOST, WEB_SERVER_PORT)

while True:
    # accept connection
    client, address = s.accept()

    worker_thread = threading.Thread(name="client worker {0}".format(address), target=client_handler, args=(client, address, ))
    worker_thread.start()
