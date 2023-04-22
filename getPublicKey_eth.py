import web3
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import ALLOWED_TRANSACTION_KEYS
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from eth_keys.datatypes import Signature
import requests


infura_endpoint = 'https://mainnet.infura.io/v3/972b4b8a084b434bba97948637e946be'
infura_API = 'PY49HDD1DPEEX9PE6PUZ56VP38493ARBGM'

w3 = web3.Web3(web3.HTTPProvider(infura_endpoint))

address = '0x324e2D42D7B65E5574787C331DfaA29d2Dead666'
transaction = 0xe606a67d46b6663b472197579f3c3e2bca657b946a0f5ec1b17b00978b00bfc5
url = 'https://api.etherscan.io/api?module=account&action=txlist&address=' + address + '&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey=' + infura_API
# https://api.etherscan.io/api?module=account&action=txlist&address=0x324e2D42D7B65E5574787C331DfaA29d2Dead666&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey=PY49HDD1DPEEX9PE6PUZ56VP38493ARBGM
d = {"status":"1","message":"OK","result":[
    {"blockNumber":"15695286","timeStamp":"1665134363","hash":"0xbac992db6a9660f6ebcdd483c244dfa1948ab8b9a63184eb3015e00258c5d1af","nonce":"5","blockHash":"0xaeedcd887a82bf916ca5194dd3c7f7a625c6b28d006a1363ea1cb0cc4f126537","transactionIndex":"244","from":"0xcac191ab410b5c225779cec01163ab7d717d3666","to":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","value":"6882485956269079","gas":"21000","gasPrice":"6362913733","isError":"0","txreceipt_status":"1","input":"0x","contractAddress":"","cumulativeGasUsed":"17407223","gasUsed":"21000","confirmations":"1383852","methodId":"0x","functionName":""},
    {"blockNumber":"15695524","timeStamp":"1665137219","hash":"0x30f81ebffb890ab9aea57ea07e63e25018028ca836cd98812b107e6f23ac872c","nonce":"0","blockHash":"0xc8e619708308a4610d87d4b2dec84417f963143f3f626ea13a15ae060c4b7467","transactionIndex":"55","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0x3dd49f67e9d5bc4c5e6634b3f70bfd9dc1b6bd74","value":"0","gas":"69129","gasPrice":"6476896228","isError":"0","txreceipt_status":"1","input":"0x095ea7b30000000000000000000000007a250d5630b4cf539739df2c5dacb4c659f2488d0000000000000000000000000000000000000000000000055de6a779bbac0000","contractAddress":"","cumulativeGasUsed":"4169909","gasUsed":"46086","confirmations":"1383614","methodId":"0x095ea7b3","functionName":"approve(address _spender, uint256 _value)"},
    {"blockNumber":"15695528","timeStamp":"1665137267","hash":"0x6f36cc7156734c6c2789355cdaa15ae373e86a997d2d1c19f2bbbc8174fde7df","nonce":"1","blockHash":"0x696612330029c64f32cc267d2e068677e085517ef4eb6f9e75e27917d5e52f82","transactionIndex":"140","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0x7a250d5630b4cf539739df2c5dacb4c659f2488d","value":"0","gas":"249427","gasPrice":"6018090283","isError":"0","txreceipt_status":"1","input":"0x02751cec0000000000000000000000003845badade8e6dff049820680d1f14bd3903a5d0000000000000000000000000000000000000000000000000038886c3ed097e00000000000000000000000000000000000000000000000000ccb457287ec0e493000000000000000000000000000000000000000000000000002092bd4f0229a2000000000000000000000000324e2d42d7b65e5574787c331dfaa29d2dead6660000000000000000000000000000000000000000000000000000000063400163","contractAddress":"","cumulativeGasUsed":"14186897","gasUsed":"164593","confirmations":"1383610","methodId":"0x02751cec","functionName":"removeLiquidityETH(address token, uint256 liquidity, uint256 amountTokenMin, uint256 amountETHMin, address to, uint256 deadline)"},
    {"blockNumber":"15695541","timeStamp":"1665137423","hash":"0x8b554d476726dfcea5fbbf7917b1a33e3e9222d80f6f930b08e39e5f7f268432","nonce":"2","blockHash":"0xa4093c95534e10d628cf91205e3869ca9ad80eff98f8a8e26229f72909028f8e","transactionIndex":"77","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0xab05cf7c6c3a288cd36326e4f7b8600e7268e344","value":"0","gas":"46591","gasPrice":"6228399044","isError":"0","txreceipt_status":"1","input":"0x095ea7b3000000000000000000000000eef417e1d5cc832e619ae18d2f140de2999dd4fbffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","contractAddress":"","cumulativeGasUsed":"7985256","gasUsed":"46591","confirmations":"1383597","methodId":"0x095ea7b3","functionName":"approve(address _spender, uint256 _value)"},
    {"blockNumber":"15695545","timeStamp":"1665137471","hash":"0x08d22e406efdc71a9541511b547faddd024373fb9b53999b1ba828475e847015","nonce":"3","blockHash":"0x86a92d7feaff203fcf1a75c9e14f6e0a48008832f6308dffb4b1496c9df42d24","transactionIndex":"77","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0xeef417e1d5cc832e619ae18d2f140de2999dd4fb","value":"0","gas":"274452","gasPrice":"6358923669","isError":"0","txreceipt_status":"1","input":"0x357a0333000000000000000000000000ab05cf7c6c3a288cd36326e4f7b8600e7268e344000000000000000000000000000000000000000000000006c9eecbbdfc9124cc","contractAddress":"","cumulativeGasUsed":"7590594","gasUsed":"256917","confirmations":"1383593","methodId":"0x357a0333","functionName":"initWithdrawal(address poolToken, uint256 poolTokenAmount)"},
    {"blockNumber":"15695566","timeStamp":"1665137723","hash":"0x385d77cdf343be84ece8330883d7cac65664f9e6da53363585f7d65aa542d72a","nonce":"4","blockHash":"0x2166a661481568a14d318b5b1a93981f8e1e1c4fa82793722ac96a435e1b034b","transactionIndex":"150","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0x49bdfdf9d103610413be6ecb25c194ce1d803bd3","value":"0","gas":"46591","gasPrice":"6445865253","isError":"0","txreceipt_status":"1","input":"0x095ea7b3000000000000000000000000eef417e1d5cc832e619ae18d2f140de2999dd4fbffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","contractAddress":"","cumulativeGasUsed":"12276031","gasUsed":"46591","confirmations":"1383572","methodId":"0x095ea7b3","functionName":"approve(address _spender, uint256 _value)"},
    {"blockNumber":"15695568","timeStamp":"1665137747","hash":"0x20a411fd04c7ca0f55837c4dff9b1321f15811cb8aa104a4249a67104778c255","nonce":"5","blockHash":"0x637b04ad99c9f5cf67ab686f0e9552d82fc05f6ef2b3ce5ca043910460cea1f0","transactionIndex":"28","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0xeef417e1d5cc832e619ae18d2f140de2999dd4fb","value":"0","gas":"259500","gasPrice":"6224608584","isError":"0","txreceipt_status":"1","input":"0x357a033300000000000000000000000049bdfdf9d103610413be6ecb25c194ce1d803bd3000000000000000000000000000000000000000000000015429740242cb20000","contractAddress":"","cumulativeGasUsed":"3248951","gasUsed":"242924","confirmations":"1383570","methodId":"0x357a0333","functionName":"initWithdrawal(address poolToken, uint256 poolTokenAmount)"},
    {"blockNumber":"15695583","timeStamp":"1665137927","hash":"0x5c383ac8cafdcdd1e4ec8138880de4125e799849b4a04cdb30d85ddd1e5655ff","nonce":"6","blockHash":"0xeca31361431f07250be77259915bcc062c3e54d92ccee874b9e76cb1da8246f9","transactionIndex":"74","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0xeef417e1d5cc832e619ae18d2f140de2999dd4fb","value":"0","gas":"399967","gasPrice":"6434778487","isError":"0","txreceipt_status":"1","input":"0x2e1a7d4d00000000000000000000000000000000000000000000000000000000000015c3","contractAddress":"","cumulativeGasUsed":"6163338","gasUsed":"312700","confirmations":"1383555","methodId":"0x2e1a7d4d","functionName":"withdraw(uint256 amount)"},{"blockNumber":"15695615","timeStamp":"1665138311","hash":"0x61225a4becc66f0db00483c142fe5957497c8392bbbb16edb42cf2942deb3806","nonce":"7","blockHash":"0xae68a2cfb79a451a0da977897da4034f51ce220b80307322a8cff4f7ba3d9de5","transactionIndex":"180","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0x408e41876cccdc0f92210600ef50372656052a38","value":"0","gas":"55918","gasPrice":"6022140950","isError":"0","txreceipt_status":"1","input":"0x095ea7b30000000000000000000000001111111254fb6c44bac0bed2854e76f90643097dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","contractAddress":"","cumulativeGasUsed":"17117776","gasUsed":"48624","confirmations":"1383523","methodId":"0x095ea7b3","functionName":"approve(address _spender, uint256 _value)"},
    {"blockNumber":"15695618","timeStamp":"1665138347","hash":"0x4c75a4a96a2375f2b0d9a89a6f188ba6930f7fd8613ddac3b57e3162deb06b9c","nonce":"8","blockHash":"0xd55d2169d64124ee5f266ad0655ac38a3289507738733df0f85417fff7203045","transactionIndex":"248","from":"0x324e2d42d7b65e5574787c331dfaa29d2dead666","to":"0x1111111254fb6c44bac0bed2854e76f90643097d","value":"0","gas":"166287","gasPrice":"4832356260","isError":"0","txreceipt_status":"1","input":"0x2e95b6c8000000000000000000000000408e41876cccdc0f92210600ef50372656052a38000000000000000000000000000000000000000000000014a73f27bb57d6aabf000000000000000000000000000000000000000000000000008090c54d5a33310000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000140000000000000003b6d03408bd1661da98ebdd3bd080f0be4e6d9be8ce9858ce26b9977","contractAddress":"","cumulativeGasUsed":"29879150","gasUsed":"107371","confirmations":"1383520","methodId":"0x2e95b6c8","functionName":"unoswap(address srcToken, uint256 amount, uint256 minReturn, bytes32[])"}]}

d2 = requests.get(url)
print('D2: ', d2.text)
def pub_key_from_tx_eth1(txid):
    tx = w3.eth.getTransaction(txid)
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
    if check_address == tx['from']:
        print('Found: ', s.recover_public_key_from_msg_hash(ut.hash()), ' From: ', check_address)
        return s.recover_public_key_from_msg_hash(ut.hash())
    else:
        print('Not Found')
        return None

def pub_key_from_tx_eth2(txid, chain='ETH'):
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
        #raise ValueError("Unable to obtain public key from transaction: " + f"{txid}")
    return(rec_pub)

for i in d["result"]:
    print(i['hash'])
    print(pub_key_from_tx_eth1(transaction))
    print('#####')
    print(pub_key_from_tx_eth2(transaction))
    print('#################################################')
