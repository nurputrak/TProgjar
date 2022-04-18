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
        flag2 = True
        command = ''
        while flag2:
            print('We have accepted a connection from', sockname)
            print('  Socket name:', sc.getsockname())
            print('  Socket peer:', sc.getpeername())
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

                pingword = "terima : " + message
                pingword = pingword.encode()
                len_ping = b"%05d" % (len(pingword),)
                pingreply = len_ping + pingword
                sc.sendall(pingreply)
            elif(command == b'ls'):
                if(message == ''):
                    list_raw = glob.glob("*")
                else:
                    if(message[0] == '/'):               
                        list_raw = glob.glob(message[1:])
                    else:
                        list_raw = glob.glob(message)

                list = ''
                for i in list_raw:
                        list = list + (i.split("\\")[-1]) + "\n"
                    
                    
                list = list.encode()
                len_list = b"%05d" % (len(list),)
                listreply = len_list + list
                sc.sendall(listreply)
            elif(command == b'get'):
                message = message.split()
                path = message[0]
                filename = message[1]
                if(path[0] == '/'):
                    src_content = open(path[1:], "rb").read()
                else:
                    src_content = open(path, "rb").read()
                des = open(filename, "wb+")
                des.write(src_content)

                msgreply = "fetch:" + path + " size: " + str(len(src_content)) + " lokal:" + filename
                des.close()

                msgreply = msgreply.encode()
                len_msgreply = b"%05d" % (len(msgreply),)
                reply = len_msgreply + msgreply
                sc.sendall(reply)
            elif(command == b'put'):
                src_content = open(message, "rb").read()
                des = open("etc/" + message, "wb+")
                des.write(src_content)

                msgreply = "send: " + message + " size: " + str(len(src_content)) + " remote:" + message
                des.close()

                msgreply = msgreply.encode()
                len_msgreply = b"%05d" % (len(msgreply),)
                reply = len_msgreply + msgreply
                sc.sendall(reply)
            elif(command == b'quit'):
                sc.sendall(b'00016Farewell, client')
                sc.close()
                print('  Reply sent, socket closed')
                flag2 = False
            else:
                sc.sendall(b'00016Want more input?')
        if(command == b'quit'):
            print("server shutdown..")
            time.sleep(1)
            break


            
    

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    #sock.sendall(b'Hi there, server')
    #msg = b'Hi there, server'
    # msg = b'Hi there, server, ini dari wahyu dan peserta kuliah'
    flag = True
    while flag:
        msg = input("> ")
        cmd = msg.split()[0]
        cmdlist = ["ping", "ls", "get", "put", "quit"]
        if(cmd in cmdlist):
            cmd = cmd.encode()
            len_cmd = b"%01d" % (len(cmd),)

            msg = ' '.join(msg.split()[1:])
            msg = msg.encode()
            len_msg = b"%05d" % (len(msg),)

            msg = len_cmd + cmd + len_msg + msg
            sock.sendall(msg)
            # reply = recvall(sock, 16)
            len_reply = recvall(sock, 5)
            reply = recvall(sock, int(len_reply))
            reply = reply.decode()
            print(reply)
            if(cmd == b'quit'): 
                print("client shutdown..")
                time.sleep(1)
                flag = False
        else:
            print("There is no command with", cmd)
    sock.close()

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
