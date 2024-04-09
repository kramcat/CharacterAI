import json
import websockets
from websockets import exceptions
import uuid

from .utils import Request, caimethod, validate
from ...errors import ServerError
from ...types import chat2

class ChatV2(Request):
    def __init__(
        self, session = None,
        token: str = None
    ):
        self.session = session
        self.token = token

    @caimethod
    async def get_histories(
        self, char: str, *,
        preview: int = 2, token: str = None
    ):
        """Get a list of your character's chat histories

        EXAMPLE::

            await client.get_chat('CHAR')

        Args:
            char (``str``):
                Character ID
            
            preview (``int``, *optional*):
                The number of recent messages
                that will be shown

        Returns:
            List of :obj:`~characterai.types.chat2.ChatData`
        """
        data = await self.request(
            f'chats/?character_ids={char}'
            f'&num_preview_turns={preview}',
            token=token, neo=True
        )

        return validate(
            chat2.ChatData,
            data['chats']
        )

    @caimethod
    async def get_history(
        self, chat_id: str, *,
        token: str = None
    ):
        """Get chat history

        EXAMPLE::

            await client.get_history('CHAT_ID')

        Args:
            chat_id (``str``):
                Chat ID

        Returns:
            :obj:`~characterai.types.chat2.History`
        """
        return chat2.History.model_validate(
            await self.request(
                f'turns/{chat_id}/',
                token=token, neo=True
            )
        )

    @caimethod
    async def get_chat(
        self, char: str, *,
        token: str = None
    ):
        """Get information about the last chat

        EXAMPLE::

            await client.get_chat('CHAR')

        Args:
            char (``str``):
                Character ID

        Returns:
            :obj:`~characterai.types.chat2.ChatData`
        """
        return chat2.ChatData.model_validate(
            (await self.request(
                f'chats/recent/{char}',
                token=token, neo=True
            ))['chats'][0]
        )

    @caimethod
    async def pin(
        self, pinned: bool, chat_id: str,
        turn_id: str, *, token: str = None
    ):
        """Pin chat messages

        This is to make sure characters
        don't forget certain things
        and they will always remember
        what's in the pinned posts

        EXAMPLE::

            await client.pin(PINNED, 'CHAT_ID', 'TURN_ID')

        Args:
            pinned (``bool``):
                ``True`` pin, ``False`` unpin
            
            chat_id (``str``):
                Chat ID
            
            turn_id (``str``):
                Message ID

        Returns:
            :obj:`~characterai.types.chat2.BotAnswer`
        """
        return chat2.BotAnswer.model_validate(
            (await self.request(
                'turn/pin', neo=True,
                token=token, data={
                    'is_pinned': pinned,
                    'turn_key': {
                        'chat_id': chat_id,
                        'turn_id': turn_id
                    }
                }
            ))['turn']
        )

    async def delete_message(
        self, chat_id: str, ids: list
    ) -> bool:
        """Deleting messages. Returns ``True`` on success

        EXAMPLE::

            await client.delete_message('CHAT_ID', ['UUID'])

        Args:
            chat_id (``str``):
                Chat ID
            
            ids (List of ``str``):
                List of message IDs to be deleted
            
        Returns:
            ``bool``
        """
        await self.ws.send(json.dumps({
            'command':'remove_turns',
            'payload': {
                'chat_id': chat_id,
                'turn_ids': ids
            }
        }))

        response = json.loads(await self.ws.recv())

        if response['command'] == 'neo_error':
            raise ServerError(response['comment'])

        return True

    async def next_message(
        self, char: str, chat_id: str, turn_id: str, 
        *, tts: bool = False, lang: str = 'English'
    ):
        """Generate an alternative answer

        EXAMPLE::

            await client.next_message(
                'CHAR', 'CHAT_ID', 'MSG_ID'
            )

        Args:
            char (``str``):
                Character ID
            
            chat_id (``str``):
                Chat ID
            
            turn_id (``str``):
                Message ID
            
            tts (``bool``, *optional*):
                Generate audio for the message
            
            lang (``str``, *optional*):
                The language of your message.
                That's the language you're most
                likely to respond in.

        Returns:
            :obj:`~characterai.types.chat2.BotAnswer`
        """
        await self.ws.send(json.dumps({
            'command':'generate_turn_candidate',
            'payload': {
                'tts_enabled': tts,
                'selected_language': lang,
                'character_id': char,
                'turn_key': {
                    'turn_id': turn_id,
                    'chat_id': chat_id
                }
            }
        }))

        while True:
            response = json.loads(await self.ws.recv())
    
            try:
                turn = response['turn']
            except:
                raise ServerError(response['comment'])
    
            if not turn['author']['author_id'].isdigit():
                try:
                    turn['candidates'][0]['is_final']
                except: ...
                else:
                    return chat2.BotAnswer.model_validate(
                        turn
                    )

    async def new_chat(
        self, char: str, creator_id: str,
        *, greeting: bool = True, chat_id: str = None
    ):
        """Editing the message text

        EXAMPLE::

            await client.new_chat('CHAR', 'CREATOR_ID')

        Args:
            char (``str``):
                Character ID
            
            creator_id (``str``):
                Your account ID. Can be found at
                :obj:`~characterai.aiocai.methods.chat2.ChatV2.get_me`
            
            greeting (``bool``, *optional*):
                If ``False``, the new chat will be
                without the character's first message
            
            chat_id (``str``, *optional*):
                You can specify your chat ID,
                it can be any ``str``

        Returns:
            :obj:`~characterai.types.chat2.BotAnswer`
        """
        chat_id = str(uuid.uuid4()) or chat_id

        if isinstance(creator_id, int):
            creator_id = str(creator_id)
        
        await self.ws.send(json.dumps({
            'command': 'create_chat',
            'payload': {
                'chat': {
                    'chat_id': chat_id,
                    'creator_id': creator_id,
                    'visibility': 'VISIBILITY_PRIVATE',
                    'character_id': char,
                    'type': 'TYPE_ONE_ON_ONE'
                },
                'with_greeting': greeting
            }
        }))

        response = json.loads(await self.ws.recv())
        try: response['chat']
        except KeyError:
            raise ServerError(response['comment'])
        else:
            answer = chat2.BotAnswer.model_validate(
                json.loads(
                    await self.ws.recv()
                )['turn']
            )

            response = chat2.ChatData.model_validate(
                response['chat']
            )

            return response, answer

    async def send_message(
        self, char: str, chat_id: str, text: str,
        author: dict = {}, *, image: str = None,
        custom_id: str = None
    ):
        """Sending a message to chat

        EXAMPLE::

            await client.send_message('CHAR', 'CHAT_ID', 'TEXT')

        Args:
            char (``str``):
                Character ID
            
            chat_id (``str``):
                Chat ID
            
            text (``str``):
                Message text
            
            custom_id (``str``, *optional*):
                Its ID for the message, can be any ``str``
            
            image (``str``, *optional*):
                Attach image to message. This should
                be the URL path on the server

        Returns:
            :obj:`~characterai.types.chat2.BotAnswer`
        """
        turn_key = {
            'chat_id': chat_id
        }
        
        if custom_id != None:
            turn_key['turn_id'] = custom_id

        message = {
            'command': 'create_and_generate_turn',
            'payload': {
                'character_id': char,
                'turn': {
                    'turn_key': turn_key,
                    'author': author,
                    'candidates': [
                        {
                            'raw_content': text,
                            'tti_image_rel_path': image
                        }
                    ]
                }
            }
        }

        await self.ws.send(json.dumps(message))

        while True:
            response = json.loads(await self.ws.recv())

            try:
                turn = response['turn']
            except:
                raise ServerError(response['comment'])

            if not turn['author']['author_id'].isdigit():
                try:
                    turn['candidates'][0]['is_final']
                except: ...
                else:
                    return chat2.BotAnswer.model_validate(
                        turn
                    )

    async def edit_message(
        self, chat_id: str, message_id: str,
        text: str, *, token: str = None
    ):
        """Edit the message text

        EXAMPLE::

            await client.edit_message('CHAT_ID', 'MSG_ID', 'TEXT')

        Args:
            chat_id (``str``):
                Chat ID
            
            message_id (``str``):
                Message ID
            
            text (``str``):
                New message text

        Returns:
            :obj:`~characterai.types.chat2.BotAnswer`
        """
        await self.ws.send(json.dumps({
            'command':'edit_turn_candidate',
            'payload': {
                'turn_key': {
                    'chat_id': chat_id,
                    'turn_id': message_id
                },
                'new_candidate_raw_content': text
            }
        }))

        response = json.loads(await self.ws.recv())

        try: response['turn']
        except KeyError:
            raise ServerError(response['comment'])
        else:
            return chat2.BotAnswer.model_validate(
                response['turn']
            )

class WSConnect(ChatV2):
    def __init__(
        self, token: str = None,
        *, start: bool = True
    ):
        if not start:
            self.token = token

    async def __call__(
        self, token: str = None,
        *, start: bool = True
    ):
        self.token = token or self.token
        
        if not start:
            return None

        return await self.__aenter__(self.token)

    async def __aenter__(
        self, token: str = None
    ):
        cookie = f'HTTP_AUTHORIZATION="Token {self.token}"'
        try:
            self.ws = await websockets.connect(
                'wss://neo.character.ai/ws/',
                extra_headers={
                    'Cookie': cookie
                }
            )
        except exceptions.InvalidStatusCode as e:
            if e.status_code == 403:
                raise ServerError('Wrong token')

        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        return await self.ws.close()