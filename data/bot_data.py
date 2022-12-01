import sqlite3


class BotDataProvide:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:
            return self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS 'reminder' (ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE, "
                "user_data DATE)")

    # create user_date
    def set_user_date(self, user_values):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'reminder' ('user_values') VALUES (?)", (user_values))

    # TODO implement later
    def del_user_date(self):
        pass
        # with self.connection:
        #     return self.cursor.execute("DELETE FROM 'reminder' WHERE user_values")

    # get values and date
    def get_from(self):
        with self.connection:
            return self.cursor.execute("SELECT 'user_values', 'user_data' FROM 'reminder'")