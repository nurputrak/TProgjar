#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/zen_utils.py
# Constants and routines for supporting a certain network conversation.

import argparse, socket, time
import sys
value = 0

def parse_command_line(description):
    """Parse command line and return a socket address."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address

def create_srv_socket(address):
    """Build and return a listening server socket."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener

def accept_connections_forever(listener):
    """Forever answer incoming connections on a listening socket."""
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock, address)

def handle_conversation(sock, address):
    """Converse with a client over `sock` until they are done talking."""
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error: {}'.format(address, e))
    finally:
        sock.close()

def handle_request(sock):
    """Receive a single client request on `sock` and send the answer."""
    global value
    # print("ini sock: ", sock)
    len_msg = recvall(sock, 3)
    message = recvall(sock, int(len_msg))
    message = str(message, encoding="ascii")

    value = operate(message)

    message = "value = : " + str(value)
    len_msg = b"%03d" % (len(message),) 
    message = len_msg + bytes(message, encoding="ascii")
    sock.sendall(message)

def operate(msg):
    global value
    ii = msg.split()

    if(ii[0] == 'ADD'):
        value += int(ii[1])
    elif(ii[0] == 'DEC'):
        value -= int(ii[1])
    else:
        print("Unknown cmd...: ", ii)
        sys.exit(0)

    return value
    
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

