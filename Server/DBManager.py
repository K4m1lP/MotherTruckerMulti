from datetime import datetime

import random
import hashlib
import mongoengine as me

me.connect("GameDB")


class User(me.Document):
    Name = me.StringField(required=True)
    Password = me.StringField(max_length=50)

    def __repr__(self):
        return str(self.id)


class UserInBattle(me.Document):
    UserId = me.ReferenceField(User)
    NumOfShots = me.DecimalField(min_value=0, max_value=100)
    NumOfShotsOnTarget = me.DecimalField(min_value=0, max_value=100)
    GivenDamage = me.DecimalField(min_value=0, max_value=1000)
    GetDamage = me.DecimalField(min_value=0, max_value=1000)
    OpponentHp = me.DecimalField(min_value=0, max_value=1000)


class Battle(me.Document):
    MapName = me.StringField(required=True, max_length=50)
    Date = me.DateField(required=True)
    Winner = me.ReferenceField(User)
    UsersResults = me.ListField(me.ReferenceField(UserInBattle))
    UsersInvolved = me.ListField(me.ReferenceField(User))


class Map(me.Document):
    MapName = me.StringField(max_length=50, unique=True)
    SrcPath = me.StringField(required=True)
    InitPos1 = me.fields.PointField()
    InitPos2 = me.fields.PointField()


def code(password):
    return hashlib.md5(password.encode()).hexdigest()


def get_nick(my_id):
    return str(User.objects(id=my_id).first().Name)


def add_battle(map_name, player1result, player2result):
    pl1res = UserInBattle()
    pl2res = UserInBattle()
    pl1res.UserId = User.objects(id=player1result["user_id"]).first()
    pl1res.NumOfShots = player1result["num_of_shots"]
    pl1res.NumOfShotsOnTarget = player1result["num_of_shots_on_target"]
    pl1res.GivenDamage = player1result["given_damage"]
    pl1res.GetDamage = player1result["my_damage"]
    pl1res.OpponentHp = player1result["opponent_hp"]

    pl2res.UserId = User.objects(id=player2result["user_id"]).first()
    pl2res.NumOfShots = player2result["num_of_shots"]
    pl2res.NumOfShotsOnTarget = player2result["num_of_shots_on_target"]
    pl2res.GivenDamage = player2result["given_damage"]
    pl2res.GetDamage = player2result["my_damage"]
    pl2res.OpponentHp = player2result["opponent_hp"]

    pl1res.save()
    pl2res.save()

    pl1_id = User.objects(id=player1result["user_id"]).first()
    pl2_id = User.objects(id=player2result["user_id"]).first()

    winner = None
    if pl1res.GivenDamage == pl1res.OpponentHp:
        winner = pl1_id
    else:
        winner = pl2_id

    bat = Battle()
    bat.MapName = map_name
    bat.Date = datetime.utcnow
    bat.Winner = winner
    bat.UsersResults = [pl1res, pl2res]
    bat.UsersInvolved = [pl1_id, pl2_id]
    bat.save()

def my_battle_history(user_id):
    history = Battle.objects()
    user = User.objects(id=user_id).first()
    j = []
    for his in history:
        if user in his.UsersInvolved:
            j.append(his)
    res = []
    for bat in j:
        winner_id = bat.Winner.id
        winner_nick = User.objects(id=winner_id).first().Name
        res.append({
            "Date": bat.Date,
            "Map Name": bat.MapName,
            "Winner": winner_nick
        })
    return res

