import sqlite3


class BotDataProvide:
    def __init__(self, date_for_tg):
        self.connection = sqlite3.connect(date_for_tg, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:
            return self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS 'reminder' (ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,"
                " date DATE, description)")

    # create user_date
    def set_user_date(self, user_id, datetime, description):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'reminder' ('user_id', 'date', 'description') VALUES (?, ?, ?)",
                                       (user_id, datetime, description))

    def del_user_date(self, user_id):
        pass

    def get_from(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM reminder WHERE user_id = ?", (user_id,)).fetchall()
