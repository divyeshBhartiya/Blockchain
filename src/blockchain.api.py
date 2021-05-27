# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:49:54 2021

@author: Divyesh Bhartiya
"""

from flask import Flask, jsonify
from blockchain import Blockchain

# Blockchain Web API
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
blockchain = Blockchain()

# Mining the Blockchain
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'message' : 'Congratulations, you just mined a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    
    return jsonify(response), 200

# Fetching the Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200


app.run(host = '0.0.0.0', port = 5000)