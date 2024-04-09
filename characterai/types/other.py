import asyncio
from typing import Optional

from curl_cffi.requests import AsyncSession
from pydantic import BaseModel

class Avatar:
    """A class for working with avatars.
    
    It exists in all classes with ``avatar_file_name`` parameter.

    .. code-block:: python

        await data.avatar.download('FILE.PNG')
        
        print(data.avatar.url)

    Parameters:
        avatar (:obj:`~characterai.types.other.Image`, *property*):
            Avatar object

        url (``str``):
            Incomplete URL
        
        type (``str``):
            Avatar type

    .. autofunction:: characterai.types.other.Image.download
    """
    @property
    def avatar(self):
        return Image(
            url=self.avatar_file_name,
            icon='avatars'
        )

class QueryChar(BaseModel):
    """Character in search

    Parameters:
        document_id (``str``):
            ID in search (?)
        
        external_id (``str``):
            Char ID
        
        title (``str``):
            Short character description
        
        greeting (``str``):
            Character greeting (first message)
        
        avatar_file_name (``str``):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
        
        visibility (``str``):
            Who can see the character (everyone, you or from link)
        
        participant__name (``str``):
            Character name

        participant__num_interactions (``float``):
            Number of interactions (chats) with the character
        
        user__username (``str``):
            Author name
        
        priority (``float``):
            Priority in the search
        
        upvotes (``int``, *optional*):
            Number of character likes
    """
    document_id: str
    external_id: str
    title: str
    greeting: str
    avatar_file_name: str
    visibility: str
    participant__name: str
    participant__num_interactions: float
    user__username: str
    priority: float
    search_score: float
    upvotes: Optional[int] = None

class Image(BaseModel):
    """Image from server

    This class has a ``download()`` function that can be used
    to download a picture. If you are using the async version
    of the library, this function will be async

    Parameters:
        url (``str``):
            Incomplete URL
        
        type (``str``):
            Image type

    .. autofunction:: characterai.types.other.Image.download
    """
    url: str
    type: str = 'UPLOADED'
    icon: str = 'user'

    async def download(
        self, path: str = None,
        width: int = 400, type: str = 'user'
    ):
        """Download any picture

        EXAMPLE::

            await data.avatar.download('FILE.PNG')

        Parameters:
            path (``str``, *optional*):
                The path to the file or the file name.
                If no path is specified, a file will be
                created with a name from the server
            
            width (``int``, *optional*):
                File resolution. Default is 400

        Returns:
            Downloaded file
        """
        if type == 'CREATED':
            await asyncio.sleep(3)
        else:
            self.url = f'https://characterai.io/i/{width}/static/{self.icon}/{self.url}'

        async with AsyncSession() as s:
            data = await s.get(
                self.url
            )

        with open(
            path or self.url.split('/')[-1], 'wb'
        ) as f:
            f.write(data.content)

class Voice(BaseModel):
    """Voice for character messages

    Parameters:
        id (``int``):
            Vote number
        
        name (``str``):
            Voice name
        
        voice_id (``str``):
            Voice ID
        
        country_code (``str``):
            Language that supports voice. Other languages
            are not voiced/skipped in the text
        
        lang_code (``str``):
            Same as ``country_code``, but there may be difference
    """
    id: int
    name: str
    voice_id: str
    country_code: str
    lang_code: str