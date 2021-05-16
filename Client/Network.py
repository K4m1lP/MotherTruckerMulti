import socket
import pickle

IS_LOGGED = False
SERVER = "127.0.0.1"
PORT = 2345
HEADER = 64

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

    def send_key(self, data_key):
        self.send_obj({"TYPE": "KEYS"})
        self.send_obj(data_key)
        msg = pickle.loads(self.client.recv(2048))
        if isinstance(msg, dict) and "TYPE" in msg.keys():
            return None
        else:
            return msg

    def is_log(self):
        return self.USER_ID

    def is_second_connected(self):
        self.send_obj({"TYPE": "SECOND_PLAYER"})
        self.send_obj({"TYPE": "SECOND_PLAYER"})
        msg = pickle.loads(self.client.recv(2048))
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
