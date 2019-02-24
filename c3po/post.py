import os
import sys
import json
from Crypto.Cipher import AES

#TODO unit test this

class PostProcess():
    def __init__(self, binarypath, statepath):
        self.binarypath = binarypath
        with open(statepath, "r") as s:
            self.state = json.load(s)
        self.data = list(open(self.binarypath,"rb").read())

    def write(self):
        with open(self.binarypath, "wb") as bf:
            bf.write(bytes(self.data))

    def encrypt(self):
        pe = self.state["post_encrypt"]
        keys = [{"key":batch["key"], "len":batch["len"]} for batch in pe]
        print("Finding {} keys:".format(len(keys)))
        for i, batch in enumerate(keys):
            print("    "+''.join("{:02x}".format(k) for k in batch["key"]))

        keystocheck = [i for i in range(len(keys))]
        for i,d in enumerate(self.data):
            for k in keystocheck:
                #if the first byte matches check the rest
                #i could implement a string matching algorithm or i could not
                if d == keys[k]["key"][0] and self.data[i:i+32] == keys[k]["key"]:
                    #print("    found {} at offset {}".format(k, i))
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
                print("Unable to find key {}".format(''.join("{:02x}".format(k) for k in keys[k]["key"])))
            print("Malformed binary, aborting")
            sys.exit(1)

        print("Encrypting:")
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
                    print("PKCS7 padding verification failed")
                    print(''.join(raw_data))
                    print("abborting")
                    sys.exit(1)
            print("PKCS7 passed ", end='')

            cipher = AES.new(bytes(key_data), AES.MODE_CBC, bytes(iv_data))
            enc_data = list(cipher.encrypt(bytes(raw_data)))

            print("{}{}".format(''.join("{:02x}".format(k) for k in raw_data[:32]),
                                  "" if len(raw_data) <= 32 else "...{} bytes more".format(len(raw_data)-32)))

            #overwrite the raw data with the encrypted version
            self.data[enc_start:enc_end] = enc_data

