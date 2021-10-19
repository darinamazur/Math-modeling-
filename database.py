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

    def SelectGreenFunction(self, name, dim):
    # returns list of strings of Green functions with apecidied NAME and DIM
        self.process = sqlite3.connect('process.db')
        cur = self.process.cursor()
        cur.execute(f'SELECT GREEN_FUNC FROM PROCESS WHERE NAME = \'{name}\' AND DIM = \'{dim}\';')
        res = cur.fetchall()
        self.process.close()
        return additional.Additional().clean_list(res)

    def SelectDiffOperator(self, name, dim):
    # returns list of strings of diff opearatos with apecidied NAME and DIM
        self.process = sqlite3.connect('process.db')
        cur = self.process.cursor()
        cur.execute(f'SELECT DIFF_OPERATOR FROM PROCESS WHERE NAME = \'{name}\' AND DIM = \'{dim}\';')
        res = cur.fetchall()
        self.process.close()
        return additional.Additional().clean_list(res)


# ======================================================================================================================
#                                                     Debug functions
# ======================================================================================================================

    def ShowTables(self):
    # logs to console all tables names
        self.process = sqlite3.connect('process.db')
        cur = self.process.cursor()
        cur.execute('SELECT distinct tbl_name FROM sqlite_master order by 1;')
        res = cur.fetchall()
        self.process.close()
        print(res)

    def SelectAllTable(self, table_name):
    # logs to console all from table table_name
        self.process = sqlite3.connect('process.db')
        cur = self.process.cursor()
        cur.execute(f'SELECT * FROM {table_name}')
        res = cur.fetchall()
        self.process.close()
        for row in res:
            print(row)

    def ShowTable(self, table_name):
    # logs to console structure of table table_name
        self.process = sqlite3.connect('process.db')
        cur = self.process.cursor()
        print(f'SELECT sql FROM sqlite_master WHERE tbl_name = \'{table_name}\' AND type = \'table\';')
        cur.execute(f'SELECT sql FROM sqlite_master WHERE tbl_name = \'{table_name}\' AND type = \'table\';')
        res = cur.fetchall()
        str_res = str(res)
        res = str_res.split('\\n')
        self.process.close()
        for row in res:
            print(row)



db = DataBase()
print(db.SelectProcessName())

