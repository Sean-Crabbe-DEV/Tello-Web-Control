from time import sleep
import socket

host = ''
port = 9000
locaddr = (host,port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("192.168.1.206", 9986))
serversocket.listen(10)
print("server created")
connection, address = serversocket.accept()

while True:
    data = connection.recv(1024).decode()
    print("Received: " + data)
    connection.send("Received".encode())
    msg = data.encode(encoding="utf-8")
    ent = sock.sendto(msg, tello_address)
