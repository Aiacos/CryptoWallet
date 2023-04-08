from web3 import Web3, HTTPProvider
#from numba import jit, cuda, njit
from timeit import default_timer as timer

import multiprocessing
import threading
import schedule
from datetime import date
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

    try:
        balance = wallet.checkBalanceETH(connection, public_key)
    except:
        balance = 0.0

    return private_key, public_key, balance
def check_infura_address(limit):
    print('Start random generate with Infura')
    connection = Web3(HTTPProvider(wallet.infura_endpoint))

    address_with_balance_list = []
    for i in range(0, limit):
        private_key, public_key, balance = random_generate(connection)

        if balance > 0.0:
            keys = {'private_key': private_key, 'public_key': public_key, 'balance': balance}
            address_with_balance_list.append(keys)

    print('Infura generator done')

    data = []
    for line in address_with_balance_list:
        line_string = str(line)
        data.append(line_string)

    if data:
        try:
            send_email('Infura Report', "\n".join(data))
        except:
            print("\n".join(data))

    return address_with_balance_list

def check_alchemy_address(limit):
    print('Start random generate with Alchemy')
    connection = Web3(HTTPProvider(wallet.alchemy_endpoint))

    address_with_balance_list = []
    for i in range(0, limit):
        private_key, public_key, balance = random_generate(connection)

        if balance > 0.0:
            keys = {'private_key': private_key, 'public_key': public_key, 'balance': balance}
            address_with_balance_list.append(keys)

    print('Alchemy generator done')

    data = []
    for line in address_with_balance_list:
        line_string = str(line)
        data.append(line_string)

    if data:
        try:
            send_email('Infura Report', "\n".join(data))
        except:
            print("\n".join(data))

    return address_with_balance_list

def process_generate_infura(n_threads=8):
    schedule.every().day.at("00:01").do(generate_random_address_with_balance_infura, n_threads)

    while True:
        try:
            schedule.run_pending()
        except:
            print('Pass Infura')

        time.sleep(60)  # wait one minute

def process_generate_alchemy(n_threads=8):
    schedule.every().day.at("00:01").do(generate_random_address_with_balance_alchemy, n_threads)

    while True:
        try:
            if date.today().day == 1:
                schedule.run_pending()
        except:
            print('Pass Alchemy')

        time.sleep(60)  # wait one minute
def generate_random_address_with_balance_infura(n_threads=8):
    print('Start random generate with Infura')

    limit = int(wallet.INFURA_LIMIT / n_threads)

    thread_list = []
    for t in range(0, n_threads):
        infura_gen = threading.Thread(target=check_infura_address, args=(limit, ))
        thread_list.append(infura_gen)

    for t in thread_list:
        t.start()

def generate_random_address_with_balance_alchemy(n_threads=8):
    print('Start random generate with Alchemy')

    limit = int(wallet.INFURA_LIMIT / n_threads)

    thread_list = []
    for t in range(0, n_threads):
        alchemy_gen = threading.Thread(target=check_alchemy_address, args=(limit, ))
        thread_list.append(alchemy_gen)

    for t in thread_list:
        t.start()

def generate_vanity_eth(pattern):
    private_key, public_key = wallet.generateAccount()
    check = wallet.check_vanity(pattern, private_key, public_key)

    while not check:
        #start = timer()
        private_key, public_key = wallet.generateAccount()
        check = wallet.check_vanity(pattern, private_key, public_key)
        #print("Time:", timer() - start)
        #print(private_key, public_key)

    try:
        send_email('Infura Report', str('Found Private_Key: ', private_key, ' Public_Key: ', public_key))
    except:
        print('Found Private_Key: ', private_key, ' Public_Key: ', public_key)

    return check



def process_generate_vanity_eth(pattern, n_threads=12):
    print('Start Vanity ETH: ', pattern)

    thread_list = []
    for t in range(0, n_threads):
        vanity_gen = threading.Thread(target=generate_vanity_eth, args=(pattern, ))
        thread_list.append(vanity_gen)

    for t in thread_list:
        t.start()



if __name__=="__main__":
    #yagmail.register('username', 'password')

    jobs = []
    jobs.append(multiprocessing.Process(target=process_generate_infura, args=(8, ), name='Infura_ETH'))
    jobs.append(multiprocessing.Process(target=process_generate_alchemy, args=(8, ), name='Alchemy_ETH'))
    jobs.append(multiprocessing.Process(target=process_generate_vanity_eth, name='Vanity_ETH', args=(pattern.lower(), pow(2, 8)-1)))

    for j in jobs:
        j.start()
