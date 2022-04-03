import sqlite3 as sl
import sys,os,random,glob,time,json

global _database_version

class Data:
    def __init__(self, path):
        _database_version = "alpha"
        self.valid = False
        self.path = path
        # Database description, each entry is a measure.
        self.database_description = """
            CREATE TABLE MEASURES (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                version TEXT,
                timestamp REAL,
                image BLOB,
                sample_id INTEGER NOT NULL
            );
            """

    def create_new_db(self, path):
        '''
        Creates a new database.

        Arguments
            -path: path where to create the new database including filename.

        Returns:
            - False if database creation went right, a string if there was an error.
        '''
        # check if the database path already exists, if not create a new one
        if not (os.path.exists(path)):
            try:
                self.connection = sl.connect(path)
            except Exception as e:
                return str(e)
        else:
            return "Path to the database exists, cannot create new database."

        # Actually write the database and commit.
        try:
            with self.connection:
                self.connection.execute(self.database_description)
                self.connection.commit()
            self.valid = True
            self.path = path
        except Exception as e:
            return str(e)


    def check(self):
        """
        Check if the database is valid.

        Returns boolean
        """
        if self.valid:
            with self.connection:
                cursor = self.connection.cursor()
                exist = len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MEASURES';").fetchall())
                if exist == 1:
                    return True
                else:
                    self.valid = False
                    return False
        else:
            return False
