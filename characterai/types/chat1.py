from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from .other import Avatar

class Replies(BaseModel):
    """Message info

    Parameters:
        text (``str``):
            Message text

        uuid (``str``):
            Message UUID

        id (``int``):
            Message ID
    """
    text: str
    uuid: str
    id: int

class Participant(BaseModel):
    name: str

class SrcChar(BaseModel, Avatar):
    """Character info in the message

    Parameters:
        name (``str``, *property*):
            Character name
        
        avatar_file_name (``str``):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
    """
    participant: Participant
    avatar_file_name: Optional[str] = None

    @property
    def name(self):
        return self.participant.name

class Message(BaseModel):
    """Информация о сообщении типа chat1

    Parameters:
        replies (List of :obj:`~characterai.types.chat1.Replies`):
            Message object
        
        src_char (:obj:`~characterai.types.SrcChar`):
            Character info
        
        is_final_chunk (``bool``):
            Whether the message (chunk) is the last in generation
        
        last_user_msg_id (``int``):
            ID последнего сообщения пользователя
        
        last_user_msg_uuid (``str``):
            UUID of the last user message

        id (``int``, *property*):
            Message ID

        text (``str``, *property*):
            Message text
        
        uuid (``str``, *property*):
            Message UUID
        
        author (``str``, *property*):
            Author name
    """
    replies: List[Replies]
    src_char: SrcChar
    is_final_chunk: bool
    last_user_msg_id: int
    last_user_msg_uuid: str

    @property
    def id(self):
        return self.replies[0].id

    @property
    def text(self):
        return self.replies[0].text

    @property
    def uuid(self):
        return self.replies[0].uuid

    @property
    def author(self):
        return self.src_char.participant.name

class UserAccount(BaseModel, Avatar):
    """Your account

    Parameters:
        name (``str``):
            Your name
        
        avatar_type (``str``):
            Avatar status (uploaded or not)
        
        onboarding_complete (``bool``):
            For pop-up banners (?)
        
        mobile_onboarding_complete (``int``, *optional*):
            For mobile pop-up banners (?)

        avatar_file_name (``str``):
            Path to the avatar on the server
        
        avatar (:obj:`~characterai.types.other.Avatar`):
            Avatar info
    """
    name: str
    avatar_type: str
    onboarding_complete: bool
    avatar_file_name: str
    mobile_onboarding_complete: int

class User(BaseModel):
    """Object in chat

    Parameters:
        username (``str``):
            Your nickname or character ID
        
        id (``bool``):
            Object ID
        
        first_name (``str``):
            Your email or character name
        
        account (:obj:`~characterai.types.chat1.UserAccount`, *optional*):
            Your account information
        
        is_staff (``bool``):
            Is the object an employee of the service
    """
    username: str
    id: int
    first_name: str
    account: Optional[UserAccount] = None
    is_staff: bool

class Participants(BaseModel):
    """Objects in chat

    Parameters:
        user (:obj:`~characterai.types.chat1.User`):
            Object information
        
        is_human (``bool``):
            Is a human
        
        name (``str``):
            Object name
        
        num_interactions (``int``):
            Total number of chats
    """
    user: User
    is_human: bool
    name: str
    num_interactions: int

class Messages(BaseModel):
    """Сообщения в чате

    Parameters:
        deleted (``bool``):
            Has the message been deleted
        
        id (``int``):
            Message ID
        
        text (``str``):
            Message text
        
        image_prompt_text (``str``):
            Picture generation promt
        
        image_rel_path (``str``):
            URL path to the picture
        
        is_alternative (``str``):
            Is the message alternatively generated
        
        responsible_user__username (``str``):
            Nickname of the character's author
        
        src__is_human (``bool``):
            Is the message from the object a person
        
        src__name (``str``):
            Character name
        
        src__user__username (``str``):
            Nickname of the character's author
        
        src_char (:obj:`~characterai.types.SrcChar`):
            Character object
    """
    deleted: bool
    id: int = Field(validation_alias='id ')
    image_prompt_text: str
    image_rel_path: str
    is_alternative: bool
    responsible_user__username: str
    src__character__avatar_file_name: str
    src__is_human: bool
    src__name: str
    src__user__username: str
    src_char: SrcChar
    text: str
    
