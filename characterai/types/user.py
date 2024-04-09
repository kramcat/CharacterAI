from pydantic import BaseModel
from typing import List

from .other import Avatar
from .character import CharShort

class User(BaseModel, Avatar):
    """User info

    Parameters:
        characters (List of :obj:`~characterai.types.character.CharShort`):
            List of user's public characters

        username (``str``):
            Public username
        
        name (``str``):
            Public name
        
        num_following (``int``):
            Number of users subscribed to the account
        
        num_followers (``int``):
            Number of users who are subscribed to the account
        
        avatar_file_name (``str``, *optional*):
            Path to the avatar on the server
        
        subscription_type (``str``):
            Type of c.ai subscription
        
        bio (``str``, *optional*):
            Account desctiption
        
        creator_info (``str``, *optional*):
            Author information. don't know what kind

        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
    """
    characters: List[CharShort]
    username: str
    name: str
    num_following: int
    num_followers: int
    avatar_file_name: str | None
    subscription_type: str
    bio: str | None
    creator_info: str | None