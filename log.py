# Reprsent a Log entry for a house
import json
import random

from utils import GenerateUUID


class Log:
    def __init__(self,nodeUUID,power,logID = GenerateUUID()):
        self.nodeUUID = nodeUUID
        self.power = power
        self.logID = logID
    
    # Convert the log of JSON
    def getJSON(self):
        return json.dumps(self.__dict__)  