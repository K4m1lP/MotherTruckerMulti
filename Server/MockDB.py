import hashlib


def code(password):
    return hashlib.md5(password.encode()).hexdigest()


def get_nick(my_id):
    return "test_user"


def add_battle(map_name, player1result, player2result):
    return True


def my_battle_history(user_id):
    return [{
            "Date": "27-05-2021",
            "Map Name": "Malinowka",
            "Winner": "test_user"
        }]


def get_stat(user_id):
    return {
        "nick": "user_test",
        "accuracy": 25.5,
        "shots_per_battle": 2.5,
        "wins_effectiveness": 0.86,
        "all_battles": 100,
        "moderate_damage": 880
    }


def login(nick, password):
    return "loged_user_test"


def sign(nick, password):
    return True


def change_password(old_nick, old_password, new_nick=None, new_password=None):
    if (not old_nick) or (not old_password):
        return False
    log = login(old_nick, old_password)
    if not log:
        return False
    if (not new_nick) and (not new_password):
        return False
    return True


def get_new_battle():
    return {
        "MapName": "Malinowka",
        "SrcPath": "",
        "Pos1": [100, 100],
        "Pos2": [200, 200],
    }


def logout():
    pass

