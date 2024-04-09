import sqlite3
import os
from config.settings import DB_PATH

class KeyWord:

    def __init__(self, word, number_in_dict, language):
        self.word = word
        self.number_in_dict = number_in_dict
        self.language = language

    def __repr__(self):
        return f'{self.word} ({self.language}:{self.number_in_dict})'

    def __str__(self):
        return self.word

class KeyWordDB:

    def __init__(self):
        self.db_path = DB_PATH
        self._check_db()

    def _check_db(self):
        if not os.path.exists(self.db_path):
            raise ValueError('Db no exists')

    def get_random_key(self, language_code:str, range:tuple):
        start, end = range
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        command = f"SELECT * FROM keyword WHERE number_in_dict BETWEEN {start} AND {end} AND language = '{language_code}' ORDER BY RANDOM() LIMIT 1"
        cursor.execute(command)
        row = cursor.fetchone()
        try:
            pk, word, lang, number_in_dict = row
            keyword = KeyWord(word, number_in_dict, lang)
            return keyword
        except TypeError as error:
            print(error)
            print(language_code, range)
            raise error

    def keys_stat(self):
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        command = """
        SELECT language,COUNT(*) FROM keyword GROUP BY language;
        """
        cursor.execute(command)
        rows = cursor.fetchall()
        for row in rows:
            lang, count = row
            print(lang, count)

keyword_db = KeyWordDB()
