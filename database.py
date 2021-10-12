import sqlite3

class DataBase:

    def __init__(self):
       self.process = sqlite3.connect('process.db')

    def CreateTable(self):
        self.process.execute('''CREATE TABLE PROCESS
                 (ID INT PRIMARY KEY     NOT NULL,
                 NAME           TEXT    NOT NULL,
                 GREEN_FUNC            TEXT     NOT NULL,
                 DIFF_OPERATOR        TEXT     NOT NULL);''')

        self.process.close()

    def Insert(self, number, name, green_func, diff_oper):
        self.process = sqlite3.connect('process.db')
        self.process.execute(f"INSERT INTO PROCESS (ID, NAME, GREEN_FUNC, DIFF_OPERATOR)\
              VALUES ({number},'{name}', '{green_func}', '{diff_oper}')")

        self.process.commit()
        self.process.close()
