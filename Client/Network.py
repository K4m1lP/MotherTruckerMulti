import socket
import pickle
import sys

IS_LOGGED = False
SERVER = "127.0.0.1"
PORT = 2345
HEADER = 10

__instance = None


class Client:
    __instance = None

    @staticmethod
    def get_instance():
        if not Client.__instance:
            Client()
        return Client.__instance

    def __init__(self):
        if Client.__instance:
            raise Exception("Class is a singleton!")
        else:
            Client.__instance = self
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (SERVER, PORT)
        self.pos = self.connect()
        self.USER_ID = None

    def get_pos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def is_connected(self):
        return self.pos

    def send_obj(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def login(self, nick, password):
        self.send_obj({"TYPE": "LOGIN"})
        self.send_obj({"nick": nick, "password": password})
        user_id = pickle.loads(self.client.recv(2048))
        if "USER_ID" in user_id.keys():
            user_id_str = user_id["USER_ID"]
            if user_id_str:
                self.USER_ID = user_id_str
                return user_id_str

    def recv_data_on_open_socket(self):
        result = None
        full_msg = b''
        new_msg = True
        flag = False
        while not flag:
            msg = self.client.recv(16)
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

    def send_data_on_open_socket(self, data):
        msg = pickle.dumps(data)
        msg = bytes(f"{len(msg):<{HEADER}}", 'utf-8') + msg
        self.client.send(msg)

    def send_key(self, data_key):
        self.send_data_on_open_socket(data_key)

    def is_log(self):
        return self.USER_ID

    def is_second_connected(self):
        try:
            msg = self.recv_data_on_open_socket()
        except socket.error as e:
            return None
        else:
            return msg["RES"]

    def i_want_to_play(self):
        self.send_obj({"TYPE": "WANT_PLAY"})
        self.send_obj({"TYPE": "WANT_PLAY"})

    def logout(self):
        self.USER_ID = None

    def get_history(self):
        self.send_obj({"TYPE": "HISTORY_ASK"})
        self.send_obj({"USER_ID": self.USER_ID})
        return pickle.loads(self.client.recv(2048))

    def get_account(self):
        self.send_obj({"TYPE": "ACCOUNT_ASK"})
        self.send_obj({"USER_ID": self.USER_ID})
        return pickle.loads(self.client.recv(2048))

    def get_stats(self):
        self.send_obj({"TYPE": "STAT_ASK"})
        self.send_obj({"USER_ID": self.USER_ID})
        return pickle.loads(self.client.recv(2048))

    def get_game_status(self):
        try:
            msg1 = self.recv_data_on_open_socket()
        except socket.error as e:
            return None
        else:
            return msg1

    def block_socket(self):
        self.client.setblocking(True)

    def unlock_socket(self):
        self.client.setblocking(False)

    def close_connection(self):
        print("we should do some exit stuff here, we are in network exit callback")
