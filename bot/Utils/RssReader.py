import feedparser
from datetime import datetime, timedelta
from time import mktime


class RssReader:
    def __init__(self, url, parse_now=True):
        self.url = url
        self.feed = None
        if parse_now is True:
            self.parse()

    def is_updated(self, cycle_seconds):
        cycle = timedelta(seconds=cycle_seconds)
        return datetime.utcnow() - cycle <= datetime.fromtimestamp(mktime(self.get_last_pubdate_parsed()))

    def set_url(self, new_url):
        self.url = new_url

    def get_url(self):
        return self.url

    def parse(self):
        self.feed = feedparser.parse(self.url)
        if len(self.feed.entries) == 0:
            print ('Unable To Connect, Reconnecting...')
            self.parse()

    def get_entries_after_time(self, time):
        entries = list()
        for e in self.feed.entries:
            if time < datetime.fromtimestamp(mktime(self.get_entry_pubdate_parsed(e))):
                entries.append(e)

        return entries

    def get_entries_latest_time(self):
        latest = self.get_entry_pubdate_parsed(self.feed.entries[0])
        for e in self.feed.entries:
            if self.get_entry_pubdate_parsed(e) > latest:
                latest = self.get_entry_pubdate_parsed(e)

        return latest

    def get_feed_title(self):
        return self.feed.feed.title

    def get_feed_description(self):
        return self.feed.feed.description

    def get_feed_link(self):
        return self.feed.feed.link

    def get_entries(self):
        return self.feed.entries

    def get_entry_title(self, id):
        return self.feed.entries[id].title

    def get_entry_description(self, id):
        return self.feed.entries[id].description

    def get_entry_link(self, id):
        return self.feed.entries[id].link

    def get_entry_link(self, entry):
        return entry.link

    def get_entry_pubdate(self, id):
        return self.feed.entries[id].published

    def get_entry_pubdate_parsed(self, id):
        return self.feed.entries[id].published_parsed

    def get_entry_pubdate_parsed(self, entry):
        return entry.published_parsed

    def get_last_title(self):
        return self.get_entry_title(0)

    def get_last_description(self):
        return self.get_entry_description(0)

    def get_last_link(self):
        return self.get_entry_link(0)

    def get_last_pubdate(self):
        return self.get_entry_pubdate(0)

    def get_last_pubdate_parsed(self):
        return self.get_entry_pubdate_parsed(0)
