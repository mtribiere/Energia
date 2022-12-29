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