from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

from .other import Avatar

class Participant(BaseModel, Avatar):
    name: str
    avatar_file_name: str

class Room(BaseModel):
    """Информация о комнатах с персонажами

    Parameters:
        external_id (``str``):
            Chat ID
        
        title (``str``):
            Room name
        
        description (``str``):
            Room description
        
        participants (List of ``Participant``):
            Characters in the room [name, avatar_file_name]
        
        img_gen_enabled (``bool``):
            Will it be possible to generate pictures
    """
    external_id: str
    title: str
    description: str
    participants: List[Participant]
    img_gen_enabled: bool

class Name(BaseModel):
    ko: Optional[str] = None
    ru: Optional[str] = None
    ja_JP: Optional[str] = None
    zh_CN: Optional[str] = None

class CharacterTranslations(BaseModel):
    name: Name

class Chat(BaseModel, Avatar):
    """Информация о чате

    Parameters:
        chat_id (``str``):
            Chat ID
        
        create_time (:py:obj:`~datetime`):
            Chat creation time

        creator_id (``str``):
            ID of the user who created the chat
        
        character_id (``str``):
            Character ID
        
        state (``str``):
            Chat state
        
        type (``str``):
            Chat type
        
        visibility (``str``):
            Chat visibility (everyone, you or from link)
        
        character_name (``str``):
            Character name
        
        character_visibility (``str``):
            Character visibility (everyone, you or from link)
        
        character_translations (``CharacterTranslations``):
            Translations of character information
            [ko, ru, ja_JP, zh_CN]
        
        default_voice_id (``str``, *optional*):
            Default voice ID
        
        avatar_file_name (``str``):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
    """
    chat_id: str
    create_time: datetime
    creator_id: str
    character_id: str
    state: str
    type: str
    visibility: str
    character_name: str
    character_visibility: str
    character_translations: CharacterTranslations
    default_voice_id: Optional[str] = None
    avatar_file_name: str = Field(
        validation_alias='character_avatar_uri'
    )