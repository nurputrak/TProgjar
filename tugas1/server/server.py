#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket
import sys
import time
import glob

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()

        print('We have accepted a connection from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())
        
        command = ''
        flag2 = True
        while flag2:
            #message = recvall(sc, 16)
            len_command = recvall(sc, 1)
            command = recvall(sc, int(len_command))
            len_msg = recvall(sc, 5)
            message = recvall(sc, int(len_msg))
            message = message.decode()

            if(command == b'ping'):
                # print('  Message len:', repr(len_msg))
                # print('  Incoming message:', repr(message))
                print('  terima :', message)

                message = "terima : " + message
            elif(command == b'ls'):
                pathclient = "../client/"

                if(message == ''):
                    list_raw = glob.glob(pathclient + "*")
                else:
                    if(message[0] == '/'):               
                        list_raw = glob.glob(pathclient + message[1:])
                    else:
                        list_raw = glob.glob(pathclient + message)

                list = ''
                for i in list_raw:
                        list = list + (i.split("\\")[-1]) + "\n"
                    
                message = list    
            elif(command == b'get'):
                pathclient = "../client/"
                pathserver = ""
                
                message = message.split()
                path = message[0]
                filename = message[1]
                if(path[0] == '/'):
                    src_content = open(pathserver + path[1:], "rb").read()
                else:
                    src_content = open(pathserver + path, "rb").read()
                des = open(pathclient + filename, "wb+")
                des.write(src_content)

                message = "fetch:" + path + " size: " + str(len(src_content)) + " lokal:" + filename
                des.close()

            elif(command == b'put'):
                pathclient = "../client/"
                pathserver = ""
                path = message
                filename = path.split("/")[-1]

                if(path[0] == '/'):
                    src_content = open(pathclient + path[1:], "rb").read()
                    
                else:
                    src_content = open(pathclient + path, "rb").read()
                des = open(pathserver + filename, "wb+")
                des.write(src_content)

                message = "send: " + filename + " size: " + str(len(src_content)) + " remote:" + filename
                des.close()
            elif(command == b'quit'):
                sc.sendall(b'00016Farewell, client')
                sc.close()
                print('  Reply sent, socket closed')
                flag2 = False
                break
            else:
                sc.sendall(b'00016Want more input?')

            message = message.encode()
            len_message = b"%05d" % (len(message),)
            reply = len_message + message
            sc.sendall(reply)

        if(command == b'quit'):
            print("server shutdown..")
            time.sleep(1)
            break


if __name__ == '__main__':
    choices = {'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
