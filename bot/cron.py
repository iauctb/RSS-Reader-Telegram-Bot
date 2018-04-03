# Check and send news to clients

from utils import RssReader, Configs, DB, BotManager
import schedule
from time import sleep

# Initialize Rss reader
rss = RssReader.RssReader(Configs.RSS.ADDRESS)

# Initialize database connection
DB.init()

# Create a new instance of Telegram bot
bot = BotManager.BotManager()


def check_and_send_feed():

    clients = DB.get_registered_clients()

    for client in clients:

        # Find Entries newer than last time broadcast
        entries = rss.get_entries_after_time(client.last_checked_time)

        # Update broadcasts last time
        DB.update_client_last_checked_time(client.chat_id)

        for entry in entries:
            # Making message by getting the entry's link
            link = rss.get_entry_link(entry)
            if not link:
                continue
            msg = link + '\n'
            # Sending message
            bot.send_message(client.chat_id, msg)


if __name__ == '__main__':
    print("Running Cron...")
    check_and_send_feed()
    schedule.every(Configs.CRON.CHECK_INTERVALS).seconds.do(check_and_send_feed)

    while 1:
        schedule.run_pending()
        sleep(1)
