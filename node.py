import hashlib
import json
import random
import sys

from flask import Flask
import requests

# List of the blocks 
blockchain = []

# List of the nodes we know
nodes = []

# Reprsent a Log entry for a house
class Log:
    def __init__(self,nodeUUID,power):
        self.nodeUUID = nodeUUID
        self.power = power
    
    # Convert the log of JSON
    def getJSON(self):
        return json.dumps(self.__dict__)  
        

# Represent a Block
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
                "power":log.power
                }) 
            
        return jsonBlock

    # Get the Block hash
    def getBlockHash(self):
        jsonBlock = self.getJSON()
        return hashlib.sha256(jsonBlock.encode('utf-8'))
    
        
# Create an unique ID for the node
def GenerateUUID():
    UUID = 0
    
    for i in range(10):
        UUID = UUID*10 + (int)(random.random()*10)
    
    return UUID

# Create the API for the node
app = Flask(__name__)

@app.route("/last_block")
def lastBlock():
    return blockchain[0].getJSON()

@app.route("/chain")
def chain():
    x = {"blocks":[]}
    for block in blockchain:
        x["blocks"].append(block.getJSON())
        
    return json.dumps(x)


# Check usage
if(len(sys.argv)<2):
    print("Usage: "+sys.argv[0] + " [port] (node)")
    exit(0)

# Start the node
print("=== Starting Energia Node ===\n")
UUID = GenerateUUID()
print("Node UUID: "+str(UUID))
print("\n")

# If an other node is supplied  
if(len(sys.argv) >= 3):
    print("Connecting to network...")
    
    # Add the node to knowned node
    nodes += [sys.argv[2]]
    
    # Ask the last block
    r = requests.get("http://"+nodes[0]+"/chain")
    chain = json.loads(r.text)
    
    for block in chain["blocks"]:
        tmpBlock  = Block()
        tmpBlock.previousHash = block["previousHash"]
        tmpBlock.nonce = block["nonce"]
        
        for log in block["logList"]:
            tmpBlock.addLog(Log(log["nodeUUID"],log["power"]))
        
        blockchain.append(tmpBlock)
    

else:
    
    # Create the genesis block
    blockchain += [Block()]
    blockchain[0].previousHash = 987654321
    blockchain[0].addLog(Log(123456789,10))
    

app.run(host='localhost', port=sys.argv[1])


##print(block.getBlockHash().hexdigest())