import socket
import sys
import threading
from datetime import datetime


LOG_FILE_NAME = "log.txt"
DEFAULT_PORT = 9090
log_file_lock = threading.Lock()


def port_or_default(text):
    try:
        res = int(text)
        return res if 1023 < res < 65536 else DEFAULT_PORT
    finally:
        return DEFAULT_PORT


def logger(text):
    with log_file_lock and open(LOG_FILE_NAME, "a") as f:
        f.write(f"{datetime.now()} {text}\n")


logger("Server started")
args = sys.argv[1:]
main_port = port_or_default(args[0]) if len(args) > 0 else DEFAULT_PORT


def client_handler(connect, address):
    with connect:
        logger(F"Connected by {address}")
        while True:
            data = connect.recv(4096)
            msg = data.decode()
            if not data:
                logger(F"Disconnected by {address}")
                break
            logger(F"Received {msg} from {address}")
            connect.send(data)
            logger(F"Sent {msg} back to {addr}")


threads = []
with socket.socket() as s:
    s.bind(('', main_port))
    s.listen(100)
    logger(f"Listening on port: {main_port}")
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=client_handler, name='t'+str(len(threads)), args=[conn, addr])
        threads.append(t)
        t.start()
logger(f"Server stopped")
