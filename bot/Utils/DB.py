from peewee import *
from . import Configs

database = MySQLDatabase(Configs.DB.NAME, **{'host': Configs.DB.HOST, 'port': Configs.DB.PORT, 'user': Configs.DB.USER})


class UnknownField(object):
    pass


class BaseModel(Model):
    class Meta:
        database = database


class Clients(BaseModel):
    chatid = CharField(unique=True)
    lastcheck = DateTimeField()
    registered = IntegerField()

    class Meta:
        db_table = Configs.DB.TABLE


def create_table():
    try:
        create_model_tables(Clients)
    except:
        return


def store(chatid, lastcheck, registered=True, retry=5):
    if retry < 0:
        return -2
    client = Clients(chatid=chatid, lastcheck=lastcheck, registered = registered)
    try:
        client.save()
        return 1
    except IntegrityError:
        return -1
    except:
        return store(chatid, lastcheck, registered, retry-1)


def get_all_registered(retry=5):
    if retry < 0:
        return -2
    try:
        clients = Clients.select().where(Clients.registered==True)
        return clients
    except IntegrityError:
        return -1
    except:
        return get_all_registered(retry-1)


def update_time(chatid, new_time, retry=5):
    if retry < 0:
        return -2
    client = Clients.get(chatid=chatid)
    client.lastcheck = new_time
    try:
        client.save()
        return 1
    except:
        return update_time(chatid, new_time, retry-1)


def switch_registration(chatid, retry=5):
    if retry < 0:
        return -2
    client = Clients.get(chatid=chatid)
    client.registered *= -1
    try:
        client.save()
        return 1
    except:
        return switch_registration(chatid, retry-1)



def get_by_id(id, retry=5):
    if retry < 0:
        return -2
    try:
        client = Clients.get(id=id)
        return client
    except DoesNotExist:
        return -1
    except:
        return get_by_id(id, retry-1)


def get_by_less_than_time(time, retry=5):
    if retry < 0:
        return -2
    try:
        clients = Clients.select().where(Clients.lastcheck < time)
        return clients
    except DoesNotExist:
        return -1
    except:
        get_by_less_than_time(time, retry-1)


def get_by_less_than_time_registered(time, registered=True, retry=5):
    if retry < 0:
        return -2
    try:
        clients = Clients.select().where(Clients.lastcheck < time, Clients.registered == registered)
        return clients
    except DoesNotExist:
        return -1
    except:
        get_by_less_than_time_registered(time, registered, retry-1)
