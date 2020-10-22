#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


async def generate_public_rsa_ssh_without_password(
        key_size: int = 2048) -> bool:
    """Function that generates RSA seed and creates MD5 hash from it.

    :param key_size: int -> RSA key size

    :return:
    """

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size, backend=default_backend())

    public_key = private_key.public_key().public_bytes(
        serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)

    return hashlib.md5(public_key.decode().encode()).hexdigest()
