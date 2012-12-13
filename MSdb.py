import sqlite3


class MillionSong:
    def __init__(self):
        self.lyrics=sqlite3.connect('dbs/mxm_dataset.db')
        self.meta=sqlite3.connect('dbs/track_metadata.db')
        self.tags=sqlite3.connect('artist_term.db')

    def search_word(self, word):

