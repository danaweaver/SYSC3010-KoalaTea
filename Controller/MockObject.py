import socket, sys, time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 1080
server_address = ("localhost", port)

while True:
    print ("Enter data to transmit: ENTER to quit")
    data = sys.stdin.readline().strip()
    if not len(data):
        break
    s.sendto(data.encode('utf-8'), server_address)
    buf, address = s.recvfrom(port)
    print(buf.decode('utf-8'))

s.shutdown(1)