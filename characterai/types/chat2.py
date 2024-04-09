from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Author(BaseModel):
    """Message author

    Parameters:
        author_id (``str``):
            Account ID

        name (``str``):
            User name

        is_human (``bool``, *option*):
            Is the author an account
    """
    author_id: str
    name: str
    is_human: Optional[bool] = None

class Editor(BaseModel):
    """Message editor

    Parameters:
        author_id (``str``):
            Account ID

        name (``str``, *optional*):
            User name
    """
    author_id: str
    name: Optional[str] = None

class TurnKey(BaseModel):
    chat_id: str
    turn_id: str

class Candidate(BaseModel):
    """Контент сообщения

    Parameters:
        candidate_id (``str``):
            Message ID
        
        create_time (:py:obj:`~datetime.datetime`):
            Date of message creation
        
        raw_content (``str``):
            Message text
        
        editor (:obj:`~characterai.types.chat2.Editor`):
            Information about who modified the message
        
        is_final (``bool``):
            Is this the last chunk of the message
        
        base_candidate_id (``str``):
            Date of message update
    """
    candidate_id: str
    create_time: datetime
    raw_content: str
    editor: Optional[Editor] = None
    is_final: bool
    base_candidate_id: Optional[str] = None

class BotAnswer(BaseModel):
    """Message object

    Parameters:
        text (``str``):
            Message text
        
        id (``str``):
            Message ID
        
        name (``str``):
            Sender's name
        
        turn_key (``TurnKey``):
            Message and chat ID [chat_id, turn_id]
        
        create_time (:py:obj:`~datetime.datetime`):
            Date of message creation
        
        last_update_time (:py:obj:`~datetime.datetime`):
            Date of message update
        
        state (``str``):
            Message state
        
        author (:obj:`~characterai.types.chat2.Author`):
            Message author
        
        candidates (List of :obj:`~characterai.types.chat2.Candidate`):
            Message content
        
        primary_candidate_id (``str``):
            Message ID (?)
    """
    @property
    def text(self):
        return self.candidates[0].raw_content

    @property
    def id(self):
        return self.candidates[0].candidate_id

    @property
    def name(self):
        return self.author.name
    
    turn_key: TurnKey
    create_time: datetime
    last_update_time: datetime
    state: str
    author: Author
    candidates: List[Candidate]
    primary_candidate_id: str

class TurnData(BaseModel):
    """Preview message

    Parameters:
        turn_key (``str``):
            Message ID
        
        create_time (:py:obj:`~datetime.datetime`):
            Date of message creation
        
        last_update_time (:py:obj:`~datetime.datetime`):
            Date of message update
        
        state (``str``):
            Message state
        
        author (:obj:`~characterai.types.chat2.Author`):
            Message author
        
        candidates (List of :obj:`~characterai.types.chat2.Candidate`):
            Message content
        
        primary_candidate_id (``str``):
            Message ID (?)
    """
    turn_key: TurnKey
    create_time: datetime
    last_update_time: datetime
    state: str
    author: Author
    candidates: List[Candidate]
    primary_candidate_id: str

class ChatData(BaseModel):
    """Chat info

    Parameters:
        chat_id (``str``):
            Chat ID
        
        create_time (:py:obj:`~datetime.datetime`):
            Date of message creation
        
        creator_id (``str``):
            Author ID
        
        character_id (``str``):
            Character ID
        
        state (``str``):
            Chat state
        
        type (``str``):
            Chat type
        
        visibility (``str``):
            Who can see the chat room
        
        preview_turns (List of :obj:`~characterai.types.chat2.TurnData`, *optional*):
            Message's preview
    """
    chat_id: str
    create_time: datetime
    creator_id: str
    character_id: str
    state: str
    type: str
    visibility: str
    preview_turns: Optional[List[TurnData]] = None

class Meta(BaseModel):
    next_token: str

class History(BaseModel):
    """Chat history

    turns (List of :obj:`~characterai.types.chat2.TurnData`):
        Message information

    meta (``Meta``):
        I don't know what it is, maybe someone could use it
    """
    turns: List[TurnData]
    meta: Meta