#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
import random
import string
import jwcrypto.jwk as pyjwk
from .helper import check_password
from sanic.log import logger
from sanic_jwt import Authentication, exceptions, Claim

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from web_backend.nvlserver.module.user.service import get_user_login_by_email
from web_backend.nvlserver.module.permission.service import (
    get_permission_list_for_user, get_permission_module_list_by_user_id
)
from web_backend.nvlserver.helper.dict_utils import sub_dict

from .helper import update_user_in_redis

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'NVLCustomClaim', 'RedisPgAuthentication',
    'generate_public_rsa_ssh_without_password', 'generate_rsa_token_key',
    'generate_random_secret', 'redis_lock_user_profile',
    'update_user_in_redis', 'nv_payload_extender', 'nv_scope_extender'
]


class NVLCustomClaim(Claim):
    key = 'smeg'

    def setup(self, payload, user):
        """

        :param payload:
        :param user:
        :return:
        """
        # logger.info('This is a custom claim ...........................')
        # logger.info(payload, user)
        return 'bar'

    def verify(self, value) -> bool:
        """

        :param value:
        :return:
        """
        return value == 'bar'


class RedisPgAuthentication(Authentication):

    async def authenticate(self, request, *args, **kwargs):
        """ Authenticate user

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        # logger.info(request.json)

        if not username or not password:
            raise exceptions.AuthenticationFailed(
                'Missing username or password.'
            )

        else:
            # QUERY DATA FROM REDIS AND DECODE TO UTF-8
            red_user_bin = await request.app.redis.get('user:{}'.format(username))
            red_user = red_user_bin.decode() if red_user_bin is not None else None
            user_data = ujson.loads(red_user) if red_user else None

            if user_data is None:
                # If there is no user data in redis -> query the database
                db_user = await get_user_login_by_email(request, username)

                if db_user is None:
                    raise exceptions.AuthenticationFailed(
                        'Unknown user'
                    )
                else:
                    scopes = await get_permission_list_for_user(request, db_user.get('user_id'))
                    module_list = await get_permission_module_list_by_user_id(request, user_id=db_user.get('user_id'))
                    # logger.info('THESE ARE SCOPES: {}'.format(scopes))
                    if scopes:
                        db_user.update({'scopes': [x.get('permission') for x in scopes]})
                    if module_list:
                        db_user.update({'acl': [x.get('module_name') for x in module_list]})
                    await request.app.redis.set('user:{}'.format(
                        db_user.get('user_id')), ujson.dumps(db_user))

            password_check = await check_password(request, username, password)
            if password_check:

                ret_val = sub_dict(
                    db_user, ['user_id', 'fullname', 'email', 'timezone_id', 'timezone_name', 'map_pool_time',
                              'language_id', 'language_name', 'language_short_code',
                              'account_type_id', 'account_type_name', 'acl', 'scopes'])
            else:
                raise exceptions.AuthenticationFailed(
                    'Passwords do not match.'
                )

        return ret_val

    async def store_refresh_token(self, user_id, refresh_token, *args, **kwargs):
        """ Store refresh token to redis

        :param user_id:
        :param refresh_token:
        :param args:
        :param kwargs:
        :return:
        """

        key = 'refresh_token:{user_id}'.format(user_id=user_id)
        await self.app.redis.set(key, refresh_token)

    async def retrieve_refresh_token(self, user_id, *args, **kwargs):
        """ Retrieve refresh token from redis

        :param user_id:
        :param args:
        :param kwargs:
        :return:
        """

        key = 'refresh_token:{user_id}'.format(user_id=user_id)
        red_token = await self.app.redis.get(key)
        token = red_token.decode() if red_token is not None else None
        return token

    async def retrieve_user(self, request, payload, *args, **kwargs):
        ret_val = None
        if payload:
            # logger.info(payload)
            user_id = payload.get('user_id', None)
            if user_id:
                user_data_bin = await request.app.redis.get('user:{}'.format(user_id))

                if user_data_bin:
                    ret_val = ujson.loads(user_data_bin.decode())
                else:
                    db_user = await get_user_login_by_email(request, user_id)
                    if db_user is not None:
                        scopes = await get_permission_list_for_user(request, db_user.get('user_id'))
                        module_list = await get_permission_module_list_by_user_id(request, user_id=user_id)
                        if scopes:
                            db_user.update({'scopes': [x.get('permission') for x in scopes]})

                        if module_list:
                            db_user.update({'acl': [x.get('module_name') for x in module_list]})

                        await request.app.redis.set('user:{}'.format(db_user.get('user_id')), ujson.dumps(db_user))
                        ret_val = db_user

        return ret_val

    async def add_scopes_to_payload(self, payload, user, *args, **kwargs):
        """ Add scopes to payload user_permissions etc.

        :param payload:
        :param user:
        :param args:
        :param kwargs:
        :return:
        """

        scopes: list = []
        if user:
            scopes = user.get('scopes')
        return scopes

    def override_scope_validator(  # noqa
        self,
        is_valid,
        required,
        user_scopes,
        require_all_actions,
        *args,
        **kwargs
    ):
        """ Override default sanic scope validator.

        :param is_valid:
        :param required:
        :param user_scopes:
        :param require_all_actions:
        :param args:
        :param kwargs:
        :return:
        """

        if not user_scopes:
            return False

        is_valid = False

        for requested in user_scopes:
            if required[0]:
                valid_namespace = required[0] == requested[0]
            else:
                valid_namespace = True

            if required[1]:
                if len(requested[1]) == 0:
                    valid_actions = True
                else:
                    method = all if require_all_actions else any
                    valid_actions = method(x in requested[1] for x in required[1])
            else:
                if require_all_actions is False:
                    valid_actions = True
                else:
                    valid_actions = False

            is_valid = all([valid_namespace, valid_actions])
            if is_valid:
                break

        return is_valid


def generate_public_rsa_ssh_without_password(
        key_size: int = 2048) -> bool:
    """Function that generates private and public RSA keys without password

    :param key_size: int -> RSA key size

    :return:
    """

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size, backend=default_backend())

    public_key = private_key.public_key().public_bytes(
        serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)

    return public_key.decode()


def generate_rsa_token_key(
        crypt='EC',
        key_size: int = 2048):
    key = pyjwk.JWK.generate(kty=crypt, size=key_size)
    return key.export_to_pem(private_key=True, password=None), key.export_to_pem(private_key=False, password=None)


def generate_random_secret(
        key_size: int = 2048):
    """ Generate random secret

    :param key_size: int -> number of characters.
    :return:
    """
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(key_size))


async def redis_lock_user_profile(
        request, user_id: int = 0) -> bool:
    ret_val = False
    if request:
        red_user_bin = await request.redis.get('user:{}'.format(user_id))
        if red_user_bin is not None:
            await request.delete('user:{}'.format(user_id))
            await request.delete('refresh_token:{}'.format(user_id))
            ret_val = True

    return ret_val


async def nv_payload_extender(payload, user, *args, **kwargs) -> dict:
    """ Simple payload extender for sanic jwt.
    In future implementation extender might leverage permission table.

    :param payload:
    :param user:
    :param args:
    :param kwargs:
    :return: dict -> updated payload
    """

    if payload and user:
        payload.update({'user': sub_dict(
            user, [
                'user_id', 'fullname', 'email', 'timezone_id', 'timezone_name', 'map_pool_time',
                'language_id', 'language_name', 'language_short_code',
                'account_type_id', 'account_type_name', 'acl'])
        })

    else:
        payload.update({'user': None})
    return payload


async def nv_scope_extender(user, *args, **kwargs):
    """ Adding scope extender.

    :param user:
    :param args:
    :param kwargs:
    :return:
    """

    scopes: list = []
    if user:
        scopes = user.get('scopes')
    return scopes
