from .utils import caimethod, validate
from ...types import other

class Chats:
    @caimethod
    def search(
        self, query: str, *, token: str = None
    ):
        """Search for characters by query

        EXAMPLE::

            await client.search('QUERY')

        Args:
            query (``str``):
                Query text

        Returns:
            List of :obj:`~characterai.types.other.QueryChar`
        """
        data = self.request(
            f'chat/characters/search/?query={query}'
        )

        return validate(
            other.QueryChar, data['characters']
        )

    @caimethod
    def create_room(
        self, name: str, chars: list,
        topic: str = '', token: str = None
    ) -> str:
        """Creating a room with a characters

        EXAMPLE::

            chars = [
                {
                    'value': 'CHAR_ID'
                    'label': 'CHAR_NAME',
                }
            ]
            await client.create_room('NAME', chars)

        Args:
            name (``str``):
                Room name

            chars (``list``):
                The characters in the room

            topic (``str``):
                Room theme description

        Returns:
            Room ID (``str``)
        """
        data = self.request(
            'chat/room/create/',
            token=token, data={
                'characters': chars,
                'name': name,
                'topic': topic,
                'visibility': 'PRIVATE'
            }
        )

        return data['room']['external_id']