class NewChat(BaseModel):
    """New chat info

    Parameters:
        title (``str``):
            Chat title (?)
        
        participants (List of :obj:`~characterai.types.chat1.Participants`):
            Objects in chat
        
        external_id (``str``):
            Chat ID
        
        last_interaction (:py:obj:`~datetime.datetime`):
            Date of last message
        
        created (:py:obj:`~datetime.datetime`):
            Chat creation date
        
        type (``str``):
            Chat type (chat or room)
        
        description (``str``):
            Chat description (?)
        
        speech (``str``):
            WebRTC voice
        
        status (``str``):
            Status of function execution
        
        has_more (``bool``):
            Are there any more chat messages
        
        messages (List of :obj:`~characterai.types.chat1.Messages`):
            Messages list
        
        id (``str``):
            Chat ID
        
        tgt (``str``, *property*):
            Old character ID type
    """
    title: str
    participants: List[Participants]
    external_id: str
    created: datetime
    last_interaction: datetime
    type: str
    description: str
    speech: str
    status: str
    has_more: bool
    messages: List[Messages]

    id: str = Field(
        validation_alias='external_id'
    )

    @property
    def tgt(self):
        return self.participants[1].user.username

class Avatars(BaseModel, Avatar):
    name: str

    avatar_file_name: Optional[str] = \
    Field(validation_alias='user__account__avatar_file_name') or \
    Field(validation_alias='character__avatar_file_name')

class ChatHistory(BaseModel):
    """Chat history

    Parameters:
        title (``str``):
            Chat name (for rooms)
        
        participants (List of :obj:`~characterai.types.chat1.Participants`):
            Objects in chat
        
        external_id (``str``):
            Chat ID
        
        last_interaction (:py:obj:`~datetime.datetime`):
            Date of last message
        
        created (:py:obj:`~datetime.datetime`):
            Chat creation date
        
        type (``str``):
            Chat type (chat or room)
        
        avatars (List of :obj:`~characterai.types.chat1.Avatars`):
            Avatars of objects in chat
        
        room_img_gen_enabled (``bool``):
            Can the pictures be generated
    """
    title: str
    participants: List[Participants]
    external_id: str
    created: datetime
    last_interaction: datetime
    type: str
    description: str
    avatars: List[Avatars]
    room_img_gen_enabled: bool

class HisMessage(BaseModel):
    """Message in the chat history list

    Parameters:
        id (``str``):
            Message ID
        
        uuid (``str``):
            Message UUID
        
        text (``str``):
            Message text
        
        src (``str``):
            User message ID
        
        tgt (``str``):
            Old character ID type
        
        is_alternative (``bool``, *optional*):
            Is the message alternatively generated
        
        image_rel_path (``str``):
            Path to the picture, if available
        
        image_prompt_text (``str``):
            Promt for the generated image
        
        deleted (``bool``, *optional*):
            Has the message been deleted
        
        src__name (``str``):
            User name
        
        src__user__username (``str``):
            User nickname
        
        src__is_human (``bool``, *optional*):
            Is the user a human/account
        
        src__character__avatar_file_name (``str``, *optional*):
            URL link to avatar
        
        src_char (:obj:`~characterai.types.SrcChar`):
            Character info
        
        responsible_user__username (``str``, *optional*):
            I don't know what it is
    """
    id: int
    uuid: str
    text: str
    src: str
    tgt: str
    is_alternative: Optional[bool] = None
    image_rel_path: str
    image_prompt_text: str
    deleted: Optional[bool] = None
    src__name: str
    src__user__username: str
    src__is_human: Optional[bool] = None
    src__character__avatar_file_name: Optional[str] = None
    src_char: SrcChar
    responsible_user__username: Optional[str] = None
    
class History(BaseModel):
    """Chat history info

    Parameters:
        external_id (``str``):
            Chat ID
        
        last_interaction (:py:obj:`~datetime.datetime`):
            Date of last message
        
        created (:py:obj:`~datetime.datetime`):
            Chat creation date
        
        msgs (List of :obj:`~characterai.types.chat1.HisMessage`):
            Messages list
    """
    external_id: str
    last_interaction: datetime
    created: datetime
    msgs: List[HisMessage]

class HisMessages(BaseModel):
    """Chat message list

    Parameters:
        messages (List of :obj:`~characterai.types.chat1.HisMessage`):
            Messages
        
        next_page (``int``):
            Next page number 
        
        has_more (``bool``):
            Is there any more messages 
    """
    messages: List[HisMessage]
    next_page: int
    has_more: bool

class Migrate(BaseModel):
    """Info about migrating from chat1 to chat2

    Parameters:
        id (``str``):
            New chat ID

        create_time (:py:obj:`~datetime.datetime`):
            Date of migration creation 

        last_update (:py:obj:`~datetime.datetime`):
            Date of data update

        status (``str``):
            Migration status

        properties (``str``):
            Additional migration options (?)
    """
    id: str = Field(validation_alias='migrationId')
    create_time: datetime = Field(validation_alias='createTime')
    last_update: datetime = Field(validation_alias='lastUpdateTime')
    status: str
    properties: str