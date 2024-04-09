from ...types import character, recent
from .utils import caimethod, validate

class Recent:
    @caimethod
    async def get_recent_chats(self, *, token: str = None):
        """Recent characters chatted with

        EXAMPLE::

            await client.get_recent_chats()

        Returns:
            List of :obj:`~characterai.types.character.CharShort`
        """
        data = await self.request(
            'chat/characters/recent/',
            token=token
        )

        return validate(
            character.CharShort,
            data['characters']
        )

    @caimethod
    async def get_recent_rooms(self, *, token: str = None):
        """Recent rooms

        EXAMPLE::

            await client.get_recent_rooms()

        Returns:
            List of :obj:`~characterai.types.recent.Room`
        """
        data = await self.request(
            'chat/rooms/recent/',
            token=token
        )

        return validate(
            recent.Room, data['rooms']
        )

    @caimethod
    async def get_recent(self, *, token: str = None):
        """Recent chats

        EXAMPLE::

            await client.get_recent()

        Returns:
            List of :obj:`~characterai.types.recent.Chat`
        """
        data = await self.request(
            'chats/recent/', neo=True,
            token=token
        )

        return validate(
            recent.Chat, data['chats']
        )