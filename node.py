import hashlib
import json
import random
import sys
import threading
import time

from flask import Flask, request
import requests

from log import Log
from block import Block
from utils import *

# List of the blocks 
blockchain = []

# List of the nodes we know
nodes = []

# List of pending logs
pendingLogs = []
        

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

@app.route('/add_log', methods=['POST'])
def addLog():
    values = request.get_json()





#############################################################
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
            tmpBlock.addLog(Log(log["nodeUUID"],log["power"],log["logID"]))
        
        blockchain.append(tmpBlock)
    

else:
    
    # Create the genesis block
    blockchain += [Block()]
    blockchain[0].previousHash = 987654321
    blockchain[0].addLog(Log(123456789,10))
    

# Start the fake dataflow
threading.Thread(target=simulateDataFlow, daemon=True).start()
app.run(host='localhost', port=sys.argv[1])


##print(block.getBlockHash().hexdigest())