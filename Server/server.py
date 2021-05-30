import socket
import threading
import DBManager
import pickle
import time
from time import time_ns as get_time

import MockDB
from engine.game_engine import GameEngine
from settings import DATA_BASE
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
PER = 10
if DATA_BASE:
    DB = DBManager
else:
    DB = MockDB
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
    user = None
    while True:
        try:
            a = conn.recv(2048)
            b = conn.recv(2048)
            my_type = pickle.loads(a)
            data = pickle.loads(b)
            print(my_type)
            print(data)
            type_str = my_type["TYPE"]
            if type_str == "LOGIN":
                user = DB.login(data["nick"], data["password"])
                send(conn, {"USER_ID": True})
            elif type_str == "WANT_PLAY":
                WANT_TO_PLAY[current_player] = True
                print("ended blocking communication with ", current_player)
                unlock_socket(conn)
                return
            elif type_str == "HISTORY_ASK":
                send(conn, DB.my_battle_history(user))
            elif type_str == "STAT_ASK":
                send(conn, DB.get_stat(user))
            elif type_str == "NICK_ASK":
                send(conn, DB.get_nick(user))
            elif type_str == "CHANGE_PASS":
                send(conn, DB.change_password(data["old_nick"], data["old_pass"], data["new_nick"], data["new_pass"]))
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
    flag = True
    index = 0
    dt = 1 / 60
    end_frame_time = 0
    start_frame_time = get_time()
    print("GAME")
    end_time = None
    while flag:
        index += 1
        keys = {}
        for i in range(len(CONNECTED_PEOPLE)):
            try:
                keys[i] = recv_data_on_open_socket(CONNECTED_PEOPLE[i])
            except socket.error as er:
                keys[i] = None

        game_state = engine.update(dt, keys[0], keys[1])

        if game_state.has_ended and end_time is None:
            end_time = get_time()
        if end_time and (get_time()-end_time) * 1e-9 >= 1:
            game_state.should_exit = True

        if index % PER == 0 or game_state.should_exit:
            index = 0
            for i in range(len(CONNECTED_PEOPLE)):
                send_data_on_open_socket(CONNECTED_PEOPLE[i], game_state)

        if game_state.should_exit:
            for i in range(len(CONNECTED_PEOPLE)):
                WANT_TO_PLAY[i] = False
                # block sockets
                block_socket(CONNECTED_PEOPLE[i])
                # create threads
                player_thread = threading.Thread(target=threaded_client, args=[CONNECTED_PEOPLE[i], i])
                player_thread.start()
                THREADS.append(player_thread)

            flag = False

        end_frame_time = get_time()
        dt = (end_frame_time - start_frame_time) * 1e-9
        start_frame_time = get_time()
    return


def start():
    global WANT_TO_PLAY
    global CONNECTED_PEOPLE
    global THREADS
    n_active_clients = 0
    server.listen(MAX_CONNECTED_PEOPLE)
    print("Waiting for a connection, Server started")
    while n_active_clients < 2:
        conn, addr = server.accept()
        print("[CONNECTED] connected to: ", addr)
        conn.send(pickle.dumps("Connected"))
        CONNECTED_PEOPLE.append(conn)
        player_thread = threading.Thread(target=threaded_client, args=[conn, n_active_clients])
        player_thread.start()
        THREADS.append(player_thread)
        n_active_clients += 1
        if n_active_clients == 2:
            waiting_for_new_game()


def waiting_for_new_game():
    global THREADS
    while True:
        time.sleep(1)
        if WANT_TO_PLAY[0] and WANT_TO_PLAY[1]:
            for th in THREADS:
                th.join()
            data = {"RES": True}
            for i in range(len(CONNECTED_PEOPLE)):
                send_data_on_open_socket(CONNECTED_PEOPLE[i], data)
            # for th in THREADS:
            #    terminate_thread(th)
            # THREADS = []
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
    msg1 = bytes(f"{len(msg):<{HEADER}}", 'utf-8') + msg
    client.send(msg1)


if __name__ == '__main__':
    print("Starting server...")
    print(ADDR)
    start()
