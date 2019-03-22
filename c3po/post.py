import os
import sys
import json
import unittest
from .output import vprint
from Crypto.Cipher import AES

#TODO unit test this

class PostProcess():
    def __init__(self, data=[], state={}):
        self.state = state
        self.data = data

    def read_data(self, binarypath):
        self.data = list(open(binarypath,"rb").read())

    def read_state(self, statepath):
        with open(statepath, "r") as s:
            self.state = json.load(s)

    def write(self, binarypath):
        with open(binarypath, "wb") as bf:
            bf.write(bytes(self.data))

    def encrypt(self):
        pe = self.state["post_encrypt"]
        keys = [{"key":batch["key"], "len":batch["len"]} for batch in pe]
        if not keys:
            vprint("No keys to process")
            return
        vprint("Finding {} keys:".format(len(keys)))

        #record which keys are acually to check
        goodkeys = set()
        badkeys = set()
        for i, batch in enumerate(keys):
            vprint("    "+''.join("{:02x}".format(k) for k in batch["key"]))
            goodkeys.update(batch["key"])

        keystocheck = [i for i in range(len(keys))]

        if len(goodkeys) > 127:
            #there might be less bytes to blacklist than white
            badkeys = set(r for r in range(256) if r not in goodkeys)
            print(f"using blacklist: {len(badkeys)} {badkeys}")
        else:
            print(f"using whitelist: {len(goodkeys)} {goodkeys}")



        for i,d in enumerate(self.data):
            if d in badkeys or d not in goodkeys:
                #cheap skipforward
                continue;

            for k in keystocheck:
                #if the first byte matches check the rest
                #i could implement a string matching algorithm or i could not
                if d not in keys[k]["key"]:
                    continue;
                if d == keys[k]["key"][0] and self.data[i:i+32] == keys[k]["key"]:
                    #vprint("    found {} at offset {}".format(k, i))
                    keys[k]["offset"] = i
                    #found dont check for it again
                    keystocheck.remove(k)
                    #only one key per match
                    break
            if not keystocheck:
                #we found them all
                break
        if keystocheck:
            for k in keystocheck:
                vprint("Unable to find key {}".format(''.join("{:02x}".format(k) for k in keys[k]["key"])))
            vprint("Malformed binary, aborting")
            raise ValueError("Malformed Binary")

        vprint("Encrypting:")
        for batch in keys:
            key_data = batch["key"]

            iv_start = batch["offset"] + 32
            iv_end = iv_start + 16
            iv_data = self.data[iv_start:iv_end]

            enc_start = iv_end
            enc_end = enc_start + batch["len"]
            raw_data = self.data[enc_start:enc_end]

            #make sure the binary generated correctly
            padding_len = raw_data[-1]
            for p in range(1, padding_len + 1):
                if raw_data[p*-1] != padding_len:
                    vprint("PKCS7 padding verification failed")
                    vprint(''.join(raw_data))
                    vprint("abborting")
                    raise ValueError("Padding Failure")
            vprint("PKCS7 passed ", end='')

            cipher = AES.new(bytes(key_data), AES.MODE_CBC, bytes(iv_data))
            enc_data = list(cipher.encrypt(bytes(raw_data)))

            vprint("{}{}".format(''.join("{:02x}".format(k) for k in raw_data[:32]),
                                  "" if len(raw_data) <= 32 else "...{} bytes more".format(len(raw_data)-32)))

            #overwrite the raw data with the encrypted version
            self.data[enc_start:enc_end] = enc_data

class PostTest(unittest.TestCase):
    def test_init(self):
        p = PostProcess()
        self.assertEquals(p.data, [])
        self.assertEquals(p.state, {})

    def test_encryption(self):
        #only run in the directory in test
        if os.path.exists("./post_unittest"):
            p = PostProcess()
            p.read_data("./post_unittest")
            p.read_state("./post_unittest.json")


            p.encrypt()

            expected = list(open("./post_unittest_encrypted","rb").read())

            self.assertEquals(p.data, expected)
        else:
            vprint("please run from run_tests.sh in test/")

    def test_bad_key(self):
        #only run in the directory in test
        if os.path.exists("./post_unittest"):
            p = PostProcess()
            p.read_data("./post_unittest")
            p.read_state("./post_unittest.json")
            #corrupt the key
            p.state["post_encrypt"][0]["key"][0] += 1


            with self.assertRaises(ValueError):
                p.encrypt()
        else:
            vprint("please run from run_tests.sh in test/")
