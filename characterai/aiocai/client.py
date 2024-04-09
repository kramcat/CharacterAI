import asyncio
import sys

from .methods import Methods
from .methods.chat1 import ChatV1
from .methods.chat2 import WSConnect
from .methods.utils import Request

from curl_cffi.requests import AsyncSession

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

class aiocai(Methods, Request):
    chat1 = ChatV1()
    connect = WSConnect(start=False)

    class Client(Methods, Request):
        """CharacterAI client

        Args:
            token (``str``):
                Account auth token

            identifier (``str``):
                Which browser version to impersonate in the session

            **kwargs (``Any``):
                Supports all arguments from curl_cffi `Session <https://curl-cffi.readthedocs.io/en/latest/api.html#sessions>`_
        
        """
        def __init__(
            self, token: str = None,
            identifier: str ='chrome120',
            **kwargs
        ):
            self.token = token
            self.session = AsyncSession(
                impersonate=identifier,
                headers={
                    'Authorization': f'Token {token}'
                },
                **kwargs
            )

            self.chat1 = ChatV1(self.session, token)
            self.connect = WSConnect(token, start=False)

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            await self.session.close()

        async def close(self):
            """If you won't be using the client in the future, please close it"""
            await self.session.close()