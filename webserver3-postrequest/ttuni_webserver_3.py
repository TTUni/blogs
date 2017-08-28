#!/usr/bin/env python
import socket
import os
import utils

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 5000

GET_RESPONSE = """<html>
<head>

</head>
<body>
<form method="post" action="/">
<div>
    <label>Username</label>
    <input name="username" />
</div>

<div>
    <label>Password</label>
    <input type="password" name="password" />
</div>

<div><input type="submit" value="Login" /></div>
</body>
</html>"""

POST_RESPONSE_SUCCESSFUL = """<html>
<header>

</header>
<body>
<div><a href="/">Login</a></div>
<div>Welcome {0}!</div>
</body>
</html>"""

POST_RESPONSE_FAILED = """<html>
<header>

</header>
<body>
<div>Invalid username/password, please <a href="/">login</a> again!</div>
</body>
</html>"""

def parse_params(rawparams):
    params = {}
    for param in rawparams.split("&"):
        name, value = param.split("=")
        params[name] = value
    return params

def generate_get_response(html_content):
    headers = { "Content-Type": "text/html;charset=utf-8" }
    return utils.encode_http_response(200, headers, html_content.encode("utf-8"))

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
        raw_request = client_sock.recv(1024).decode("utf-8")

        if raw_request:
            print(raw_request)

            request_method, request_uri, request_body, _ = utils.parse_http_request(raw_request)

            if request_method.upper() == "GET":
                response = generate_get_response(GET_RESPONSE)
            elif request_method.upper() == "POST":
                post_params = parse_params(request_body)
                username = post_params["username"]
                password = post_params["password"]

                if username == "admin" and password == "admin":
                    response = generate_get_response(POST_RESPONSE_SUCCESSFUL.format(username))
                else:
                    response = generate_get_response(POST_RESPONSE_FAILED)
            else:
                response = utils.encode_http_response(404, {}, "Invalid HTTP Method {0}".format(request_method))

            # send http response to client
            client_sock.send(response)

        # close connection
        client_sock.close()

if __name__=="__main__":
    main()
