import sqlite3
import sys
from flask import Flask, request
from flask import make_response

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

    nodeID = values["nodeID"]
    pubKey = values["pubKey"]

    conn.execute("INSERT INTO keys ('nodeID', 'pubKey') VALUES(?,?)", (nodeID, pubKey))
    
    print("Added node " + nodeID + " : " + pubKey)

    conn.close()
    
    return "OK"



@app.route('/get_key', methods=['GET'])
def getKey():
    conn = get_db_connection()

    nodeID = request.args.get("nodeID",type=str)

    print(nodeID)

    key = conn.execute("SELECT pubKey FROM keys WHERE nodeID=?",(nodeID,)).fetchone()[0]

    print("Node " + nodeID + " pubKey : " + key)

    conn.close()

    return app.make_response(key)


#############################################################
# Check usage
if(len(sys.argv)<2):
    print("Usage: "+sys.argv[0] + " [port]")
    exit(0)

# Start the node
print("=== Starting Energia \"\"\"Central\"\"\" Authority Node ===\n")
app.run(host='localhost', port=sys.argv[1], ssl_context=('PKI/ca.crt','PKI/ca.key'))