import pymongo
import hashlib

'''myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient["GameDB"]
'''

def code(password):
    return hashlib.md5(password.encode()).hexdigest()


def login(nick, password):
    '''my_user_info = db["Users"].find({"name": nick})
    len = db["Users"].count_documents({"name": nick})
    if len == 1 and my_user_info[0]["password"] == code(password):
        return str(my_user_info[0]["_id"])
    return None'''
    return "some user id"

def sing(nick, password):
    # db["User"].insert_one({"name": nick, password: code(password)})
    pass

def get_account(user_id):
    pass

def get_history(user_id):
    pass

def get_stat(user_id):
    pass

if __name__ == '__main__':
    print(login("TOMIKSON","tomekjestsuper"))


def get_stats(param):
    return None