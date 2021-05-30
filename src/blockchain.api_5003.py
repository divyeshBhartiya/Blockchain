# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:49:54 2021

@author: Divyesh Bhartiya
"""

from uuid import uuid4
from flask import Flask, jsonify, request
from heercoin.heer import Heer

# Blockchain Web API
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
heer = Heer()

# Creating an address for the node on Port 5003
node_address = str(uuid4()).replace('-','')

# Mining the Blockchain
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = heer.blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    
    proof = heer.blockchain.proof_of_work(previous_proof)
    previous_hash = heer.blockchain.hash(previous_block)
    heer.add_transaction(sender=node_address, receiver='Mommy', amount=10)
    
    block = heer.blockchain.create_block(proof, previous_hash)
    
    response = {'message' : 'Congratulations, you just mined a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions' : block['transactions']}
    
    return jsonify(response), 200

# Fetching the Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : heer.blockchain.chain,
                'length': len(heer.blockchain.chain)}
    
    return jsonify(response), 200

# Checking the validity of Blockchain
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = heer.blockchain.is_valid_chain(heer.blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Something went HayWire. The Blockchain is not valid.'}
        
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing!!', 400
    index = heer.add_transaction(json['sender'], json['receiver'], json['amount'])

    response = {'message' : f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node', 400
    for node in nodes:
        heer.add_node(node)
    response = {'message' : 'All the nodes are now connected. The Heercoin Blockchain now contains following nodes:',
                'total_nodes' : list(heer.blockchain.nodes)}
    return jsonify(response), 201 

# Replacing the chain with longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_replaced = heer.replace_chain()
    if is_replaced:
        response = {'message': 'The node had different chain, so the chain was replaced with longest and valid one.',
                    'new_chain': heer.blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the longest one. No need for replacement.',
                    'actual_chain': heer.blockchain.chain}
        
    return jsonify(response), 200

app.run(host = '127.0.0.1', port = 5003)