import sqlite3


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as error:
            print('Query Failed: %s\nError: %s' % (args, str(error)))

    return wrapper


class Database:
    instance = None
    __DB_LOCATION = "databases/db.sqlite"

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(Database)
            return cls.instance
        return cls.instance

    def __init__(self, db_location=None):
        try:
            if db_location is not None:
                self.connection = sqlite3.connect(db_location)
            else:
                self.connection = sqlite3.connect(self.__DB_LOCATION)
            self.cur = self.connection.cursor()
            print("SUCCESSFULLY CONNECTED TO DATABASE")
        except sqlite3.Error as error:
            print('ERROR CONNECTION TO DATABASE\nError: %s' % (str(error)))
            exit(-1)

    @exception_handler
    def get_rule_names(self):
        self.cur.execute(f"""
                SELECT RULE_NAME FROM RULES
                """)
        return self.cur.fetchall()


    @exception_handler
    def select_one(self, sql, data=None):
        self.execute(sql, data)
        row = self.cur.fetchone()
        return row

    @exception_handler
    def get_all_records(self, table_name: str):
        self.cur.execute(f"""
        SELECT * FROM {table_name}
        """)
        return self.cur.fetchall()

    @exception_handler
    def execute(self, sql, data: list = None):
        if data is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, data)

        self.commit()

    @exception_handler
    def executemany(self, sql, data):
        self.cur.executemany(sql, data)
        self.commit()

    def commit(self):
        self.connection.commit()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        if self.connection is not None:
            self.connection.close()

    def __del__(self):
        if self.connection is not None:
            self.cur.close()
            self.connection.close()