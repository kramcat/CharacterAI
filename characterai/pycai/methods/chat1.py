from .utils import Request, caimethod, validate
from ...types import chat1

class ChatV1(Request):
    def __init__(self, session = None, token = None):
        self.session = session
        self.token = token

    @caimethod
    def send_message(
        self, chat_id: str, tgt: str, text: str,
        token: str = None, **kwargs
    ):
        """Sending a message to chat

        EXAMPLE::

            await client.chat1.send_message('CHAT_ID', 'TGT', 'TEXT')

        Args:
            chat_id (``str``):
                Chat or room ID

            tgt (``str``):
                Old character ID type

            text (``str``):
                Message text

            primary_msg_uuid (``str``, *optional*):
                Reply to the next generated message from
                :obj:`~characterai.aiocai.methods.chat1.ChatV1.next_message`

        Returns:
            :obj:`~characterai.types.chat1.Message`
        """
        data = self.request(
            'chat/streaming/', token=token,
            data={
                'history_external_id': chat_id,
                'text': text,
                'tgt': tgt,
                **kwargs
            }
        )

        return chat1.Message.model_validate(
            data
        )

    @caimethod
    def get_chat(
        self, char_id: str, chat_id: str,
        token: str = None
    ):
        """Get information about the chat

        EXAMPLE::

            await client.chat1.get_chat('CHAR', 'CHAT_ID')

        Args:
            char_id (``str``):
                Character ID

            chat_id (``str``):
                Room or chat ID

        Returns:
            :obj:`~characterai.types.chat1.ChatHistory`
        """
        data = self.request(
            'chat/history/continue/',
            token=token, data={
                'character_external_id': char_id,
                'history_external_id': chat_id
            }
        )

        return chat1.ChatHistory.model_validate(
            data
        )

    @caimethod
    def new_chat(
        self, char_id: str, *, token: str = None
    ):
        """Create a new chat

        EXAMPLE::

            await client.chat1.new_chat('CHAR_ID')

        Args:
            char_id (``str``):
                Character ID

        Returns:
            :obj:`~characterai.types.chat1.NewChat`
        """
        data = self.request(
            'chat/history/create/',
            token=token, data={
                'character_external_id': char_id
            }
        )
        
        return chat1.NewChat.model_validate(
            data
        )

    @caimethod
    def next_message(
        self, chat_id: str, tgt: str,
        parent_msg_uuid: str, *,
        token: str = None, **kwargs
    ):
        """Generate an alternative answer

        EXAMPLE::

            msg = await client.chat1.send_message(
                'CHAT_ID', 'TGT', 'TEXT'
            )

            await client.chat1.next_message(
                'CHAT_ID', 'TGT', msg.last_user_msg_uuid
            )

        Args:
            chat_id (``str``):
                Chat ID

            tgt (``str``):
                Old character ID type

            parent_msg_uuid (``str``):
                ID of the message from which you
                want to get an alternative reply

        Returns:
            :obj:`~characterai.types.chat1.Message`
        """
        return chat1.Message.model_validate(
            self.request(
                'chat/streaming/',
                token=token, data={
                    'history_external_id': chat_id,
                    'parent_msg_uuid': parent_msg_uuid,
                    'tgt': tgt,
                    **kwargs
                }
            )
        )

    @caimethod
    def get_histories(
        self, char: str, *, num: int = 999,
        token: str = None
    ):
        """Get a list of your character's chat histories

        EXAMPLE::

            await client.chat1.get_histories('CHAR_ID')

        Args:
            char (``str``):
                Character ID

            num (``str``):
                Maximum number of chats

        Returns:
            :obj:`~characterai.types.chat1.History`
        """
        data = self.request(
            'chat/character/histories_v2/',
            token=token, data={
                'external_id': char,
                'number': num
            }
        )

        return validate(
            chat1.History,
            data['histories']
        )

    @caimethod
    def get_history(
        self, chat_id: str,
        *, token: str = None
    ):
        """Get chat history

        EXAMPLE::

            await client.chat1.get_history('CHAT_ID')

        Args:
            chat_id (``str``):
                Chat ID

        Returns:
            :obj:`~characterai.types.chat1.History`
        """
        data = self.request(
            'chat/history/msgs/user/?'
            'history_external_id='
            f'{chat_id}', token=token
        )

        return chat1.HisMessages.model_validate(
            data
        )

    @caimethod
    def delete_message(
        self, chat_id: str, uuids: list,
        *, token: str = None
    ) -> bool:
        """Deleting messages. Returns ``True`` on success.

        EXAMPLE::

            await client.chat1.delete_message('CHAT_ID', ['UUID'])

        Args:
            chat_id (``str``):
                Chat ID

            uuids (List of ``str``):
                List of message IDs to be deleted

        Returns:
            ``bool``
        """
        self.request(
            'chat/history/msgs/delete/',
            token=token, data={
                'history_id': chat_id,
                'uuids_to_delete': uuids
            }
        )

        return True

    @caimethod
    def migrate(
        self, chat_id: str, *,
        token: str = None
    ):
        """Migrate chat1 to chat2

        EXAMPLE::

            await client.chat1.migrate('CHAT_ID')

        Args:
            chat_id (``str``):
                Chat1 ID

        Returns:
            :obj:`~characterai.types.chat1.Migrate`
        """
        self.request(
            f'migration/{chat_id}',
            token=token, data=True, neo=True
        )

        data = self.request(
            f'migration/{chat_id}',
            token=token, neo=True
        )

        return chat1.Migrate.model_validate(
            data['migration']
        )