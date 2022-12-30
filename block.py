# Represent a Block
import hashlib
import json
import random

from log import Log


class Block:
    
    logList = []
    previousHash = 0
    nonce = 0
    
    def __init__(self):
        self.logList = []
    
    # Add a log to the Block
    def addLog(self,log):
        self.logList.append(log)
    
    # Convert the Block to JSON
    def toJSON(self):  
        jsonBlock = {
            "previousHash": self.previousHash,
            "nonce": self.nonce,
            "logList": []
        }
        
        
        for log in self.logList:
            jsonBlock["logList"].append(log.toJSON()) 
            
        return jsonBlock
    
    def fromJSON(json):
        tmpBlock  = Block()
        tmpBlock.previousHash = json["previousHash"]
        tmpBlock.nonce = json["nonce"]
        
        for log in json["logList"]:
            tmpBlock.addLog(Log.fromJSON(log))
        
        return tmpBlock

    # Get the Block hash
    def getBlockHash(self):
        jsonBlock = str(json.dumps(self.toJSON()))
        return hashlib.sha256(jsonBlock.encode('utf-8')).hexdigest()
    
    # Mine the current block
    def mine(self):
        while (self.getBlockHash()[:4] != "0000"):
            self.nonce += 1
        
        print("Block mined :  "+self.getBlockHash())