import hashlib
import json
import logging
import sys
import time

import utils

MINING_DIFFICULTY = 6

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class BlockChain(object):

    def __init__(self):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash({}))

    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(self, sender_blockchain_address,
                        recipient_blockchain_address, value):
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address': sender_blockchain_address,
            'recipient_blockchain_address': recipient_blockchain_address,
            'value': float(value)
        })
        self.transaction_pool.append(transaction)
        return True

    def valid_proof(self, transactions, previous_hash, nonce,
                    difficulty=MINING_DIFFICULTY):
        guess_block = utils.sorted_dict_by_key({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        guess_hash = self.hash(guess_block)
        return guess_hash[:difficulty] == '0' * difficulty

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce


def pprint(chains):
    for i, chain in enumerate(chains):
        print(f'{"=" * 25} Chain {i} {"=" * 25}')
        for k, v in chain.items():
            if k == 'transactions':
                print(k)
                for d in v:
                    print(f'{"-" * 40}')
                    for kk, vv in d.items():
                        print(f' {kk:30}{vv}')
            else:
                print(f'{k:15}{v}')
    print(f'{"*" * 25}')


if __name__ == '__main__':
    time_list = []
    for j in range(1):
        start_time = time.process_time()

        block_chain = BlockChain()
        # pprint(block_chain.chain)

        block_chain.add_transaction('A', 'B', 1.0)
        previous_hash = block_chain.hash(block_chain.chain[-1])
        nonce = block_chain.proof_of_work()
        block_chain.create_block(nonce, previous_hash)
        # pprint(block_chain.chain)

        block_chain.add_transaction('C', 'D', 2.0)
        block_chain.add_transaction('X', 'Y', 3.0)
        previous_hash = block_chain.hash(block_chain.chain[-1])
        nonce = block_chain.proof_of_work()
        block_chain.create_block(nonce, previous_hash)
        # pprint(block_chain.chain)

        end_time = time.process_time()
        elapsed_time = end_time - start_time
        time_list.append(elapsed_time)
    # print(f'{"/"*10} {elapsed_time}sec {"/"*10}')
    [print(aa) for aa in time_list]