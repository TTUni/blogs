import socket

HOST = "127.0.0.1"
PORT = 4444

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((HOST, PORT))
while True:
    data = raw_input("Enter message: ").strip()
    if not data:
        break

    encoded_data = data.encode("utf-8")
    client_sock.send(encoded_data)
    received_data = client_sock.recv(1024).decode("utf-8")
    print "received: {0}".format(received_data)
