import random
import util
import db
import configparser

N_GROUP = 40


def groupAssignAll():
    listOfIds = db.getAllDiscordUid()
    random.shuffle(listOfIds)
    ind = 0
    result = [list() for i in range(N_GROUP)]
    for e in listOfIds:
        result[ind].append(e[0])
        ind = (ind+1) % N_GROUP

    util.fileExist("SaveInd")
    with open("SaveInd", "w") as f:
        f.write(str(ind))

    util.fileExist("Group Assign Result.txt")
    with open("Group Assign Result.txt", "w") as f:
        for i in range(N_GROUP):
            f.write(f"-Group {i+1}-\n")
            for e in result[i]:
                stuId = db.getStuCodeFromDiscordId(e)[6:]
                f.write(f"{stuId}\n")
            f.write(f"\n\n")

    return result.copy()


def addingGroup(newId):
    result = [list() for i in range(N_GROUP)]

    util.fileExist("SaveInd")
    with open("SaveInd", "r") as f:
        content = f.read().strip()
        if content:
            ind = int(content)
        else:
            ind = 0

    if type(newId) == type(list()):
        for e in newId:
            result[ind].append(e)
            ind = (ind+1) % N_GROUP
    else:
        result[ind].append(newId)
        ind = (ind+1) % N_GROUP

    util.fileExist("SaveInd")
    with open("SaveInd", "w") as f:
        f.write(str(ind))

    return result.copy()


if __name__ == "__main__":
    thisConfig = configparser.ConfigParser()
    thisConfig.read("BigConfig.ini")
    thisToken = thisConfig["bot"]["TOKEN"].strip()

    print("Connect to SQL")
    db.connect(thisConfig)

    result = groupAssignAll()
    for i in range(N_GROUP):
        print(f"--Group {i+1}--")
        for e in result[i]:
            print(e)
        print()
