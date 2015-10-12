from Utils import RssReader, DB, BotManager, Configs
from datetime import datetime
from time import mktime

rss = RssReader.RssReader(Configs.RSS.ADDRESS)
db = DB
entries = rss.get_entries()
clients = db.get_all_registered()

for client in clients:

    # Find Entries newer than last time broadcast.
    entries = rss.get_entries_after_time(client.lastcheck)
    bot = BotManager.BotManager()

    # Update broadcasts last time.
    db.update_time(client.chatid, datetime.fromtimestamp(mktime(rss.get_entries_latest_time())))
    for entry in entries:
        # Making message by getting the entry's link.
        msg = rss.get_entry_link(entry) + '\n'
        # Sending message.
        bot.send_message(client.chatid, msg)