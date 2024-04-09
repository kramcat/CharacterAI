from .users import Users
from .characters import Characters
from .account import Account
from .other import Other
from .recent import Recent
from .chats import Chats
from .chat2 import ChatV2

class Methods(
    Users, Characters,
    Account, Recent,
    Chats, Other, ChatV2
):
    ...