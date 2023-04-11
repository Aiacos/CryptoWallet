from web3 import Web3, HTTPProvider
# from numba import jit, cuda, njit
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


class RandomGenerateAddress:
    def __init__(self, connection):
        self.connection = connection
        self.valid_address_list = []
        self.vanity_address_list = []

    def generate_account(self, mode='mnemonic'):
        private_key, public_key, mnemonic = wallet.generateAccount(mode)

        return private_key, public_key, mnemonic

    def get_balance(self, address):
        balance = wallet.checkBalanceETH(self.connection, address)

        return balance

    def generate_and_check_balance(self, mode):
        private_key, public_key, mnemonic = self.generate_account(mode)
        balance = self.get_balance(public_key)

        return {'private_key': private_key, 'public_key': public_key, 'balance': balance, 'mnemonic: ': mnemonic}

    def check_vanity(self, vanity_address, public_key, regex=True):
        return wallet.check_vanity(vanity_address, public_key, regex)

    def generate_address(self, iteration_limit, gen_mode='mnemonic', vanity_address=None, regex=True, check_balance=True, console_print=True, console_print_empty=False):
        if iteration_limit == 0:
            while True:
                key = self.generate_and_check_balance(gen_mode)
                if console_print_empty: print(key)

                if vanity_address:
                    if self.check_vanity(vanity_address, key['public_key'], regex):
                        self.vanity_address_list.append(key)
                        if console_print: print(key)

                if check_balance and key['balance'] > 0.0:
                    self.valid_address_list.append(key)
                    if console_print: print(key)
        else:
            for i in range(0, iteration_limit):
                key = self.generate_and_check_balance(gen_mode)
                if console_print_empty: print(key)

                if vanity_address:
                    if self.check_vanity(vanity_address, key['public_key'], regex):
                        self.vanity_address_list.append(key)
                        if console_print: print(key)

                if check_balance and key['balance'] > 0.0:
                    self.valid_address_list.append(key)
                    if console_print: print(key)

def check_infura_address(limit):
    connection = Web3(HTTPProvider(wallet.infura_endpoint))

    infura_instance = RandomGenerateAddress(connection)
    infura_instance.generate_address(limit)

def check_alchemy_address(limit=0):
    connection = Web3(HTTPProvider(wallet.alchemy_endpoint))

    infura_instance = RandomGenerateAddress(connection)
    infura_instance.generate_address(limit)




def process_generate_infura(n_threads=8):
    schedule.every().day.at("00:01").do(generate_random_address_with_balance_infura, n_threads)

    while True:
        try:
            # schedule.run_pending()
            schedule.run_all()
        except:
            print('Pass Infura')

        time.sleep(60)  # wait one minute


def process_generate_alchemy(n_threads=8):
    schedule.every().day.at("10:13").do(generate_random_address_with_balance_alchemy, n_threads)

    while True:
        try:
            if date.today().day == 11:
                schedule.run_pending()
                # schedule.run_all()
        except:
            print('Pass Alchemy')

        time.sleep(60)  # wait one minute


def generate_random_address_with_balance_infura(n_threads=8):
    print('Start random generate with Infura')

    limit = int(wallet.INFURA_LIMIT / n_threads)

    thread_list = []
    for t in range(0, n_threads):
        infura_gen = threading.Thread(target=check_infura_address, args=(limit,))
        thread_list.append(infura_gen)

    for t in thread_list:
        t.start()


def generate_random_address_with_balance_alchemy(n_threads=8):
    print('Start random generate with Alchemy')

    limit = int(wallet.ALCHEMY_LIMIT / n_threads)

    thread_list = []
    for t in range(0, n_threads):
        alchemy_gen = threading.Thread(target=check_alchemy_address, args=(0,))
        thread_list.append(alchemy_gen)

    for t in thread_list:
        t.start()


def generate_vanity_eth(pattern):
    private_key, public_key = wallet.generateAccount()
    check = wallet.check_vanity(pattern, private_key, public_key)

    while not check:
        # start = timer()
        private_key, public_key = wallet.generateAccount()
        check = wallet.check_vanity(pattern, private_key, public_key)
        # print("Time:", timer() - start)
        # print(private_key, public_key)

    try:
        send_email('Infura Report', str('Found Private_Key: ', private_key, ' Public_Key: ', public_key))
    except:
        print('Found Private_Key: ', private_key, ' Public_Key: ', public_key)

    return check


def process_generate_vanity_eth(pattern, n_threads=12):
    print('Start Vanity ETH: ', pattern)

    thread_list = []
    for t in range(0, n_threads):
        vanity_gen = threading.Thread(target=generate_vanity_eth, args=(pattern,))
        thread_list.append(vanity_gen)

    for t in thread_list:
        t.start()


if __name__ == "__main__":
    # yagmail.register('username', 'password')

    jobs = []
    # jobs.append(multiprocessing.Process(target=process_generate_infura, args=(8, ), name='Infura_ETH'))
    # jobs.append(multiprocessing.Process(target=process_generate_alchemy, args=(8, ), name='Alchemy_ETH'))
    # jobs.append(multiprocessing.Process(target=process_generate_vanity_eth, name='Vanity_ETH', args=(pattern.lower(), pow(2, 8)-1)))

    for j in jobs:
        j.start()

    connection = Web3(HTTPProvider(wallet.alchemy_endpoint))
    print(connection.isConnected())
    while True:
        private_key, public_key, balance, mnemonic = random_generate(connection)

        # print(mnemonic, balance)
        if balance and balance > 0.0:
            keys = {'private_key': private_key, 'public_key': public_key, 'balance': balance, 'Mnemonic: ': mnemonic}
            print(keys)
