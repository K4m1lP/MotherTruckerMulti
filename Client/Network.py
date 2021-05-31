import socket
import pickle

IS_LOGGED = False
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
        self.addr = None
        self.pos = None
        self.USER_ID = None

    def get_pos(self):
        return self.pos

    def get_nick(self):
        self.send_obj({"TYPE": "NICK_ASK"})
        self.send_obj({"TYPE": "NICK_ASK"})
        user_nick = pickle.loads(self.client.recv(2048))
        if user_nick:
            return str(user_nick)

    def connect(self, ip):
        try:
            addr = (ip, PORT)
            self.client.connect(addr)
            self.addr = addr
            self.pos = pickle.loads(self.client.recv(2048))
        except:
            print("Nie polaczono")

    def is_connected(self):
        return self.pos

    def send_obj(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)
            pass

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
            # print(e)
            return None
        else:
            print(msg["RES"])
            return msg["RES"]

    def i_want_to_play(self):
        self.send_obj({"TYPE": "WANT_PLAY"})
        self.send_obj({"TYPE": "WANT_PLAY"})
        self.unlock_socket()

    def logout(self):
        self.USER_ID = None

    def get_history(self):
        self.send_obj({"TYPE": "HISTORY_ASK"})
        self.send_obj({"TYPE": "HISTORY_ASK"})
        return pickle.loads(self.client.recv(2048))

    def get_stats(self):
        self.send_obj({"TYPE": "STAT_ASK"})
        self.send_obj({"TYPE": "STAT_ASK"})
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

    def change_password(self, nick, password, new_nick, new_password):
        if not nick or not password:
            return False
        if not new_nick:
            new_nick = None
        if not new_password:
            new_password = None
        if new_nick is None and new_password is None:
            return False
        self.send_obj({"TYPE": "CHANGE_PASS"})
        self.send_obj({"old_nick": nick, "old_pass": password, "new_nick": new_nick, "new_pass": new_password})
        return pickle.loads(self.client.recv(2048))

