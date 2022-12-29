# Represent a Block
import hashlib
import random


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
    def getJSON(self):    ## <--- Refactor me :(
        jsonBlock = {
            "previousHash": self.previousHash,
            "nonce": self.nonce,
            "logList": []
        }
        
        
        for log in self.logList:
            jsonBlock["logList"].append({
                "nodeUUID":log.nodeUUID,
                "power":log.power,
                "logID": log.logID
                }) 
            
        return jsonBlock

    # Get the Block hash
    def getBlockHash(self):
        jsonBlock = self.getJSON()
        return hashlib.sha256(jsonBlock.encode('utf-8'))
