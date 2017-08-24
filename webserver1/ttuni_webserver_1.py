#!/usr/bin/env python
import socket

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 4444

response_body = "Hello TTUni"
response = """HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {0}

{1}""".format(len(response_body), response_body)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((WEB_SERVER_HOST, WEB_SERVER_PORT))
s.listen(5)

print "server is listenning on {0}:{1}".format(WEB_SERVER_HOST, WEB_SERVER_PORT)

while True:
    # accept connection
    client, address = s.accept()
    print "reiceived connection from {0}".format(address)

    # get http request
    request = client.recv(1024)
    print(request.decode("utf-8"))

    # send http response to client
    client.send(response.encode())

    # close connection
    client.close()
