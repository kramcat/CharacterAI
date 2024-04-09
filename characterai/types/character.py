from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from .other import Avatar

class Promts(BaseModel):
    phrases: list

class Character(BaseModel, Avatar):
    """Character info

    Parameters:
        external_id (``str``):
            Character ID
        
        title (``str``, *optional*):
            Short character description
        
        name (``str``):
            Character name
        
        visibility (``str``):
            Character visibility (everyone, you or from link)
        
        copyable (``bool``):
            Can other users copy a character
        
        greeting (``str``):
            Character greeting (first message)
        
        description (``str``, *optional*):
            Character description
        
        identifier (``str``):
            Character ID
        
        avatar_file_name (``str``):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
        
        songs (``list``):
            List of songs (?)
        
        img_gen_enabled (``bool``):
            Can the character generate pictures
        
        base_img_prompt (``str``, *optional*):
            Basic prompt for generating pictures
        
        img_prompt_regex (``str``, *optional*):
            Regex for a picture prompt
        
        strip_img_prompt_from_msg (``str``):
            Remove the prompt from the message
        
        definition (``str``):
            Character definition
        
        default_voice_id (``str``):
            Default voice ID
        
        starter_prompts (``Promts``, *optional*):
            Prompts for start (?)
        
        comments_enabled (``bool``):
            Can comment on the character (?)
        
        user__username (``str``):
            Author nickname
        
        participant__name (``str``):
            Character name, same as ``name``
        
        participant__user__username (``str``):
            Character ID
        
        participant__num_interactions (``int``, *optional*):
            Number of interactions (chats) with the character
        
        voice_id (``str``, *optional*):
            Voice ID
        
        usage (``str``, *optional*):
            How well the character is used (?)

        upvotes (``int``, *optional*):
            Number of likes
    """
    external_id: str
    title: str | None
    name: str
    visibility: str
    copyable: bool
    greeting: str
    description: str | None
    identifier: str
    avatar_file_name: str | None
    songs: list
    img_gen_enabled: bool
    base_img_prompt: str | None
    img_prompt_regex: str | None
    strip_img_prompt_from_msg: bool
    default_voice_id: str | None
    starter_prompts: Optional[Promts] = None
    comments_enabled: bool
    user__username: str
    participant__name: str
    participant__num_interactions: Optional[int] = None
    participant__user__username: str
    voice_id: str | None
    usage: Optional[str] = None
    upvotes: Optional[int] = None

class CharShort(BaseModel, Avatar):
    """Краткая информация о персонаже

    Parameters:
        external_id (``str``):
            Character ID
        
        title (``str``, *optional*):
            Short character description
        
        name (``str``, *optional*):
            Character name
        
        greeting (``str``):
            Character greeting (first message)
        
        description (``str``, *optional*):
            Character description
        
        avatar_file_name (``str``):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
        
        visibility (``str``, *optional*):
            Character visibility (everyone, you or from link)
        
        copyable (``bool``, *optional*):
            Can other users copy a character
        
        participant__name (``str``):
            Character name, same as ``name``
        
        user__id (``int``, *optional*):
            Author ID (?)
        
        user__username (``str``):
            Author nickname
        
        img_gen_enabled (``bool``):
            Can the character generate pictures
        
        participant__num_interactions (``int``, *optional*):
            Number of interactions (chats) with the character
        
        default_voice_id (``str``, *optional*):
            Default voice ID
        
        upvotes (``int``, *optional*):
            Number of likes
        
        max_last_interaction (:py:obj:`~datetime.datetime`, *optional*):
            Maximum time of the last interaction with the character (?)
    """
    external_id: str
    title: str | None
    description: Optional[str | None] = None
    greeting: str
    avatar_file_name: str | None
    visibility: Optional[str] = None
    copyable: Optional[str | bool] = None
    participant__name: str
    user__id: Optional[int] = None
    user__username: str
    img_gen_enabled: bool
    participant__num_interactions: Optional[int] = None
    default_voice_id: Optional[str] = None
    upvotes: Optional[int] = None
    max_last_interaction: Optional[datetime] = None

class Categories(BaseModel):
    """List of categories
    
    Parameters:
        animals (List of :obj:`~characterai.types.character.CharShort`):
            Animals bots

        anime (List of :obj:`~characterai.types.character.CharShort`):
            Anime bots
        
        anime_game (List of :obj:`~characterai.types.character.CharShort`):
            Anime game bots
        
        chinese (List of :obj:`~characterai.types.character.CharShort`):
            Chinese bots
        
        comedy (List of :obj:`~characterai.types.character.CharShort`):
            Comedy bots
        
        discussion (List of :obj:`~characterai.types.character.CharShort`):
            Discussion bots

        famous (List of :obj:`~characterai.types.character.CharShort`):
            Famous bots
        
        game (List of :obj:`~characterai.types.character.CharShort`):
            Game bots
        
        games (List of :obj:`~characterai.types.character.CharShort`):
            Games bots
        
        helpers (List of :obj:`~characterai.types.character.CharShort`):
            Helpers bots
        
        image (List of :obj:`~characterai.types.character.CharShort`):
            Image bots
        
        movies (List of :obj:`~characterai.types.character.CharShort`):
            Movies bots
        
        philosophy (List of :obj:`~characterai.types.character.CharShort`):
            Philosophy bots
        
        politics (List of :obj:`~characterai.types.character.CharShort`):
            Politics bots
        
        religion (List of :obj:`~characterai.types.character.CharShort`):
            Religion bots
        
        vtuber (List of :obj:`~characterai.types.character.CharShort`):
            VTuber bots
    """
    animals: List[CharShort] = Field(validation_alias='Animals')
    anime: List[CharShort] = Field(validation_alias='Anime')
    anime_game: List[CharShort] = Field(validation_alias='Anime Game Characters')
    books: List[CharShort] = Field(validation_alias='Books')
    chinese: List[CharShort] = Field(validation_alias='Chinese')
    comedy: List[CharShort] = Field(validation_alias='Comedy')
    discussion: List[CharShort] = Field(validation_alias='Discussion')
    famous: List[CharShort] = Field(validation_alias='Famous People')
    game: List[CharShort] = Field(validation_alias='Game Characters')
    games: List[CharShort] = Field(validation_alias='Games')
    helpers: List[CharShort] = Field(validation_alias='Helpers')
    image: List[CharShort] = Field(validation_alias='Image Generating')
    movies: List[CharShort] = Field(validation_alias='Movies & TV')
    philosophy: List[CharShort] = Field(validation_alias='Philosophy')
    politics: List[CharShort] = Field(validation_alias='Politics')
    religion: List[CharShort] = Field(validation_alias='Religion')
    vtuber: List[CharShort] = Field(validation_alias='VTuber')