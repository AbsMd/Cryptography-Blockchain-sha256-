import hashlib
import json
from time import time
from sha import *
import random

# function to add to JSON
def w_json(data, filename='file.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

class Blockchain(object):
    def __init__(self):
        with open('file.json') as json_file:
            data = json.load(json_file)
        self.chain = data
        self.current_transactions = []
        self.block={}
        # Create the genesis block
        #self.makeBlock(previous_hash=1, proof=100)

    def makeBlock(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        """

        block = {
            'index': self.chain[-1]['index'] +1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []


        self.chain.append(block)
        return block

    def newTrans(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        returns the index of the block added
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def proofOfWork(self, last_proof):
        p = 11
        g = 2
        r = random.randint(0,p-1)
        h = (g**r)%(p)
        b = random.randint(0,1)
        s = (r+ b*last_proof)%(p-1)
        y = (g**last_proof)%(p)
        proof = self.verifyTrans(y, s, h, b)
        return proof

    @staticmethod
    def verifyTrans(y, s, h, b):   
        """
        
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        p = 11
        g = 2
        if ((g**s)%(p)) == (h*(y**b)%p):
            return ((g**s)%(p))**y
                    
    def mineBlock(self):
        # We run the proof of work algorithm to get the next proof...
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proofOfWork(last_proof)

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        self.block = blockchain.makeBlock(proof, previous_hash)

    @staticmethod
    def hash(block):##need to be modified
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hasher(block_string)

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]


        
if __name__ == '__main__':
    #Instantiate a BlockChain
    blockchain = Blockchain()
    c=1;
    print("Blockchain is created." )
    while(c):

        print("Choose from the following options:")
        print("1: Make a Transaction.")
        print("2: View BlockChain")
        print("3: View Transactions for a User")
        print("4: Exit")
        x=input()

        if(x=="1"):
            print("processing...")
            print("Enter Sender name:")
            sender=input()
            print("Enter Receiver name:")
            receiver=input()
            print("Enter Amount:")
            amount=input()
            index = blockchain.newTrans(sender, receiver, amount)
            print("Transaction will be added to Block:" + str(blockchain.chain[-1]['index'] +1))
            blockchain.mineBlock()

        elif(x=="2"):
            #view blocks\
            print("processing...")

            print(json.dumps(blockchain.chain, indent = 4))

        elif(x=="3"):
            print("processing...")
            #transactions for a user
            print("Enter User:")
            user=input()
            Balance=0
            for block in blockchain.chain:
                # print(type(block["transactions"]))
                if(block['transactions'][0]['sender'] == user ):
                    Balance= Balance-int(block["transactions"][0]["amount"])
                    print(json.dumps(block["transactions"], indent = 4))
                elif (block['transactions'][0]['recipient'] == user):
                    Balance = Balance +int( block["transactions"][0]["amount"])
                    print(json.dumps(block["transactions"], indent=4))
            print("\n\nBalance : " + str(Balance)+ "\n")

        else:
            c=0
            with open('file.json') as json_file:
                data = json.load(json_file)
                data.append(blockchain.block)
            w_json(blockchain.chain)
            print("exiting....")