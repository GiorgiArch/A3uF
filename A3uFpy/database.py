import sqlite3 as sl
import sys,os,random,glob,time,json
import datetime


class Data:
    def __init__(self, path):
        self.database_version = "alpha"
        self.valid = False
        self.path = path
        # Database description, each entry is a measure.
        self.database_description = """
            CREATE TABLE MEASURES (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                version TEXT,
                timestamp TEXT,
                site TEXT,
                unit TEXT,
                stratum TEXT,
                level TEXT,
                weight FLOAT,
                area FLOAT,
                image_front BLOB,
                image_back BLOB,
                spectral_data BLOB,
                notes TEXT,
                analyzed BOOLEAN
            );
            """

    def database_connect(self, path):
        """
        Connect to the database
        """
        try:
            self.connection = sl.connect(path)
        except Exception as e:
            return str(e)

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

    def check_site(self, value):
        error_message = "you need to use the trinomial system CA-SITE-NUMBER"
        try:
            if len(value.split("-"))!=3:
                return error_message
        except Exception as e:
            return error_message


    def check_stratum(self, value):
        return

    def check_level(self, value):
        return

    def check_unit(self, value):
        return

    def check_notes(self,value):
        error_messagge = "note cannot be longer than 250 characters"
        try:
            if len(value)> 250:
                return error_message
        except Exception as e:
            return error_message

    def insert(self, site, unit, stratum, level, weight, image_front, image_back, notes):
        """
        Add an element to the database.
        View
        """
        # check value example
        err = self.check_site(site)
        if err is not None:
            return err
        err = self.check_unit(unit)
        if err is not None:
            return err
        err = self.check_stratum(stratum)
        if err is not None:
            return err
        err = self.check_level(level)
        if err is not None:
            return err
        timestamp = str(datetime.datetime.now())
        cur = self.connection.cursor()
        insert_string = "INSERT INTO MEASURES (version, timestamp, site, unit, stratum, level, notes) VALUES(?, ?, ?, ?, ?, ?, ?);"
        cur.execute(insert_string, (self.database_version, timestamp, site, unit, stratum, level, notes))
        self.connection.commit()
        return

    def list_all(self):
        """
        Lists all entry in the database and prints them nicely on terminal.
        """

    def search(self, name_of_the_field, value_of_the_field):
        """
        Search in the database for all elements matching a field
        """
        return
