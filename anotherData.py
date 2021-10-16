
import util
import yaml
import RandomGroup as rg

listName = [
    "1. Bas Greetar SwordFun",
    "2. Cheer Water bruh",
    "3. Valley Softball",
    "4. Pingpong Arrow Trakor",
    "5. Rukbee Fighting",
    "6. Petong BigBrain chess Bruh",
    "7. Football Gun",
    "8. Hockey Crossword",
    "9. Kick Udo",
    "10. Batmin Tennis",
]

DEFAULT_DATA = {
    "cataId": -1,
    "RealPrevGroup": []
}

DEFAULT_DATA2 = {
    "Tarn 1": -1,
    "Tarn 2": -1,
    "Tarn 3": -1,
    "Tarn 4": -1,
    "Tarn 5": -1,
}

thisCategoryData = {}
thisSeqData = {}
gameInd = 1


def saveData():
    global thisCategoryData, thisSeqData, gameInd
    util.fileExist("category Data.txt")
    util.fileExist("SeqData.txt")
    util.fileExist("SaveIndGame")
    with open("category Data.txt", "w") as f:
        f.write(yaml.dump(thisCategoryData))

    with open("SeqData.txt", "w") as f:
        f.write(yaml.dump(thisSeqData))

    with open("SaveIndGame", "w") as f:
        f.write(str(gameInd))


def validData():
    global thisCategoryData, thisSeqData
    for n in listName:
        for e in DEFAULT_DATA:
            if e not in thisCategoryData[n]:
                if type(DEFAULT_DATA[e]) == type(list()):
                    thisCategoryData[n][e] = list()
                else:
                    thisCategoryData[n][e] = DEFAULT_DATA[e]

    for i in range(rg.N_GROUP):
        namae = f"Group {i+1}"
        for e in DEFAULT_DATA2:
            if e not in thisSeqData[namae]:
                thisSeqData[namae][e] = DEFAULT_DATA2[e]

    saveData()


def loadData():
    global thisCategoryData, thisSeqData, gameInd
    util.fileExist("category Data.txt")
    with open("category Data.txt", "r") as f:
        content = f.read().strip()
        if content:
            thisCategoryData = yaml.load(content, Loader=yaml.FullLoader)
        else:
            thisCategoryData = {}
            for e in listName:
                thisCategoryData[e] = dict()

    util.fileExist("SeqData.txt")
    with open("SeqData.txt", "r") as f:
        content = f.read().strip()
        if content:
            thisSeqData = yaml.load(content, Loader=yaml.FullLoader)
        else:
            thisSeqData = {}
            for i in range(rg.N_GROUP):
                thisSeqData[f"Group {i+1}"] = dict()

    util.fileExist("SaveIndGame")
    with open("SaveIndGame", "r") as f:
        try:
            gameInd = int(f.read())
        except:
            gameInd = 1
    validData()


def getPrevGroupOfCategory(gameNum):
    return thisCategoryData[listName[gameNum-1]]["prevGroup"]


def getCataId(gameNum):
    return thisCategoryData[listName[gameNum-1]]["cataId"]


def getPrevGroupOfCategory(gameNum):
    return thisCategoryData[listName[gameNum-1]]["RealPrevGroup"]


def addNewGroupOfCategory(gameNum, newGroup):
    thisCategoryData[listName[gameNum-1]]["RealPrevGroup"].append(newGroup)
    saveData()


def resetPrevGroupOfCategory(gameNum):
    thisCategoryData[listName[gameNum-1]]["RealPrevGroup"].clear()
    saveData()


def getNowIndGame():
    return gameInd


def setNowIndGame(newInd):
    global gameInd
    gameInd = newInd
    saveData()


def getTarnOfGroup(numGroup, ind):
    return thisSeqData[f"Group {numGroup}"][f"Tarn {ind}"]
