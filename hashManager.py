import json
import os 
import hashlib

hashPath = os.getcwd() + "/image/hash.md5"

def updateCurrentHash(file):
    newMd5 = ""
    with open(file, 'rb') as checked:
        # read contents of the file
        data = checked.read()    
        # pipe contents of the file through
        newMd5 = hashlib.md5(data).hexdigest()
    
    writeToHashFile(hashPath, newMd5)


def writeToHashFile(path, hash):
    config = []

    with open(path, "r") as md5File:
        config = json.load(md5File)
        md5File.close()

    config["md5"] = hash

    with open(path, "w") as newMd5:
        json.dump(config, newMd5)

updateCurrentHash(os.getcwd() + "/image/latest.png")