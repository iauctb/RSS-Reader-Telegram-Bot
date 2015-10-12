# encoding=utf8
import telegram
from . import Configs


class BotManager(object):
    token = Configs.Server.TELEGRAM_TOKEN

    def __init__(self):
        self.bot = telegram.Bot(token=self.token)

    @staticmethod
    def json_to_update(j):
        return telegram.Update.de_json(j)

    def set_webhook(self):
        self.bot.setWebhook(Configs.Server.SERVER_ADDRESS + Configs.Server.WEB_HOOK_ADDRESS)

    def send_message(self, chat_id, message, disable=True, replyTo=None, retry=5):
        if retry < 0:
            return
        try:
            self.bot.sendMessage(chat_id, message)
        except:
            self.send_message(chat_id, message, retry-1)
