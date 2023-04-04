from web3 import Web3, HTTPProvider
#from numba import jit, cuda
from timeit import default_timer as timer

import multiprocessing
import threading
import schedule
import time
import yagmail
import wallet

pattern = '0x324e2d42d7b65e5574787c331dfaa29d2dead666'

def send_email(subject, body):
    email = "uni.lorenzo.a@gmail.com"

    yag = yagmail.SMTP(email)
    yag.send(
        to=email,
        subject=subject,
        contents=body
    )
#@jit(target_backend='cuda')
def random_generate(connection):
    private_key, public_key = wallet.generateAccount()
    balance = wallet.checkBalanceETH(connection, public_key)

    return private_key, public_key, balance
def check_infura_address():
    print('Start random generate with Infura')
    connection = Web3(HTTPProvider(wallet.infura_endpoint))

    address_with_balance_list = []
    for i in range(0, 11-1):
        private_key, public_key, balance = random_generate(connection)

        if balance > 0.0:
            keys = {'private_key': private_key, 'public_key': public_key, 'balance': balance}
            address_with_balance_list.append(keys)

    print('Infura generator done')
    #global data
    #data.append(address_with_balance_list)

    data = []
    for line in address_with_balance_list:
        line_string = str(line)
        data.append(line_string)
    data = {'private_key': 'test pkey', 'public_key': 'test addres', 'balance': 12} #Todo: Delete this line
    if data:
        send_email('Infura Report', data)

    return address_with_balance_list

def check_alchemy_address():
    print('Start random generate with Alchemy')
    connection = Web3(HTTPProvider(wallet.alchemy_endpoint))

    address_with_balance_list = []
    for i in range(0, wallet.ALCHEMY_LIMIT - 1):
        private_key, public_key, balance = random_generate(connection)

        if balance > 0.0:
            keys = {'private_key': private_key, 'public_key': public_key, 'balance': balance}
            address_with_balance_list.append(keys)

    print('Alchemy generator done')
    global data
    data.append(address_with_balance_list)
    return address_with_balance_list

def generate_random_address_with_balance_infura():
    schedule.every().day.at("00:01").do(check_infura_address)

    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute

def generate_random_address_with_balance_alchemy():
    schedule.every().month.at("00:01").do(check_alchemy_address)

    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute

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
    jobs.append(multiprocessing.Process(target=generate_random_address_with_balance_infura, name='Infura_ETH'))
    #jobs.append(multiprocessing.Process(target=check_alchemy_address, name='Alchemy_ETH'))
    #jobs.append(multiprocessing.Process(target=generate_vanity_eth, name='Vanity_ETH', args=(pattern,)))

    for j in jobs:
        j.start()

    #start = timer()
    #randomGenerate()
    #print("without GPU:", timer() - start)

    #start = timer()
    #randomGenerateCUDA()
    #print("with GPU:", timer() - start)

    # Multithread
    #infura_thread = threading.Thread(target=check_infura_address)
    #alchemy_thread = threading.Thread(target=check_alchemy_address)

    # starting thread 1
    #infura_thread.start()
    # starting thread 2
    #alchemy_thread.start()

    #infura_thread.join()
    #alchemy_thread.join()