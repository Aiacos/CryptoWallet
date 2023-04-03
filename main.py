from eth_account import Account
from web3 import Web3, HTTPProvider
#from numba import jit, cuda
from timeit import default_timer as timer
import re

import multiprocessing

pattern = '0x666' #0x324e2d42d7b65e5574787c331dfaa29d2dead666 sostituisci "123" con la stringa desiderata per l'indirizzo vanity

infura_endpoint='https://mainnet.infura.io/v3/972b4b8a084b434bba97948637e946be'
alchemy_endpoint='https://eth-mainnet.g.alchemy.com/v2/csmoa4n5DwucntIE0vZtb5NtOiJLC_ez'

connection = Web3(HTTPProvider(alchemy_endpoint))


def generateAccount():
    acct = Account.create()
    address = acct.address#.lower()

    private_key = acct.key.hex()

    return private_key, address

def checkBalanceETH(address):
    #safe_address = connection.to_checksum_address(address)
    #print("Safe: " + str(safe_address))
    wei_balance = connection.eth.get_balance(address)
    balance = connection.from_wei(wei_balance, 'ether')

    return balance

def generateVanity(pattern, private_key, public_key):
    if re.match(pattern, public_key):
        print(f"Vanity address found: {public_key}")
        print(f"Private key: {private_key}")

        return private_key, public_key

    return None

#@jit(target_backend='cuda')
def randomGenerateCUDA():
    while True:
        private_key, public_key = generateAccount()
        balance = checkBalanceETH(public_key)

        print(public_key)
        if balance > 0.0:
            print("Private key: " + str(private_key), " Balance: " + str(balance))

def randomGenerate():
    while True:
        private_key, public_key = generateAccount()
        balance = checkBalanceETH(public_key)

        #print(public_key)
        if balance > 0.0:
            print("Private key: " + str(private_key), " Balance: " + str(balance))



if __name__=="__main__":
    NUM_PROC = 8

    jobs = []

    for i in range(NUM_PROC):
        process = multiprocessing.Process(target=randomGenerate)
        jobs.append(process)

    for j in jobs:
        j.start()

    #start = timer()
    #randomGenerate()
    #print("without GPU:", timer() - start)

    #start = timer()
    #randomGenerateCUDA()
    #print("with GPU:", timer() - start)