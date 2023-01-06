# echo-client.py

import socket, json

# HOST = "127.0.0.1"  # The server's hostname or IP address
import time

HOST = "localhost"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

# json_data_str =\
# '''GET /post/test HTTP/1.1\r\nHost: localhost:5000\r\nContent-Type: application/json\r\nConnection: keep-alive\r\nAccept: */*\r\nContent-Length: 59\r\n\r\n
# {"key1":"Hi! Are you my server?", "key2":123.99, "key3":True}'''
# json_data_str =\
# '''GET /post/test HTTP/1.1\r\nHost: localhost:5000\r\nContent-Type: application/json\r\nConnection: keep-alive\r\nAccept: */*\r\nContent-Length: 64\r\n\r\n'''

d = {
    "key1":"Hi! Are you my server?",
    "key2":123.99,
    "key3":True
}
d_body_str = json.dumps(d)
# dest_ip_addr = "localhost"
# dest_ip_addr = "192.168.0.103"  #don't care param
json_data_header ='''GET /post/test HTTP/1.1\r\nHost: %s:%d\r\nContent-Type: application/json\r\nConnection: keep-alive\r\nAccept: */*\r\nContent-Length: %d\r\n\r\n''' \
                %(HOST, PORT,len(d_body_str))
json_data = json_data_header + d_body_str

# json_data_str = json.dumps(json_data)
while(1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((HOST, PORT))
        # s.sendall(b"Hello, world")
        s.send(bytes(json_data, "utf-8"))
        data = s.recv(1024)
        print(f"Received {data!r}")
        s.close()
        time.sleep(2)
        E = 1
E = 1
