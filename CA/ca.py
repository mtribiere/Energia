import sqlite3
import sys
from flask import Flask

# Create the API for the node
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/add_key', methods=['POST'])
def addKey():
    conn = get_db_connection()

    values = request.get_json()

    conn.execute("""
        INSERT INTO keys VALUES 
        (values["nodeIP"],values["pubKey"])
    """)

    # Add the node to the list
    pubKey.append(values["pubKey"]) 
    
    print("Added node " + values[nodeID] + " : " +values["pubKey"])
    
    return "OK"



@app.route('/get_key', methods=['GET'])
def getKey():
    conn = get_db_connection()

    nodeID = request.args

    key = conn.execute('SELECT pubKey FROM keys WHERE nodeID=' + nodeID).fetchone()

    print("Node " + nodeID + " pubKey : "+values["pubKey"])
    
    return "OK"


#############################################################
# Check usage
if(len(sys.argv)<2):
    print("Usage: "+sys.argv[0] + " [port]")
    exit(0)

# Start the node
print("=== Starting Energia \"\"\"Central\"\"\" Authority Node ===\n")
app.run(host='localhost', port=sys.argv[1], ssl_context=('PKI/ca.crt','PKI/ca.key'))