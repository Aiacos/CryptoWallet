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
from tqdm import tqdm

pattern = '0x324e2D42D7B65E5574787C331DfaA29d2Dead666'


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

    def generate_and_check_balance(self, mode, check_balance=False):
        private_key, public_key, mnemonic = self.generate_account(mode)
        if check_balance:
            balance = self.get_balance(str(public_key))
        else:
            balance = None

        return {'private_key': private_key, 'public_key': public_key, 'balance': balance, 'mnemonic: ': mnemonic}

    def check_vanity(self, vanity_address, public_key, regex=True):
        return wallet.check_vanity(vanity_address, public_key, regex)

    def generate_address(self, iteration_limit, gen_mode='mnemonic', vanity_address=None, regex=True, check_balance=True, console_print=True, console_print_empty=False):
        if iteration_limit == 0:
            while True:
                key = self.generate_and_check_balance(gen_mode, check_balance)
                if console_print_empty: print(key, end="\r", flush=True)

                if vanity_address:
                    if self.check_vanity(vanity_address, key['public_key'], regex):
                        self.vanity_address_list.append(key)
                        if console_print: print(key)

                if check_balance and key['balance'] == None: break
                if check_balance and key['balance'] > 0.0:
                    self.valid_address_list.append(key)
                    if console_print: print(key)
        else:
            for i in tqdm(range(0, iteration_limit)):
                key = self.generate_and_check_balance(gen_mode, check_balance)
                if console_print_empty: print(key, end="\r", flush=True)

                if vanity_address:
                    if self.check_vanity(vanity_address, key['public_key'], regex):
                        self.vanity_address_list.append(key)
                        if console_print: print(key)

                if check_balance and key['balance'] == None: break
                if check_balance and key['balance'] > 0.0:
                    self.valid_address_list.append(key)
                    if console_print: print(key)

def check_infura_address(limit):
    connection = Web3(HTTPProvider(wallet.infura_endpoint))

    infura_instance = RandomGenerateAddress(connection)
    infura_instance.generate_address(limit - 1)

def check_alchemy_address(limit=0):
    connection = Web3(HTTPProvider(wallet.alchemy_endpoint))

    infura_instance = RandomGenerateAddress(connection)
    infura_instance.generate_address(limit - 1)




def scheduler_generate_infura(n_threads=8):
    schedule.every().day.at("00:01").do(generate_random_address_infura, n_threads)

    while True:
        try:
            schedule.run_pending()
            #schedule.run_all()
        except:
            print('Pass Infura')

        time.sleep(60)  # wait one minute


def scheduler_generate_alchemy(n_threads=8):
    schedule.every().day.at("00:01").do(generate_random_address_alchemy, n_threads)

    while True:
        try:
            if date.today().day == 1:
                schedule.run_pending()
                # schedule.run_all()
        except:
            print('Pass Alchemy')

        time.sleep(60)  # wait one minute


def generate_random_address_infura(n_threads=8):
    print('Start random generate with Infura')

    limit = int(wallet.INFURA_LIMIT / n_threads)

    thread_list = []
    for t in range(0, n_threads):
        infura_gen = threading.Thread(target=check_infura_address, args=(limit,))
        thread_list.append(infura_gen)

    for t in thread_list:
        t.start()


def generate_random_address_alchemy(n_threads=8):
    print('Start random generate with Alchemy')

    limit = int(wallet.ALCHEMY_LIMIT / n_threads)

    thread_list = []
    for t in range(0, n_threads):
        alchemy_gen = threading.Thread(target=check_alchemy_address, args=(0,))
        thread_list.append(alchemy_gen)

    for t in thread_list:
        t.start()


def generate_vanity_eth(pattern):
    connection = Web3(HTTPProvider(wallet.alchemy_endpoint))

    infura_instance = RandomGenerateAddress(connection)
    infura_instance.generate_address(0, gen_mode='fast', vanity_address=pattern, regex=False, check_balance=False, console_print=True, console_print_empty=False)


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
    jobs.append(multiprocessing.Process(target=scheduler_generate_infura, args=(1, ), name='Infura_ETH'))
    #jobs.append(multiprocessing.Process(target=scheduler_generate_alchemy, args=(8, ), name='Alchemy_ETH'))
    #jobs.append(multiprocessing.Process(target=process_generate_vanity_eth, name='Vanity_ETH', args=(pattern, 256)))

    for j in jobs:
        j.start()
