#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

import Crypto.Cipher.AES
import argparse
import base64
import boto3
import logging
import os
import os.path
import sys

def pad(data):
    return data + b" " * (32 - len(data) % 32)

def encrypt(kms, key_id, data, **kwargs):
    resp = kms.generate_data_key(KeyId=key_id, **kwargs)
    crypter = Crypto.Cipher.AES.new(resp.get("Plaintext"))
    encoded = base64.b64encode(data)
    encrypted = crypter.encrypt(pad(encoded))
    return (encrypted, resp.get("CiphertextBlob"))

def decrypt(kms, key_id, data, ciphertext_blob, **kwargs):
    resp = kms.decrypt(CiphertextBlob=ciphertext_blob, **kwargs)
    crypter = Crypto.Cipher.AES.new(resp.get("Plaintext"))
    decrypted = crypter.decrypt(data)
    decoded = base64.b64decode(decrypted)
    return decoded

def dump(name, data, armor):
    with open(name, "wb") as fp:
        if armor:
            fp.write(base64.b64encode(data))
        else:
            fp.write(data)

def load(name, armor):
    with open(name, "rb") as fp:
        if armor:
            return base64.b64decode(fp.read())
        else:
            return fp.read()

parser = argparse.ArgumentParser()

parser.add_argument("--armor", dest="armor", action="store_true", default=False)
parser.add_argument("--debug", dest="debug", action="store_true", default=False)
parser.add_argument("--encrypt", dest="encrypt", action="store_true", default=False)
parser.add_argument("--decrypt", dest="decrypt", action="store_true", default=False)
parser.add_argument("--key-id", dest="key_id", default=os.getenv("AWS_KMS_KEY_ID"))
parser.add_argument("--key-spec", dest="key_spec", default="AES_256")
parser.add_argument("--profile", dest="profile")

options, filenames = parser.parse_known_args(sys.argv[1:])

if options.debug:
  logging.basicConfig(level=logging.DEBUG)

if options.key_id is None:
    print("need CMK identifier", file=sys.stderr)
    sys.exit(1)

if options.profile:
    session = boto3.Session(profile_name=options.profile)
    kms = session.client("kms")
else:
    kms = boto3.client("kms")

if options.decrypt:
    for filename in filenames:
        ciphertext_blob = load(filename + ".key", options.armor)
        data = decrypt(kms, options.key_id, load(filename + ".enc", options.armor), ciphertext_blob)
        dump(filename, data, False)
else:
    for filename in filenames:
        data = load(filename, False)
        encrypted, ciphertext_blob = encrypt(kms, options.key_id, data, KeySpec=options.key_spec)
        dump(filename + ".enc", encrypted, options.armor)
        dump(filename + ".key", ciphertext_blob, options.armor)

# vim:set ft=python :
