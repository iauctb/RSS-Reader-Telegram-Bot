"""This module contains configuration objects."""


class Message(object):
    """This object represents a Message."""

    START_TEXT = """
    This is a sample Bot.
    This Bot will send news for you.
    """

    HELP_TEXT = """
    This is a sample Bot.
    This Bot will send news for you.
    You can unregister by using /unregister command.
    """

    # Add your custom messages here.


class DB(object):
    """This object represents DB configurations"""

    # Change Information or add other information.
    NAME = 'bot_db'
    HOST = '127.0.0.1'
    PORT = 3306
    USER = 'root'
    PASSWORD = ''

    # The table which the clients data will be stored.
    CLIENTS_TABLE = 'clients'


class RSS(object):
    """This object represents RSS configurations"""

    # The RSS address
    ADDRESS = 'http://www.theguardian.com/world/rss'


class Server(object):
    """This object represents Server configurations"""

    # The server address
    SERVER_ADDRESS = 'https://bot.server.com'

    # The web-hook address
    WEB_HOOK_ADDRESS = '/web_hook'

    # Your Bot secret token.
    TELEGRAM_TOKEN = 'Very Secret Token!'
