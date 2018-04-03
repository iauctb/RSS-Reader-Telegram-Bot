import feedparser
from datetime import datetime, timedelta
from time import mktime


class RssReader(object):
    def __init__(self, url, parse_now=True):
        self.url = url
        self.feed = None
        if parse_now is True:
            self.parse()

    def parse(self):
        self.feed = feedparser.parse(self.url)
        if len(self.feed.entries) == 0:
            print('Unable To Connect, Reconnecting...')
            self.parse()

    def get_entries_after_time(self, time):
        entries = list()
        for e in self.feed.entries:
            if time < datetime.fromtimestamp(mktime(self.get_entry_pubdate_parsed(e))):
                entries.append(e)

        return entries

    def get_entry_link(self, entry):
        try:
            return entry.link
        except AttributeError:
            return None

    def get_entry_pubdate_parsed(self, entry):
        return entry.published_parsed

    def get_last_pubdate_parsed(self):
        return self.get_entry_pubdate_parsed(0)
