import pickle
from server import HEADER

def send_object_message(conn, event, message):
    """
    Send a python object to a socket connection.
    """
    try:
        pk = pickle.dumps(message)
        msg_len = len(pk)
        head = str(msg_len) + "|" + str(event)
        header = f"{head:<50}"
        conn.send(header)
        conn.send(pk)
    except Exception as e:
        print(e)
        return False
    return True


def read_object_message(message):
    return NotImplemented


