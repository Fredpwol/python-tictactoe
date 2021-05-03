import socket
import threading
import selectors
import traceback
from server import HEADER, HOST, PORT
from server.libserver import Message

select = selectors.DefaultSelector()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.setblocking(False)
s.listen(15)

select.register(s, events=selectors.EVENT_READ, data=None)

def accept_request(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    message = Message(select, conn, addr)
    select.register(conn, events=selectors.EVENT_READ, data=message)

# A Multiplexing Event Loop
while True:
    for key, mask in select.select(timeout=None):
        if key.data == None:
            accept_request(key.fileObj)
        else:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print('main: error: exception for',
                      f'{message.addr}:\n{traceback.format_exc()}')
                message.close()

