from os import path


def fileExist(thisPath):
    if not path.exists(thisPath):
        with open(thisPath, "w") as f:
            f.write("")
