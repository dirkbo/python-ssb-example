import sqlite3


class SsbDatabase:
    def __init__(self, db_name='ssb.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS state (
               key text,
               author text,
               sequence number
             )''')
        self.conn.commit()

    def insert_message(self, message):
        # Insert a row of data
        self.c.execute("INSERT INTO state (key, author, sequence) VALUES (?, ?, ?)",
                       [message.key, message.author, message.value['sequence']])
        self.conn.commit()

    def get_previous(self, author):
        self.c.execute('''SELECT key, sequence
                     FROM state
                     WHERE author = ?
                     ORDER BY sequence''', [author])
        result = self.c.fetchone()
        if result is None:
            return (None, 0)
        else:
            return result
