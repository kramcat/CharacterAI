from datetime import datetime
from pydantic import BaseModel
from typing import Any, List, Optional

from .other import Avatar

class Anonymous(BaseModel):
    username: str = 'ANONYMOUS'

class Guest(BaseModel):
    username: str
    id: int
    account: Optional[Any] = None 
    is_staff: bool = False
    subscription: Optional[int] = None
    is_human: bool = True
    name: str
    email: Optional[str] = None
    hidden_characters: list
    blocked_users: list

class Profile(BaseModel, Avatar):
    """Your account info

    Parameters:
        name (``str``):
            Your name
        
        avatar_type (``str``):
            Avatar status, uploaded or not
        
        avatar_file_name (``str``, *optional*):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
        
        onboarding_complete (``bool``):
            For pop-up banners (?)
        
        mobile_onboarding_complete (``int``, *optional*):
            For mobile pop-up banners (?)
        
        bio (``str``, *optional*):
            Account description
        
        username (``str``):
            Public user nickname
        
        id (``str``):
            ID аккаунта, также ``author_id``
        
        first_name (``str``, *optional*):
            Account email
        
        is_staff (``bool``):
            Is the account an employee of the service
        
        subscription (``int``, *optional*):
            Subscription type
        
        is_human (``bool``):
            Is the account a human
        
        email (``str``):
            Your email
        
        needs_to_acknowledge_policy (``str``):
            Should the user agreement be accepted
        
        suspended_until (:py:obj:`~datetime.datetime`, *optional*):
            Account lockout end date
        
        hidden_characters (List of ``str``):
            Hidden characters
        
        blocked_users (List of ``str``):
            Blocked users
    """
    name: Optional[str] = None
    avatar_type: Optional[str] = None
    onboarding_complete: bool
    avatar_file_name: str | None
    mobile_onboarding_complete: int | None
    bio: str | None
    username: str
    id: int
    first_name: str | None
    is_staff: bool
    subscription: Optional[dict] = None
    is_human: bool
    email: str
    needs_to_acknowledge_policy: bool
    suspended_until: datetime | None
    hidden_characters: List[str]
    blocked_users: List[str]

class Persona(BaseModel, Avatar):
    """Информация о вашей персоне

    Parameters:
        external_id (``str``):
            Persona ID
        
        title (``str``):
            Persona title
        
        name (``str``):
            Persona name
        
        visibiility (``str``):
            Persona visibility
        
        copyable (``bool``):
            Can other users copy a persona
        
        greeting (``str``):
            Persona greeting (?)
        
        description (``str``):
            Persona description
        
        identifier (``str``):
            Persona ID
        
        avatar_file_name (``str``):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
        
        songs (``list``):
            Songs list (?)
        
        img_gen_enabled (``bool``):
            Can a persona generate pictures (?)
        
        base_img_prompt (``str``):
            Basic prompt for generating pictures (?)
        
        img_prompt_regex (``str``):
            Regex for a picture prompt (?)
        
        strip_img_prompt_from_msg (``str``):
            Remove the prompt from the message (?)
        
        definition (``str``):
            Persona definition
        
        default_voice_id (``str``):
            Default voice ID (?)
        
        starter_prompts (``Any``):
            Prompts for a start (?)
        
        comments_enabled (``bool``):
            Can comment on the persona (?)
        
        categories (``list``):
            Persona categories (?)
        
        user__username (``str``):
            User name
        
        participant__name (``str``):
            Person's name, same as ``name``
        
        participant__user__username (``str``):
            Persona ID
        
        num_interactions (``str``):
            Number of interactions with the person (?)
        
        voice_id (``str``):
            Voice ID (?)
    """
    external_id: str
    title: str
    name: str
    visibility: str
    copyable: bool
    greeting: str
    description: str
    identifier: str
    avatar_file_name: str
    songs: list
    img_gen_enabled: bool
    base_img_prompt: str
    img_prompt_regex: str
    strip_img_prompt_from_msg: bool
    definition: str
    default_voice_id: str
    starter_prompts: Any
    comments_enabled: bool
    categories: list
    user__username: str
    participant__name: str
    participant__user__username: str
    num_interactions: int
    voice_id: str

class PersonaShort(BaseModel, Avatar):
    """Короткая информация о вашей персоне

    Parameters:
        external_id (``str``):
            Persona ID
        
        title (``str``, *optional*):
            Persona title
        
        greeting (``str``):
            Persona greeting (?)
        
        description (``str``, *optional*):
            Persona description
        
        definition (``str``):
            Persona definition
        
        avatar_file_name (``str``):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
        
        visibiility (``str``):
            Persona visibility
        
        copyable (``bool``):
            Can other users copy a persona
        
        participant__name (``str``):
            Person's name, same as ``name``
        
        participant__num_interactions (``str``):
            Number of interactions with the person (?)
        
        user__id (``int``):
            User ID, and also ``author_id``
        
        user__username (``str``):
            User name
        
        img_gen_enabled (``bool``):
            Can a persona generate pictures (?)
        
        default_voice_id (``str``, *optional*):
            Default voice ID (?)
        
        is_persona (``bool``):
            Is the object a person
    """
    external_id: str
    title: str | None
    greeting: str
    description: str | None
    definition: str
    avatar_file_name: str | None
    visibility: str
    copyable: bool
    participant__name: str
    participant__num_interactions: int
    user__id: int
    user__username: str
    img_gen_enabled: bool
    default_voice_id: str | None
    is_persona: bool
