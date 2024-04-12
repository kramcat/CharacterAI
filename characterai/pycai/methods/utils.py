from characterai.pycai import client, methods
from ...errors import (
    ServerError, AuthError,
    JSONError
)

from curl_cffi import CurlMime

from functools import wraps
import json

class Request:
    def request(
        self, url: str, *, token: str = None,
        method: str = 'GET', data: dict = {},
        split: bool = False, neo: bool = False,
        multipart: CurlMime = None
    ):
        key = self.token or token

        if key == None:
            raise AuthError('No token')

        headers = {
            "Authorization": f"Token {key}"
        }

        link = f'https://plus.character.ai/{url}'

        if neo:
            link = link.replace('plus', 'neo')

        if multipart != None:
            r = self.session.post(
                link, headers=headers, data=data,
                multipart=multipart
            )
        elif data != {} or data:
            r = self.session.post(
                link, headers=headers, json=data
            )
        elif method == 'GET':
            r = self.session.get(
                link, headers=headers
            )
        elif method == 'PUT':
            r = self.session.put(
                link, headers=headers, json=data
            )

        if neo and not r.ok:
            try:
                raise ServerError(r.json()['comment'])
            except KeyError:
                raise ServerError(r.text)

        if r == 404:
            raise ServerError('Not Found')
        elif not r.ok:
            raise ServerError(r.status_code)

        text = r.text

        if '}\n{' in text:
            text = '{' + text.split('}\n{')[-1]

        try:
            res = json.loads(
                text.encode('utf-8')
            )
        except json.decoder.JSONDecodeError:
            raise JSONError(
                'Unable to decode JSON.'
                f'Server response: {r.text}'
            )

        try:
            if res['force_login']:
                raise AuthError('Need Auth')
            elif res['status'] != 'OK' or res['abort']:
                raise ServerError(res['error'])
            elif res['error'] != None:
                raise ServerError(res['error'])
        except KeyError:
            return res

def checkSession(args) -> bool:
    return any(
        isinstance(
            a, client.pycai.Client
        ) for a in args
    )

def delClass(args) -> tuple:
    new = ()

    for a in args:
        if not isinstance(a, (
            methods.chat1.ChatV1
        )):
            new = (a, *new)

    return new[::-1]

def caimethod(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            try:
                token = kwargs['token']
            except (AttributeError, KeyError):
                token = args[0].token
        except AttributeError:
            token = None

        temp = False

        if not checkSession(args):
            temp = True

            args = (client.pycai.Client(
                token=token
            ), *args)

        args = delClass(args)

        result = func(*args, **kwargs)

        # Closing the session if the function
        # was used through a library class
        if temp:
            args[0].close()

        return result
    
    return wrapper

def flatten(d, parent_key='', sep=''):
    items = []
    for k, v in d.items():
        if v == '':
            v = None

        if isinstance(v, dict):
            items.extend(flatten(v, k, sep=sep).items())
        else:
            items.append((k, v))
    return dict(items)

def validate(_class, data):
    return [
        _class(**a) for a in data
    ]
