from flask import Flask, request, make_response
from utils import BotManager, DB, Configs
from datetime import datetime

app = Flask(__name__)

# Create a new instance of Telegram bot
bot = BotManager.BotManager()

# Set webhook address
bot.set_webhook()


@app.route(Configs.Server.WEB_HOOK_ADDRESS, methods=["POST"])
def web_hook():
    """Telegram will send new messages to this web-hook"""

    # Translate POST request data to JSON format.
    j = request.json
    update = bot.json_to_update(j)

    if not update.message.text:
        return "invalid_message"

    # If the request is `start` command.
    if update.message.text.lower() in ["/start", "/start@sample_bot"]:
        chat_id = update.message.chat_id
        d = DB
        d.store(str(chat_id), datetime.now().date())
        bot.send_message(update.message.chat_id, Configs.Message.START_TEXT)

    # If the request is `help` command.
    if update.message.text.lower() in ["/help", "/help@sample_bot"]:
        bot.send_message(update.message.chat_id, Configs.Message.HELP_TEXT)

    # If the request is `switchreg` command.
    # `switchreg` command will switch client registeration.
    # Unregistered cients won't be notified of new rss entries anymore until they re-register.
    if update.message.text.lower() in ["/switchreg", "/switchreg@sample_bot"]:
        chat_id = update.message.chat_id
        d = DB
        d.switch_registration(str(chat_id))
        bot.send_message(update.message.chat_id, 'Your registeration switched succesfully')

    # The request was processed successfully.
    return "ok"


if __name__ == '__main__':
    app.run()
