import socket
import pickle

IS_LOGGED = False
SERVER = "127.0.0.1"
PORT = 2345
HEADER = 64


class Client:

    def __init__(self):
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

    def is_log(self):
        return self.USER_ID


