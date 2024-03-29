#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        try:
            #print(url)
            addr = url.split(":")
            host = addr[0]
            port = addr[1]
        except:
            host = socket.gethostbyname(url)
            port = 80
        return host, port
    		
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        response = data.split("\r\n")
        code = response[0].split()
        return code[1]

    def get_headers(self,data):
        response = data.split("\r\n\r\n")
        return response[0]

    def get_body(self, data):
        response = data.split("\r\n\r\n")
        return response[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        if url[-1] != "/":
            url = url + "/"
        url_info = urllib.parse.urlparse(url)
        host = url_info.netloc
        path = url_info.path
        host, port = self.get_host_port(host)
        content = ("""GET %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: browser details\r\nAccept: */*\r\nAccept-Language: en\r\nConnection: close\r\n\r\n"""%(path, url_info.netloc))
        #print(content)
        #print("host : %s prot : %s\n"%(host,port))
        self.connect(host, int(port))
        self.sendall(content)
        #self.socket.shutdown(socket.SHUT_WR)
        full_data = self.recvall(self.socket)
        print(full_data)
        self.close()
        code = int(self.get_code(full_data))
        body = self.get_body(full_data)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        if url[-1] != "/":
            url = url + "/"
        url_info = urllib.parse.urlparse(url)
        host = url_info.netloc
        path = url_info.path
        host, port = self.get_host_port(host)
        to_post = ""
        if args != None:
            for key, value in args.items():
                to_post = to_post + key.replace(" ", "+") + "=" + value.replace(" ", "+") +"&"
            to_post = to_post + "\r\n"
            #print("to_post: " + to_post)
            #print(len(to_post))
            length = len(to_post)
            content = ("""POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %d\r\nUser-Agent: browser details\r\nAccept: */*\r\nAccept-Language: en\r\nConnection: close\r\n\r\n%s"""%(path, host, length, to_post))
        else:
            content = ("""POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 0\r\nUser-Agent: browser details\r\nAccept: */*\r\nAccept-Language: en\r\nConnection: close\r\n\r\n"""%(path, host))
        #print(content)
        #print("host : %s prot : %s\n"%(host,port))
        self.connect(host, int(port))
        self.sendall(content)
        #self.socket.shutdown(socket.SHUT_WR)
        full_data = self.recvall(self.socket)
        print(full_data)
        self.close()
        code = int(self.get_code(full_data))
        body = self.get_body(full_data)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
