import sqlite3
from sqlite3 import Error

"""
DatabaseConnection class intializes and performs all actions on the database
"""
class DatabaseConnection:
    def  __init__(self):
        databasePath = r"path"
        conn = None

    """
    Create database connection, create Tea and Alarm tables and populate with
    preset data
    """
    def initDatabase(self):
        try:
            conn = sqlite3.connect(path)
        except Error as e:
            print(e)
        if conn is not None:
            this.createTable(conn, """ CREATE TABLE IF NOT EXISTS Tea (
                                            teaID integer PRIMARY KEY,
                                            name text NOT NULL,
                                            time integer,
                                            temperature real,
                                            isCustom integer
                                           ); """)
            this.createTable(conn, """ CREATE TABLE IF NOT EXISTS Alarm (
                                            alarmID integer PRIMARY KEY,
                                            name text NOT NULL,
                                            location text NOT NULL,
                                           ); """)
        else:
            print("Error: Database connection could not be created")
        # Adding tea profile presets
        teaPresetProfile1 = ('Green Tea', 180, 150.0, 0)
        addTeaProfile(conn, teaPresetProfile1)
        teaPresetProfile2 = ('Orange Pekoe', 240, 190.2, 0)
        addTeaProfile(conn, teaPresetProfile2)
        teaPresetProfile3 = ('Ginger', 60, 105.5, 0)
        addTeaProfile(conn, teaPresetProfile3)
        teaPresetProfile4 = ('Earl Grey', 100, 120.0, 0)
        addTeaProfile(conn, teaPresetProfile4)

        # Adding alarm presets
        alarmPreset1 = ('Classic', "this/is/a/test1")
        addAlarmProfile(conn, alarmPreset1)
        alarmPreset2 = ('Waves', "this/is/a/test2")
        addAlarmProfile(conn, alarmPreset2)
        alarmPreset3 = ('Piano', "this/is/a/test3")
        addAlarmProfile(conn, alarmPreset3)
        alarmPreset4 = ('Drip', "this/is/a/test4")
        addAlarmProfile(conn, alarmPreset4)

    """
    Add entry to the database table Tea

    tea - Tea entry to add
    """
    def addTeaProfile(self, tea):
        sql = ''' INSERT INTO Tea(name,time,temperature, isCustom)
              VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, tea)
        return cur.lastrowid

    """
    Add entry to the database table Alarm

    alarm - Alarm entry to add
    """
    def addAlarmProfile(self, alarm):
        sql = ''' INSERT INTO Alarm(name,location)
              VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, alarm)
        return cur.lastrowid

    """
    Create database table

    createTableSql - SQL command
    """
    def createTable(self, createTableSql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    """
    Retrieve all entries from database table Tea
    """
    def getTeaInformation(self):
         cur = conn.cursor()
         cur.execute("SELECT * FROM Tea")
         rows = cur.fetchall()
         return rows

    """
    Retrieve all entries from database table Alarm
    """
    def getAlarmInformation(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM Alarm")
        rows = cur.fetchall()
        return rows

    """
    Add custom entry to database table Tea

    name - Name of tea profile being added
    time - Steeptime (in sec) of tea profile being added
    temp - Temperature (in degrees) of tea profile being added
    """
    def addCustomTeaInformation(self, name, time, temp):
        customTeaProfile = (name, time, temp, 1)
        addTeaProfile(conn, customTeaProfile)

    """
    Remove custom entry from database table Tea

    teaID - ID of entry to be removed
    """
    def removeCustomTeaInformation(self, teaID):
        sql = ''' DELETE FROM Tea WHERE (id=? AND isCustom=1)'''
        cur = conn.cursor()
        cur.execute(sql, (teaID,))
        conn.commit()