def get_stat(user_id):
    data = UserInBattle.objects(UserId=user_id)
    history = Battle.objects()
    user = User.objects(id=user_id).first()
    battles = []
    for his in history:
        if user in his.UsersInvolved:
            battles.append(his)
    wins = 0
    wins_effectiveness = 0
    all_battles = len(battles)
    for bat in battles:
        if bat.Winner.id == user_id:
            wins += 1
    if all_battles > 0:
        wins_effectiveness = wins / all_battles
    accuracy = 0
    shots_in_target = 0
    shots = 0
    shots_per_battle = 0
    num_of_battles = len(data)
    all_opponent_hp = 0
    all_given_damage = 0
    moderate_damage = 0
    for bat in data:
        shots_in_target += bat.NumOfShotsOnTarget
        shots += bat.NumOfShots
        all_opponent_hp += bat.OpponentHp
        all_given_damage += bat.GivenDamage
    if shots > 0:
        accuracy = shots_in_target / shots
    if num_of_battles > 0:
        shots_per_battle = shots / num_of_battles
    if all_opponent_hp > 0:
        moderate_damage = all_given_damage / all_opponent_hp
    return {
        "nick": User.objects(id=user_id).first().Name,
        "accuracy": accuracy,
        "shots_per_battle": shots_per_battle,
        "wins_effectiveness": wins_effectiveness,
        "all_battles": all_battles,
        "moderate_damage": moderate_damage
    }

def login(nick, password):
    if nick and password:
        my_user_info = User.objects(Name=nick, Password=code(password))
        if my_user_info:
            res = my_user_info[0]
            return res.id
    return None


def sign(nick, password):
    l1 = User.objects(Name=nick)
    l2 = User.objects(Password=code(password))
    if l1 or l2:
        return False
    User(Name=nick, Password=code(password)).save()
    return True


def change_password(old_nick, old_password, new_nick=None, new_password=None):
    if (not old_nick) or (not old_password):
        return False
    log = login(old_nick, old_password)
    if not log:
        return False
    if (not new_nick) and (not new_password):
        return False
    if (not new_nick) and new_password:
        new_nick = old_nick
    if (not new_password) and new_nick:
        new_password = old_password
    User.objects(Name=old_nick).first().update(Name=new_nick, Password=code(new_password))
    return True


def get_new_battle():
    map_list = Map.objects()
    if map_list:
        chosen_map = random.choice(map_list)
        return {
            "MapName": chosen_map.MapName,
            "SrcPath": chosen_map.SrcPath,
            "Pos1": chosen_map.InitPos1["coordinates"],
            "Pos2": chosen_map.InitPos2["coordinates"],
        }
    return False


def add_map(src_path, name, init_pos1, init_pos2):
    if Map.objects(MapName=name):
        return False
    mp = Map()
    mp.MapName = name
    mp.SrcPath = src_path
    mp.InitPos1 = [init_pos1[0], init_pos1[1]]
    mp.InitPos2 = [init_pos2[0], init_pos2[1]]
    mp.save()
    return True

def delete_map(self, map_name):
    Map.objects(MapName=map_name).first().delete()



def i_want_to_play():
    # get init map
    map_name = get_new_battle()["MapName"]
    # get random object
    user1id = random.choice(User.objects()).id
    user2id = random.choice(User.objects()).id
    while user1id == user2id:
        user2id = random.choice(User.objects()).id
    num_of_shots = int(random.uniform(1, 10))
    num_of_shots_on_target = int(random.uniform(1, 5))
    damage1 = int(random.uniform(1, 1000))
    player_result = {
        "user_id": user1id,
        "num_of_shots": num_of_shots,
        "num_of_shots_on_target": num_of_shots_on_target,
        "given_damage": damage1,
        "my_damage": 1000,
        "opponent_hp": 1000
    }
    num_of_shots = int(random.uniform(1, 10))
    player2_result = {
        "user_id": user2id,
        "num_of_shots": num_of_shots,
        "num_of_shots_on_target": num_of_shots_on_target,
        "given_damage": 1000,
        "my_damage": damage1,
        "opponent_hp": 1000
    }
    add_battle(map_name, player_result, player2_result)


def get_all_battles():
    history = Battle.objects()
    res = []
    for bat in history:
        winner_id = bat.Winner.id
        winner_nick = User.objects(id=winner_id).first().Name
        res.append({
            "Date": bat.Date,
            "Map Name": bat.MapName,
            "Winner": winner_nick
        })
    return res

def get_all_users():
    users = User.objects()
    return [us.Name for us in users]

if __name__ == '__main__':
    pass


