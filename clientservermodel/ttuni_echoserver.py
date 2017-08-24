import socket

HOST = "127.0.0.1"
PORT = 4444

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(3)

print "server is listening on {0}:{1}".format(HOST, PORT)

running = True
while running:
    client_sock, addr = server_sock.accept()
    print "{0} connected".format(addr)

    while True:
        try:
            data = client_sock.recv(1024)
            if not data:
                break

            print "received {0}".format(data)
            client_sock.send(data)
        except ConnectionResetError:
            print "client terminated connection"
            break

server_sock.close()
