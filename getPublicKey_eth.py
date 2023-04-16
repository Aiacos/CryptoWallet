import web3
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import ALLOWED_TRANSACTION_KEYS
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict

infura_endpoint = 'https://mainnet.infura.io/v3/972b4b8a084b434bba97948637e946be'
transaction = 0xe606a67d46b6663b472197579f3c3e2bca657b946a0f5ec1b17b00978b00bfc5

w3 = web3.Web3(web3.HTTPProvider(infura_endpoint))
tx = w3.eth.getTransaction(transaction)
#print('tx.hash: ', tx.hash)

s = w3.eth.account._keys.Signature(vrs=(
    to_standard_v(extract_chain_id(tx.v)[1]),
    w3.toInt(tx.r),
    w3.toInt(tx.s)
))

#print("signature: ", s)

tt = {k: tx[k] for k in ALLOWED_TRANSACTION_KEYS - {'chainId', 'data'}}
tt['data'] = tx.input
tt['chainId'] = extract_chain_id(tx.v)[0]

print("Transaction: ", tt)

ut = serializable_unsigned_transaction_from_dict(tt)

# print("Hash:: ", ut.hash())
print("Public kye: ", s.recover_public_key_from_msg_hash(ut.hash()))

check_address = s.recover_public_key_from_msg_hash(ut.hash()).to_checksum_address()
print('Check Address: ', check_address)


from eth_keys.datatypes import Signature
def pub_key_from_tx_eth(txid, chain='ETH'):
    """Obtain the public key from an Ethereum transaction
    """
    w3test = web3.Web3(web3.HTTPProvider(infura_endpoint))
    transaction = w3test.eth.get_transaction(txid)
    vrs = (to_standard_v(transaction['v']),
           int.from_bytes(transaction['r'], "big"),
           int.from_bytes(transaction['s'], "big"))
    signature = Signature(vrs=vrs)
    tx_dict = {'nonce': transaction.nonce,
               'gasPrice': transaction.gasPrice,
               'gas': transaction.gas,
               'to': transaction.to,
               'value': transaction.value
    }
    if chain == "ETH":
        tx_dict['chainId'] = "0x01"
    elif chain == "tETH":
        tx_dict['chainId'] = "0x03"
    if 'input' in transaction:
        tx_dict['data'] = transaction['input']
    serialized_tx = serializable_unsigned_transaction_from_dict(tx_dict)
    rec_pub = signature.recover_public_key_from_msg_hash(serialized_tx.hash())
    if rec_pub.to_checksum_address() != transaction['from']:
        print('Wrong:', rec_pub.to_checksum_address(), ' From: ', transaction['from'])
        raise ValueError("Unable to obtain public key from transaction: " +
                         f"{txid}")
    return(rec_pub)

print(pub_key_from_tx_eth(transaction))
