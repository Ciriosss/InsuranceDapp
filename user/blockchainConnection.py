from web3 import Web3
import json

# connecting to my local blockchain
ganache_url = "HTTP://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# smart contract info
contractAddress = web3.toChecksumAddress("0xCad3c874F0118D4244C105Ac75EA3a8584d16f92")
path = "C:/Users/domen/PycharmProjects/solidity/insurance/truffle/build/contracts/HAMSAToken.json"

with open(path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    abi = contract_json['abi']
    bytecode = contract_json['bytecode']

contract = web3.eth.contract(address=contractAddress, abi=abi, bytecode=bytecode)

"""
Function that determines the imported ethereum address via the private key.
the pk is encrypted before being saved on the server
"""
def newAccount(profile,privateKey):

   account = web3.eth.account.privateKeyToAccount(privateKey)
   profile.address = account.address
   profile.encrypt = account.encrypt('start2impact')

   profile.save()

#function to transfer ether from one account to another
def transaction(profile,amount):

    str = profile.encrypt
    encrypt = str.replace("\'", "\"")
    privakeKey = web3.eth.account.decrypt(encrypt, "start2impact")
    addressFrom = profile.address

    addressTo = web3.eth.accounts[0]

    nonce = web3.eth.getTransactionCount(addressFrom)
    tx = {
        'nonce': nonce,
        'to': addressTo,
        'value': web3.toWei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    }
    signed_tx = web3.eth.account.signTransaction(tx,privakeKey)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return (web3.toHex(tx_hash))

"""
functions to transfer tokens by calling the functions of the smart contract
"""
def buyToken(_to, _value):

    _from = web3.eth.accounts[0]
    _value = int(_value)
    # contract function to transfer the ERC20 token
    contract.functions.transferFrom(_from,_to, _value).transact()

def buyPolicy(_from, _value):

    _to = web3.eth.accounts[0]
    _value = int(_value)
    # contract function to transfer the ERC20 token
    contract.functions.transferFrom(_from,_to, _value).transact()

def getTokenBalance(profile):

    web3.eth.defaultAccount = profile.address
    return contract.functions.balanceOf().call()

def getEthBalance(address):

    wei = web3.eth.getBalance(address)
    balance = web3.fromWei(wei,'ether')
    return round(balance, 4)

def supply():

    web3.eth.defaultAccount = web3.eth.accounts[0]
    supply = contract.functions.supply().call()
    return supply




