from eth_account import Account
from web3 import Web3, HTTPProvider
import re


infura_endpoint = 'https://mainnet.infura.io/v3/972b4b8a084b434bba97948637e946be'
alchemy_endpoint = 'https://eth-mainnet.g.alchemy.com/v2/csmoa4n5DwucntIE0vZtb5NtOiJLC_ez'

INFURA_LIMIT = 100000
ALCHEMY_LIMIT = 300000000000


def generateAccount():
    acct = Account.create()
    address = acct.address#.lower()

    private_key = acct.key.hex()

    return private_key, address

def generatePrivateKey():
    acct = Account.create()
    #address = acct.address#.lower()

    private_key = acct.key.hex()

    return str(private_key)

def generatePublicKeyFromPrivate(private_key):
    acct = Account.from_key(private_key)
    address = acct.address#.lower()

    return address

def checkBalanceETH(connection, address, coin='ether'):
    #safe_address = connection.to_checksum_address(address)
    #print("Safe: " + str(safe_address))
    wei_balance = connection.eth.get_balance(address)
    balance = connection.from_wei(wei_balance, coin)

    return balance

def check_vanity(pattern, private_key, public_key, regex=False):
    if regex:
        if re.match(pattern, public_key):
            return private_key, public_key
        else:
            return None
    else:
        if pattern == public_key:
            return private_key, public_key
        else:
            return None

    return None