# DISCLAIMER:
# This is not an official library and is not coordinated with developers who may not like it.
# You may use the library for any purpose and modify it as you wish, 
# but you must be sure to include the name KRAMCAT as the original author

__version__ = '1.0.0a1'

from .aiocai.client import aiocai
from .pycai.client import pycai
from .auth import sendCode, authUser, authGuest