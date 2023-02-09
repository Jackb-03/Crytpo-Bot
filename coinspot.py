# Adapted from Clugg coinspot-py: https://github.com/clugg/coinspot-py
import hashlib
from flask import session
import requests
import hmac
import json
from time import time
from hashlib import sha512

api_key = "630e2b3bb27264b9a9c7f684c701abbe"
api_secret = "U853N9EQ5QA3WLLAPYQEHDGCECPDC2QKQL3BDQA5GN27WD6MJCZTD4F6V1WK3QBQ5L57J7VNYYJCF977"

def api_public_request(path):
    api_endpoint = "https://www.coinspot.com.au/pubapi/v2/"
    return requests.get(api_endpoint+path, verify=False).json()





def _chunker(self, data):
    yield data

def api_request(path):
    api_endpoint = "https://www.coinspot.com.au/api/v2"

    data = {"nonce" : int(time() * 1000)}
    json_data = json.dumps(data, separators=(',', ':')).encode()

    return requests.post(
        api_endpoint + path,
        verify=False,
        data=self._chunker(json_data),

        headers={
            "Content-Type": "application/json",
            "sign": hmac.new(session['secret_key'].encode(), json_data, sha512).hexdigest(),
            "key": session['api_key']
        }
    ).json()










def latest(cointype=None):
    path = "latest"
    if cointype:
        path = path + "/" + cointype
        print (path)    
    return api_public_request(path)



def my_balances():
    return api_request("my/balances")

def my_balance(cointype):
    return api_request("my/balance/"+cointype)

def my_deposit():
    return api_request("my/deposits")

def my_purchase(cointype=None, amount=None, amounttype = None):
    path = "/quote/buy/now"
    if cointype:
        path = path + "/" + amount  + "/" + amounttype
    return api_request(path)


def check():
    return api_request("/status")








