import time
import ctypes
import socket
import pickle
import db_mock
import threading
import db_manager
from utils import Player
from settings import DATABASE
from time import time_ns as get_time
from engine.game_engine import GameEngine


"""
Yes, tey are global, we are sorry,
    we don't know how to deal with threading and networking
    without using global variables.
Client - server architecture is hard and full of zasadzkas
"""

SERVER_IP = '127.0.0.1'
PORT = 31415
MAX_CONNECTED_PEOPLE = 2
ADDR = (SERVER_IP, PORT)
HEADER = 10
CONNECTED_PEOPLE = []
WANT_TO_PLAY = [False, False]
THREADS = []
server_socket = None
SENDING_PERIOD = 4  # how many frames skip
if DATABASE: DB = db_manager
else: DB = db_mock


# helper server functions
def recv_data_on_open_socket(client):
    result = None
    msg_len = 0
    full_msg = b''
    new_msg = True
    is_received = False
    while not is_received:
        msg = client.recv(16)
        if new_msg:
            msg_len = int(msg[:HEADER])
            new_msg = False
        full_msg += msg
        if len(full_msg) - HEADER == msg_len:
            result = pickle.loads(full_msg[HEADER:])
            is_received = True
            new_msg = True
            full_msg = b''
    return result
def send_data_on_open_socket(client, data):
    success = True
    msg = pickle.dumps(data)
    msg1 = bytes(f"{len(msg):<{HEADER}}", 'utf-8') + msg
    try:
        client.send(msg1)
    except:
        success = False
    return success
def terminate_thread(thread):
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("Nonexistent thread id")
    elif res > 1:
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
            # print(my_type)
            # print(data)
            type_str = my_type["TYPE"]
            if type_str == "LOGIN":
                user = DB.login(data["nick"], data["password"])
                send(conn, {"USER_ID": True})
            elif type_str == "WANT_PLAY":
                WANT_TO_PLAY[current_player] = True
                unlock_socket(conn)
                return True
            elif type_str == "HISTORY_ASK":
                send(conn, DB.my_battle_history(user))
            elif type_str == "STAT_ASK":
                send(conn, DB.get_stat(user))
            elif type_str == "NICK_ASK":
                send(conn, DB.get_nick(user))
            elif type_str == "CHANGE_PASS":
                send(conn, DB.change_password(data["old_nick"], data["old_pass"], data["new_nick"], data["new_pass"]))
            elif type_str == "DISCONNECT":
                print("Exiting client thread")
                return False
        except socket.error as err:
            print("moj blad: ", err)
            break
def run_game():
    global CONNECTED_PEOPLE
    global THREADS
    player1 = Player("Dark Conqueror")
    player2 = Player("Knight of Light")
    engine = GameEngine(player1, player2)
    game_running = True
    frame_in_period = 0
    dt = 1 / 60
    start_frame_time = get_time()
    print("GAME")
    end_time = None
    keys = [None] * 2
    while game_running:
        frame_in_period += 1

        # get players keys (non blocking)
        for i in range(len(CONNECTED_PEOPLE)):
            try:
                keys[i] = recv_data_on_open_socket(CONNECTED_PEOPLE[i])
            except socket.error:
                keys[i] = None

        # update logic
        state = engine.update(dt, keys[0], keys[1])

        # check for endgame
        if state.has_ended and end_time is None:
            end_time = get_time()
        if end_time and (get_time()-end_time) * 1e-9 >= 1:
            state.should_exit = True
            print("Game over")

        if state.should_exit:
            for i in range(len(CONNECTED_PEOPLE)):
                WANT_TO_PLAY[i] = False
                # block sockets
                block_socket(CONNECTED_PEOPLE[i])
                # create threads
                player_thread = threading.Thread(target=threaded_client, args=[CONNECTED_PEOPLE[i], i])
                player_thread.start()
                THREADS.append(player_thread)

            game_running = False


        # send data (if period ended)
        if frame_in_period % SENDING_PERIOD == 0 or state.should_exit:
            frame_in_period = 0
            for i in range(len(CONNECTED_PEOPLE)):
                if not send_data_on_open_socket(CONNECTED_PEOPLE[i], state):
                    print("Client exited.")
                    return False

        # calculate frame time
        end_frame_time = get_time()
        dt = (end_frame_time - start_frame_time) * 1e-9
        start_frame_time = get_time()
    return True
def init_socket():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(ADDR)
        server_socket.listen(MAX_CONNECTED_PEOPLE)
    except socket.error:
        print("Failed to initialize the socket")
        exit(1)
def start_server():
    global WANT_TO_PLAY
    global CONNECTED_PEOPLE
    global THREADS
    global server_socket
    n_active_clients = 0
    # serve clients
    print("Waiting for a connection, Server started")
    while n_active_clients < 2:
        conn, addr = server_socket.accept()
        print("[CONNECTED] connected to: ", addr)
        conn.send(pickle.dumps("Connected"))
        CONNECTED_PEOPLE.append(conn)
        player_thread = threading.Thread(target=threaded_client, args=[conn, n_active_clients])
        player_thread.start()
        THREADS.append(player_thread)
        n_active_clients += 1

        if n_active_clients == 2:
            while True:
                time.sleep(1)
                for th in THREADS:
                    th.join()
                if WANT_TO_PLAY[0] and WANT_TO_PLAY[1]:
                    data = {"RES": True}
                    for i in range(len(CONNECTED_PEOPLE)):
                        send_data_on_open_socket(CONNECTED_PEOPLE[i], data)
                    run_game()
                else:
                    return


if __name__ == '__main__':
    print("Starting server...")
    print("Server address: ", ADDR)
    init_socket()

    start_server()

    server_socket.close()
