import socket
import threading
from _thread import *
import DBManager
import pickle

from time import time_ns as get_time

from engine.game_engine import GameEngine
from utils import Player, GameState

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
WANT_TO_PLAY = [False, False]
DB = DBManager
game_state = None
keys1 = None
keys2 = None


def send(client, data):
    try:
        client.send(pickle.dumps(data))
    except socket.error as e:
        print(e)


def threaded_client(conn, current_player):
    global game_state
    global keys1
    global keys2
    global WANT_TO_PLAY
    conn.send(pickle.dumps("Connected"))
    print("New connection")
    CONNECTED_PEOPLE[current_player] = conn
    while True:
        try:
            type = pickle.loads(conn.recv(2048))
            data = pickle.loads(conn.recv(2048))
            print("Jestem klient: ", conn, " i wiadomosci ", type["TYPE"], data)
            type_str = type["TYPE"]
            if type_str == "LOGIN":
                result = DBManager.login(data["nick"], data["password"])
                send(conn, {"USER_ID": result})
            elif type_str == "KEYS":
                if current_player == 0:
                    keys1 = data
                elif current_player == 1:
                    keys2 = data
                if game_state:
                    send(conn, game_state.to_render())
                else:
                    send(conn, {"TYPE": None})
            elif type_str == "RENDER_ASK":
                pass
            elif type_str == "SECOND_PLAYER":
                print("zapytanie o drugiego", WANT_TO_PLAY[0], WANT_TO_PLAY[1])
                if WANT_TO_PLAY[0] and WANT_TO_PLAY[1]:
                    send(conn, {"RES": True})
                else:
                    send(conn, {"RES": False})
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
    print("Lost connection")
    conn.close()


def game():
    print("GAME")
    global game_state
    player1 = Player("player1")
    player2 = Player("player2")
    engine = GameEngine(player1, player2)
    flag = True
    dt = 1/60
    end_frame_time = 0
    start_frame_time = get_time()
    while flag:
        game_state = engine.update(dt, keys1, keys2)
        end_frame_time = get_time()
        dt = (end_frame_time-start_frame_time) * 1e-9
        start_frame_time = get_time()


def start():
    global WANT_TO_PLAY
    current_player = 0
    server.listen(MAX_CONNECTED_PEOPLE)
    print("Waiting for a connection, Server started")
    conn, addr = server.accept()
    print("[CONNECTED] connected to: ", addr)
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
    print("[Active connections]", threading.activeCount() - 1)
    conn, addr = server.accept()
    print("[CONNECTED] connected to: ", addr)
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
    print("[Active connections]", threading.activeCount() - 1)
    while True:
        if current_player == 2 and WANT_TO_PLAY[0] and WANT_TO_PLAY[1]:
            game()
            break




if __name__ == '__main__':
    print("Starting server...")
    print(ADDR)
    start()
