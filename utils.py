# Simulate the data flow 
import random
import time

# Simulate a dataflow
def simulateDataFlow():
    time.sleep(5)
        
# Create an unique ID for the node
def GenerateUUID():
    UUID = 0
    
    for i in range(10):
        UUID = UUID*10 + (int)(random.random()*10)
    
    return UUID

# Return true if the log is already pending
def isLogPending(log,pendingLogs):
    for tmpLog in pendingLogs:
        if tmpLog.logID == log.logID:
            return True
    
    return False

# Should Sync with a remote blockchain (Consensus)
def shouldSyncBlockChain(proposedChain,currentChain):
    
    if len(proposedChain) > len(currentChain):
        return True
    
    return False