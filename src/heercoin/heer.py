# -*- coding: utf-8 -*-
"""
Created on Fri May 28 23:35:54 2021

@author: Divyesh Bhartiya
"""
from blockchain import Blockchain
import requests
from urllib.parse import urlparse


class Heer:
    # Building the Heer Cryptocurrency
    blockchain = Blockchain()

    def add_transaction(self, sender, receiver, amount):
        self.blockchain.transactions.append({'sender' : sender,
                                'receiver' : receiver,
                                'amount' : amount})

        previous_block = self.blockchain.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.blockchain.nodes.add(parsed_url.netloc) 
        # netloc would provide the host and port of the server which is part of blockchain's distributed network.

    def replace_chain(self):
        # This would replace chain with the longest one in the network as per the consensus between the servers.
        blockchain_network = self.blockchain.nodes
        longest_chain = None # it would have the longest chain after scanning the chains across network or nodes
        max_length = len(self.blockchain.chain) # we assume that as of now the chain in the current node has the max_length

        for node in blockchain_network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                json_response = response.json()
                length = json_response['length']
                chain = json_response['chain']

                if length > max_length and self.blockchain.is_valid_chain(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.blockchain.chain = longest_chain
            return True
        return False