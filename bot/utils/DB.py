from peewee import *
from . import Configs
from time import time

# Instance of the database (MySQL)
db = MySQLDatabase(
    Configs.DB.NAME,
    **{
        'host': Configs.DB.HOST,
        'port': Configs.DB.PORT,
        'user': Configs.DB.USER,
        'password': Configs.DB.PASSWORD
    }
)


# Base model for all models
class BaseModel(Model):
    class Meta:
        database = db


# Bot clients model
class Client(BaseModel):
    chat_id = CharField(unique=True)
    last_checked_time = TimestampField()
    is_registered = BooleanField()

    class Meta:
        table_name = Configs.DB.CLIENTS_TABLE


# Initialize database and dao
def init():
    # Connect to database
    db.connect()
    # Create tables if they don't exist
    db.create_tables([Client])


# Add new client
def add_client(chat_id):
    try:
        client = Client.get(Client.chat_id == chat_id)
        client.is_registered = True
    except DoesNotExist:
        client = Client(chat_id=chat_id, last_checked_time=time(), is_registered=True)
    client.save()
    return client


# Switch registration of the client
def switch_registration(chat_id):
    try:
        client = Client.get(Client.chat_id == chat_id)
        if client.is_registered:
            client.is_registered = False
        else:
            client.is_registered = True
            client.last_checked_time = time()
        client.save()
    except DoesNotExist:
        client = None
    return client


# Get list of registered clients
def get_registered_clients():
    clients = Client.select().where(Client.is_registered)
    return clients


def update_client_last_checked_time(chat_id):
    Client.update(last_checked_time=time()).where(Client.chat_id == chat_id).execute()
