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
    choices = {'client': client}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
