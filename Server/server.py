import socket
import threading
import DBManager
import pickle
import time
from time import time_ns as get_time
from engine.game_engine import GameEngine
from utils import Player
import ctypes


SERVER = '127.0.0.1'
PORT = 2345
MAX_CONNECTED_PEOPLE = 2
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)
HEADER = 10
CONNECTED_PEOPLE = []
WANT_TO_PLAY = [False, False]
THREADS = []
PER = 5
DB = DBManager
game_state = None

try:
    server.bind(ADDR)
except socket.error as e:
    str(e)


def terminate_thread(thread):
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def send(client, data):
    try:
        client.send(pickle.dumps(data))
    except socket.error as e:
        print(e)


def block_socket(sock):
    sock.setblocking(True)


def unlock_socket(sock):
    sock.setblocking(False)


def threaded_client(conn, current_player):
    global game_state
    global WANT_TO_PLAY
    global CONNECTED_PEOPLE

    conn.send(pickle.dumps("Connected"))
    print("New connection")
    CONNECTED_PEOPLE.append(conn)
    while True:
        try:
            a = conn.recv(2048)
            b = conn.recv(2048)
            print(len(a))
            print(len(b))
            my_type = pickle.loads(a)
            data = pickle.loads(b)
            type_str = my_type["TYPE"]
            if type_str == "LOGIN":
                result = DBManager.login(data["nick"], data["password"])
                send(conn, {"USER_ID": result})
            elif type_str == "WANT_PLAY":
                WANT_TO_PLAY[current_player] = True
            elif type_str == "ACCOUNT_ASK":
                send(conn, DBManager.get_account(data["USER_ID"]))
            elif type_str == "HISTORY_ASK":
                send(conn, DBManager.get_history(data["USER_ID"]))
            elif type_str == "STATS_ASK":
                send(conn, DBManager.get_stats(data["USER_ID"]))
        except socket.error as err:
            print("moj blad: ", err)
            break


def game():
    global game_state
    global CONNECTED_PEOPLE
    global THREADS
    # POBRAC NICKI
    player1 = Player("player1")
    player2 = Player("player2")
    engine = GameEngine(player1, player2)
    for i in range(len(CONNECTED_PEOPLE)):
        unlock_socket(CONNECTED_PEOPLE[i])
    flag = True
    index = 0
    dt = 1 / 60
    end_frame_time = 0
    start_frame_time = get_time()
    print("GAME")
    while flag:
        index += 1
        keys = {}
        for i in range(len(CONNECTED_PEOPLE)):
            try:
                keys[i] = recv_data_on_open_socket(CONNECTED_PEOPLE[i])
            except socket.error as er:
                keys[i] = None
                print("ERROR: ", er)
        game_state = engine.update(dt, keys[0], keys[1])
        if index % PER == 0:
            index = 0
            for i in range(len(CONNECTED_PEOPLE)):
                send_data_on_open_socket(CONNECTED_PEOPLE[i], game_state.to_render)
        end_frame_time = get_time()
        dt = (end_frame_time - start_frame_time) * 1e-9
        start_frame_time = get_time()


def start():
    global WANT_TO_PLAY
    global CONNECTED_PEOPLE
    global THREADS
    current_player = 0
    server.listen(MAX_CONNECTED_PEOPLE)
    print("Waiting for a connection, Server started")
    while current_player < 2:
        conn, addr = server.accept()
        print("[CONNECTED] connected to: ", addr)
        player_one_thread = threading.Thread(target=threaded_client, args=[conn, current_player])
        player_one_thread.start()
        THREADS.append(player_one_thread)
        current_player += 1
        print("[Active connections]", threading.activeCount() - 1)
        flag1 = True
        if current_player == 2:
            while flag1:
                time.sleep(1)
                if current_player == 2 and WANT_TO_PLAY[0] and WANT_TO_PLAY[1]:
                    data = {"RES": True}
                    for i in range(len(CONNECTED_PEOPLE)):
                        send_data_on_open_socket(CONNECTED_PEOPLE[i], data)
                    for th in THREADS:
                        terminate_thread(th)
                    flag1 = False
    game()


def recv_data_on_open_socket(client):
    result = None
    full_msg = b''
    new_msg = True
    flag = False
    while not flag:
        msg = client.recv(16)
        if new_msg:
            msglen = int(msg[:HEADER])
            new_msg = False
        full_msg += msg
        if len(full_msg) - HEADER == msglen:
            result = pickle.loads(full_msg[HEADER:])
            flag = True
            new_msg = True
            full_msg = b""
    return result


def send_data_on_open_socket(client, data):
    msg = pickle.dumps(data)
    msg = bytes(f"{len(msg):<{HEADER}}", 'utf-8') + msg
    client.send(msg)


if __name__ == '__main__':
    print("Starting server...")
    print(ADDR)
    start()


