import sqlite3
import json
from sqlite3 import Error

"""
DatabaseConnection class intializes and performs all actions on the database
"""
class DatabaseConnection:
    def __init__(self):
        self.databasePath = r"C:\Users\Dana Weaver\Desktop\School\Fourth Year\SYSC3010\SYSC3010-KoalaTea\KoalaTea.db"
        #self.databasePath = r"/home/pi/Desktop/Dana/SYSC3010-KoalaTea/DatabaseServer/KoalaTea.db"
        self.conn = self.createConnection()

    """
    Create connecton to the database
    """
    def createConnection(self):
        try:
            db = sqlite3.connect(self.databasePath)
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])
        return db


    """
    Ensure database is in ready state. If not created, create it and add presets
    """
    def checkDatabaseState(self):
        if self.conn is not None:
            if self.isDbEstablished() is False: # If database isn't already established, initialize
                print("Intializing Database")
                self.initDatabase()
        else:
           print("Error: Database connection could not be created")


    """
    Intializes Tea and Alarm table and adds system preset values to each
    """
    def initDatabase(self):
        self.createTable(""" CREATE TABLE IF NOT EXISTS Tea (
                                            teaID integer PRIMARY KEY,
                                            name text NOT NULL,
                                            steepTime integer,
                                            temperature real,
                                            isCustom integer
                                           ); """)
        self.createTable(""" CREATE TABLE IF NOT EXISTS Alarm (
                                        alarmID integer PRIMARY KEY,
                                        name text NOT NULL,
                                        fileLocation text NOT NULL
                                       ); """)
        # Adding tea profile presets
        teaPresetProfile1 = ('Green Tea', 180, 150.0, 0)
        self.addTeaProfile(teaPresetProfile1)
        teaPresetProfile2 = ('Orange Pekoe', 240, 190.2, 0)
        self.addTeaProfile(teaPresetProfile2)
        teaPresetProfile3 = ('Ginger', 60, 105.5, 0)
        self.addTeaProfile(teaPresetProfile3)
        teaPresetProfile4 = ('Earl Grey', 100, 120.0, 0)
        self.addTeaProfile(teaPresetProfile4)

        # Adding alarm presets
        alarmPreset1 = ('Classic', "/home/pi/Desktop/Music/BasicAlarm.mp3")
        self.addAlarmProfile(alarmPreset1)
        alarmPreset2 = ('HIP', "/home/pi/Desktop/Music/HIP.mp3")
        self.addAlarmProfile(alarmPreset2)
        alarmPreset3 = ('Eye Of The Tiger', "/home/pi/Desktop/Music/EyeOfTheTiger.mp3")
        self.addAlarmProfile(alarmPreset3)
        alarmPreset4 = ('Mistletoe', "/home/pi/Desktop/Music/Mistletoe.mp3")
        self.addAlarmProfile(alarmPreset4)


    """
    Check if database tables 'Tea' and 'Alarm' exist
    """
    def isDbEstablished(self):
        try:
            cur = self.conn.cursor()
            sqlTable = ''' SELECT name FROM sqlite_master WHERE type='table' and name='Tea' or name='Alarm' '''
            cur.execute(sqlTable)
            tables = cur.fetchall()
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])

        if len(tables) != 2:
            print("Database is NOT initialized!")
            return False
        return True


    """
    Create database table

    createTableSql - SQL command
    """
    def createTable(self, createTableSql):
        try:
            c = self.conn.cursor()
            c.execute(createTableSql)
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])


    """
    Add entry to the database table Tea

    tea - Tea entry to add
    """
    def addTeaProfile(self, tea):
        try:
            sql = ''' INSERT INTO Tea (name, steepTime, temperature, isCustom)
                  VALUES(?,?,?,?) '''
            cur = self.conn.cursor()
            cur.execute(sql, tea)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])


    """
    Add entry to the database table Alarm

    alarm - Alarm entry to add
    """
    def addAlarmProfile(self, alarm):
        try:
            sql = ''' INSERT INTO Alarm (name, fileLocation)
                  VALUES(?,?) '''
            cur = self.conn.cursor()
            cur.execute(sql, alarm)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])


    """
    Retrieve all entries from database table Tea and returns entries in array of JSON objects
    """
    def getTeaInformation(self):
        teasJson = []
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT teaId, name, steepTime, temperature, isCustom FROM Tea")
            # Format entries into JSON objects
            header = ("teaId", "name", "steepTime", "temp", "isCustom")
            for i in cur.fetchall():
                teasJson.append(dict(zip(header, i)))
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])
        return teasJson


    """
    Retrieve all entries from database table Alarm and returns entries in array of JSON objects
    """
    def getAlarmInformation(self):
        alarmsJson = []
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT name, fileLocation FROM Alarm")
            # Format entries into JSON objects
            header = ("name", "fileLocation")
            for i in cur.fetchall():
                alarmsJson.append(dict(zip(header,i)))
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])
        return alarmsJson


    """
    Add custom entry to database table Tea and returns its tea ID

    name - Name of tea profile being added
    steepTime - Steeping time (in sec) of tea profile being added
    temp - Temperature (in degrees) of tea profile being added
    """
    def addCustomTeaProfile(self, name, steepTime, temp):
        teaId = -1
        customTeaProfile = (name, steepTime, temp, 1)
        self.addTeaProfile(customTeaProfile)
        # Confirm entry has been added and get its tea ID
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT teaID FROM Tea WHERE name=? AND steepTime=? AND temperature=? AND isCustom=1", (name, steepTime, temp))
            teaId = cur.fetchone()[0]
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])
        return teaId


    """
    Remove custom entry from database table Tea

    teaID - ID of entry to be removed
    """
    def removeCustomTeaProfile(self, teaId):
        try:
            sql = ''' DELETE FROM Tea WHERE (teaID=? AND isCustom=1)'''
            cur = self.conn.cursor()
            cur.execute(sql, (teaId,))
            self.conn.commit()
            # Check if entry actually was removed
            cur.execute("SELECT * FROM Tea WHERE teaID=?", (teaId,))
            if cur.fetchone() is None:
                return teaId
            else:
                return -1
        except sqlite3.Error as e:
            print("Database error: ", e.args[0])
