import socket
import threading
from _thread import *
import DBManager
import pickle

SERVER = '127.0.0.1'
PORT = 2345
MAX_CONNECTED_PEOPLE = 2
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)

try:
    server.bind(ADDR)
except socket.error as e:
    str(e)


HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = "!CLOSE"
CONNECTED_PEOPLE = [None, None]
DB = DBManager

def send(client, data):
    try:
        client.send(pickle.dumps(data))
    except socket.error as e:
        print(e)

def threaded_client(conn, current_player):
    conn.send(pickle.dumps("Connected"))
    print("New connection")
    CONNECTED_PEOPLE[current_player] = conn
    while True:
        try:
            type = pickle.loads(conn.recv(2048))
            data = pickle.loads(conn.recv(2048))
            type_str = type["TYPE"]
            if type_str == "LOGIN":
                result = DBManager.login(data["nick"], data["password"])
                send(conn, {"USER_ID": result})
            elif type_str == "":
                pass
            else:
                pass
        except:
            break
    print("Lost connection")
    conn.close()


def start():
    current_player = 0
    server.listen(MAX_CONNECTED_PEOPLE)
    print("Waiting for a connection, Server started")
    while True:
        conn, addr = server.accept()
        print("[CONNECTED] connected to: ", addr)
        start_new_thread(threaded_client, (conn, current_player))
        current_player += 1
        print("[Active connections]", threading.activeCount() - 1)


if __name__ == '__main__':
    print("Starting server...")
    print(ADDR)
    start()
