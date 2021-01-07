from threading import Thread
import os, time, pprint
from web3 import Web3, eth
from tqdm import tqdm
from functions import simple_getTokenToTokenPrice
from orfeed import Orfeed
from data import token_symbols


w3 = Web3(Web3.HTTPProvider('https://'+os.getenv("NETWORK")+'.infura.io/v3/'+os.getenv("INFURA_PROJECT_ID")))
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) # uncomment if you use ganache-cli
orfeed_i = Orfeed(w3)

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        # print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def run():
    a = time.perf_counter()
    list_thread = {}
    for token in token_symbols:
        list_thread[token] = ThreadWithReturnValue(target=simple_getTokenToTokenPrice, args=(orfeed_i, token))
        list_thread[token].start()

    # res = [{i: list_thread[i].join()} for i in list_thread if list_thread[i].join() != -1]
    res = {}
    for i in list_thread:
        val = list_thread[i].join()
        if val != -1:
            res[i] = list_thread[i].join()
    # import pdb; pdb.set_trace()
    sorted_list = sorted(res.items(), key=lambda x: x[1]["%"], reverse=True)
    pprint.pprint(sorted_list)
    print(time.perf_counter() - a)

while True:
    run()
    for i in tqdm(range(20), desc="cooldown"):
        time.sleep(1)
