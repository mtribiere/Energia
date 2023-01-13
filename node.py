import datetime
import hashlib
import json
import random
import sys
import threading
import time
import base64
import cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec

import copy


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

# Certs

with open(sys.argv[3], "rb") as key_file:
    privateKey = serialization.load_pem_private_key(
        key_file.read(),
        password=None,

    )

# NodeID
nodeID = sys.argv[4] 

# Create the API for the node
app = Flask(__name__)

@app.route("/last_block")
def lastBlock():
    return blockchain[0].getJSON()

@app.route("/chain")
def chain():
    global blockchain, pendingLogs
    x = {"blocks":[]}
    for block in blockchain:
        x["blocks"].append(block.toJSON())
        
    return json.dumps(x)

@app.route('/add_node', methods=['POST'])
def addNode():
    
    global blockchain, pendingLogs, nodes
    values = request.get_json()

    # Add the node to the list
    nodes.append(values["nodeIP"]) 
    
    print("Added node : "+values["nodeIP"])
    
    return "OK"

@app.route('/add_log', methods=['POST'])
def addLog():
    
    global blockchain, pendingLogs
    values = request.get_json()
    
    # Get the log we want to add
    toAdd = Log.fromJSON(values["log"])

    # If the log should be added
    if isLogPending(toAdd,pendingLogs) or toAdd.nodeUUID == UUID:
        return "Not added"
    
    # Verify signature 
    originNodeId = values["nodeID"]
    signature = values["signature"]

    # Get Public Key of Origin Node
    req = requests.get("https://get_key/"+originNodeId,verify=False)

    publicKey = x509.load_pem_x509_certificate(req.content).public_key() 

    try:
        publicKey.verify(signature, toAdd, ec.ECDSA(hashes.SHA256()))
    except cryptography.exceptions.InvalidSignature:
        return "Validation Error", 400
    else:

        # Add the log to the list
        pendingLogs.append(toAdd)
    
        print("Added pending log from "+str(toAdd.nodeUUID))
    
        # Broadcast the log to all known nodes
        for node in nodes:
        
            body = {"log":values["log"],"nodeID":values["nodeID"],"signature":values["signature"]}
            requests.post("http://"+node+"/add_log",json=body)
    
        # If the queue is full
        if len(pendingLogs) > 5:
            mineBlock()
    
        return "OK"

    return "Validation Error", 400

@app.route('/sync_chain', methods=['POST'])
def syncChain():
    global blockchain, pendingLogs
    
    values = request.get_json()
    
    # Get the proposed chain
    proposedChain = []
    for block in values["blocks"]:
        proposedChain.append(Block.fromJSON(block))
    
    # If we should not accept the chain
    if not(shouldSyncBlockChain(proposedChain,blockchain)):
        return "Not accepted chain"
    
    # Accept the chain
    blockchain = proposedChain
    pendingLogs = []
    
    print(" [Chain synced by remote] ")
    
    return "OK"

@app.route("/mine")
def mine():
    
    mineBlock()

    return "OK"


def mineBlock():
    global blockchain, pendingLogs
    
    # Create a new block
    newBlock = Block()
    newBlock.previousHash = blockchain[len(blockchain)-1].getBlockHash()
    
    for log in pendingLogs:
        newBlock.addLog(log)

    # Mine it
    newBlock.mine()
    blockchain.append(newBlock)
    pendingLogs = []

    # Broadcast the new chain
    body = {"blocks":[]}
    for block in blockchain:
        body["blocks"].append(block.toJSON())
    
    for node in nodes:
        requests.post("http://"+node+"/sync_chain",json=body)
    


# Simulate a dataflow
def simulateDataFlow():
    while True:
        time.sleep(random.randint(0,10))
        
        # Broadcast the log to all known nodes
        newLog = Log(UUID,random.randint(1,100),GenerateUUID())
        for node in nodes:
            signature = privateKey.sign(json.dumps(newLog.toJSON()).encode('utf-8'),ec.ECDSA(hashes.SHA256()))
            body = {"log":newLog.toJSON(),"nodeID":nodeID,"signature":signature}
            requests.post("http://"+node+"/add_log",json=body)
        
        del newLog

#############################################################
# Check usage
if(len(sys.argv)<2):
    print("Usage: "+sys.argv[0] + " [port]")
    exit(0)

# Start the node
print("=== Starting Energia Node ===\n")
UUID = GenerateUUID()
print("Node UUID: "+str(UUID))
print("\n")

    
# Create the genesis block
blockchain += [Block()]
blockchain[0].previousHash = 987654321
blockchain[0].addLog(Log(123456789,10))
    

# Start the fake dataflow
threading.Thread(target=simulateDataFlow, daemon=True).start()
app.run(host='localhost', port=sys.argv[1])
