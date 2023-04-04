from web3 import Web3, HTTPProvider
#from numba import jit, cuda
from timeit import default_timer as timer

import multiprocessing
import threading
import wallet

pattern = '0x324e2d42d7b65e5574787c331dfaa29d2dead666'

#@jit(target_backend='cuda')
def random_generate(connection):
    private_key, public_key = wallet.generateAccount()
    balance = wallet.checkBalanceETH(connection, public_key)

    return private_key, public_key, balance
def check_infura_address():
    print('Start random generate with Infura')
    connection = Web3(HTTPProvider(wallet.infura_endpoint))

    address_with_balance_list = []
    for i in range(0, wallet.INFURA_LIMIT-1):
        private_key, public_key, balance = random_generate(connection)

        if balance > 0.0:
            data = {'private_key': private_key, 'public_key': public_key, 'balance': balance}
            address_with_balance_list.append(data)

    return data


def check_alchemy_address():
    print('Start random generate with Alchemy')
    connection = Web3(HTTPProvider(wallet.alchemy_endpoint))

    address_with_balance_list = []
    for i in range(0, wallet.ALCHEMY_LIMIT - 1):
        private_key, public_key, balance = random_generate(connection)

        if balance > 0.0:
            data = {'private_key': private_key, 'public_key': public_key, 'balance': balance}
            address_with_balance_list.append(data)

    return data

def generate_vanity_eth(pattern):
    print('Start Vanity ETH: ', pattern)

    private_key, public_key = wallet.generateAccount()
    check = wallet.check_vanity(pattern, private_key, public_key)

    while not check:
        private_key, public_key = wallet.generateAccount()
        check = wallet.check_vanity(pattern, private_key, public_key)

    print('Found Private_Key: ', private_key, ' Public_Key: ', public_key)






if __name__=="__main__":

    jobs = []
    jobs.append(multiprocessing.Process(target=check_infura_address, name='Infura_ETH'))
    jobs.append(multiprocessing.Process(target=check_alchemy_address, name='Alchemy_ETH'))
    jobs.append(multiprocessing.Process(target=generate_vanity_eth, name='Vanity_ETH', args=(pattern,)))

    for j in jobs:
        j.start()

    #start = timer()
    #randomGenerate()
    #print("without GPU:", timer() - start)

    #start = timer()
    #randomGenerateCUDA()
    #print("with GPU:", timer() - start)