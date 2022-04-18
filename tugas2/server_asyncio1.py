#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio1.py
# Asynchronous I/O inside "asyncio" callback methods.

import asyncio, zen_utils

class ZenServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.data = b''
        print('Accepted connection from {}'.format(self.address))

    def data_received(self, data):
        self.data += data
        # print("ini data: ", data[3:])
        msg = str(data[3:], encoding="ascii")
        res = zen_utils.operate(msg)
        
        msgres = "value: " + str(res)
        len_msgres = b"%03d" % (len(msgres),)
        answer = len_msgres + bytes(msgres, encoding="ascii")
        self.transport.write(answer)

    def connection_lost(self, exc):
        if exc:
            print('Client {} error: {}'.format(self.address, exc))
        elif self.data:
            print('Client {} sent data but then closed'
                  .format(self.address)) #, self.data))
        else:
            print('Client {} closed socket'.format(self.address))

if __name__ == '__main__':
    address = zen_utils.parse_command_line('asyncio server using callbacks')
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ZenServer, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
