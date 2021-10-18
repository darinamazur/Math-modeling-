import sqlite3
import additional

class DataBase:

    def __init__(self):
       self.process = sqlite3.connect('process.db')

    def CreateTable(self):
        self.process.execute('''CREATE TABLE PROCESS
                 (ID INT PRIMARY KEY     NOT NULL,
                 DIM    INT       NOT NULL,
                 NAME           TEXT    NOT NULL,
                 GREEN_FUNC            TEXT     NOT NULL,
                 DIFF_OPERATOR        TEXT     NOT NULL);''')

        self.process.close()

    def Insert(self, number, dim, name, green_func, diff_oper):
        self.process = sqlite3.connect('process.db')
        self.process.execute(f"INSERT INTO PROCESS (ID, NAME, DIM, GREEN_FUNC, DIFF_OPERATOR)\
              VALUES ({number},{dim}, '{name}', '{green_func}', '{diff_oper}')")

        self.process.commit()
        self.process.close()


    def SelectProcessName(self):
        self.process = sqlite3.connect('process.db')
        cur = self.process.cursor()
        cur.execute('SELECT DISTINCT (NAME) FROM PROCESS;')
        res = cur.fetchall()
        self.process.close()
        return additional.Additional().clean_list(res)

'''
db = DataBase()
print(db.SelectProcessName())
'''