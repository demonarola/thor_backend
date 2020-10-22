#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'
import re
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

HASH_REGEX_MATCH = r',"hash":"\w+"'

SSH_RSA_TEMP_STREAM = (
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDADgcVkg+oemrU3WDEsL+05sRibFRPEGGceZ9tA"
    "IP3xPs+OnqQI4cQLqUE6Xlzpls2cNSvYQZo1aanKlNh4hwPmF9bJ/CJazPRWsi3zhXLqTL8plhTPr"
    "4OvFFwTU1rdfgYZVolVByRuUdxZY7NJnoqv+3U7p6B7vz/LQPLbAj8dWbigKe1Is7Lv7gouG456aG"
    "0KdVoMLYyIC8/DBR3jhdxSodBGmqZ7uOi3HexTeeTDY5Dpe5dlAgQe55KjvyE6u1WITWpezOEjZHo"
    "sKkWgpZUp47qK32HFvShTwR7Wx9FyYbUEivDa1Xci+T7CRGH4tpxHxHrZP+J/AY477QdRhh7"
)
INITIAL_JSON_TEST_STREAM = (
    '{"request_id":1234567890,"modem_id":"21EC2020-3AEA-4069-A2DD-08002B30309D"'
    ',"lift_id":1234567890,"lift_group_id":1234567890}'
)

INITIAL_FAILED_TEST = '{"request_id":1234567890,"status":2}'


def generate_base_hash() -> str:
    """ Function that generates ssh public key.

    :return: str -> unicode public ssh key
    """
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)
    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
    return public_key.decode('utf-8')


def dehash_json(
        input_stream: str) -> (str, str):
    """ Function with a small wrapper that removes hash from JSON.
    On error it returns original json end error message as second param.

    :param input_stream: properly formatted JSON without any empty spaces
    :return: (str, str) Tuple containing JSON without hash and hash
    """
    hash_list = re.search(HASH_REGEX_MATCH, input_stream)
    matched_hash = hash_list.group(0)
    plain_json_list = input_stream.split(matched_hash)
    if matched_hash.startswith(',"hash":'):
        plain_hash = matched_hash[8:]
    else:
        plain_hash = ''
    return ''.join(plain_json_list).rstrip('\n').rstrip('\r'), plain_hash


def insert_hash_to_stream(
        initial_string: str,
        hashing_element: str) -> str:
    """ Functions that inserts hash generated from provided JSON and returns properly
    structured and signed JSON.

    :param initial_string: str -> JSON represented as a string.
    :param hashing_element: str -> hashing string -> string used as a seed
    :return: str -> JSON in string format with hash inserted.
    """
    m = hashlib.md5()
    m.update(initial_string.encode() + hashing_element.encode())
    return initial_string[0:-1] + ',"hash":"{}"{}'.format(m.hexdigest(), initial_string[-1:])


def generate_hash_for_stream(
        initial_string: str,
        hashing_element: str) -> str:
    """ Function used to generate MD5 hash from input string and seed.

    :param initial_string: str
    :param hashing_element: str
    :return: str
    """
    m = hashlib.md5()
    # print('HASH FOR STREAM STRING: {}'.format(initial_string.encode() + hashing_element.encode()))
    m.update(initial_string.encode() + hashing_element.encode())
    return m.hexdigest()
