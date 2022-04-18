#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio2.py
# Asynchronous I/O inside an "asyncio" coroutine.
# python server_asyncio2.py 127.0.0.1
import asyncio, zen_utils

@asyncio.coroutine
def handle_conversation(reader, writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    while True:
        data = b''

        more_data = yield from reader.read(4096)
        if not more_data:
            if data:
                print('Client {} sent data but then closed'
                        .format(address)) #, data))
            else:
                print('Client {} closed socket normally'.format(address))
            return
        data += more_data[3:]
        # print("ini more data: ", more_data[3:])
        # print("ini data res: ", data)

        msg = str(data, encoding="ascii")
        res = zen_utils.operate(msg)

        msgres = "value: " + str(res)
        len_msgres = b"%03d" % (len(msgres),)
        answer = len_msgres + bytes(msgres, encoding="ascii")
        writer.write(answer)

if __name__ == '__main__':
    address = zen_utils.parse_command_line('asyncio server using coroutine')
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()