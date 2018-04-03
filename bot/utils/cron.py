# Check and send news to clients

from . import RssReader, Configs

rss = RssReader.RssReader(Configs.RSS.ADDRESS)


def check_and_send_feed(db, bot):

    clients = db.get_registered_clients()

    for client in clients:

        # Find Entries newer than last time broadcast
        entries = rss.get_entries_after_time(client.last_checked_time)

        # Update broadcasts last time
        db.update_client_last_checked_time(client.chat_id)

        for entry in entries:
            # Making message by getting the entry's link
            link = rss.get_entry_link(entry)
            if not link:
                continue
            msg = link + '\n'
            # Sending message
            bot.send_message(client.chat_id, msg)
