# Source: https://pymotw.com/2/socket/udp.html
import json
import socket, sys, time, random

host = sys.argv[1]
textport = sys.argv[2]
n = 10
a = 0
x = {
    "msgId": 3
}
#x = {
#    "msgId": 11,
#    "name": "SYSC3010",
#    "time": 30,
#    "temp": 50
#}
#x = {
#    "msgId": 12,
#    "teaId": 5,
#}



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = int(textport)
server_address = (host, port)

y = json.dumps(x)
print ("Sending " + y)
s.sendto(y.encode('utf-8'), server_address)
print("Receiving")
buf, address = s.recvfrom(port)
print(buf.decode('utf-8'))

s.shutdown(1)

