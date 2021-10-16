import configparser
import mysql.connector

dbconnector = None


def connect(config):
    global dbconnector
    dbconnector = mysql.connector.connect(host=config['SQL']['ipHost'],
                                          user=config['SQL']['username'],
                                          password=config['SQL']['password'],
                                          database=config['SQL']['database'],
                                          port=int(config['SQL']['port']))


def getDataOfStuCode(studentCode):
    mycursor = dbconnector.cursor(buffered=True)
    mycursor.execute(
        f"SELECT * FROM `sophomore_day` WHERE `std_id` = '{studentCode}'")
    return mycursor.fetchall()  # ? Will return as list


def requestAttend(userDiscordId, studentCode):
    mycursor = dbconnector.cursor(buffered=True)
    mycursor.execute(
        f"UPDATE `sophomore_day` SET `uid` = '{userDiscordId}' WHERE `std_id` = '{studentCode}'")
    dbconnector.commit()


def getDiscordIdFromStuCode(studentCode):
    mycursor = dbconnector.cursor(buffered=True)
    mycursor.execute(
        f"SELECT `uid` FROM `sophomore_day` WHERE `std_id` = '{studentCode}'")
    return int(mycursor.fetchall()[0][0])  # ? Will return as list


def getStuCodeFromDiscordId(disId):
    mycursor = dbconnector.cursor(buffered=True)
    mycursor.execute(
        f"SELECT `std_id` FROM `sophomore_day` WHERE `uid` = '{disId}'")
    return mycursor.fetchall()[0][0]  # ? Will return as list


def getAllDiscordUid():
    mycursor = dbconnector.cursor(buffered=True)
    mycursor.execute(
        f"SELECT `uid` FROM `sophomore_day` WHERE std_id LIKE '64%' AND uid IS NOT NULL;")
    return mycursor.fetchall()  # ? Will return as list


if __name__ == '__main__':
    thisConfig = configparser.ConfigParser()
    thisConfig.read("BigConfig.ini")
    thisToken = thisConfig["bot"]["TOKEN"].strip()

    print("Connect to SQL")
    connect(thisConfig)
    print(getAllDiscordUid())
