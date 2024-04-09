Methods
=======

All available API methods. All methods listed here are bound to the ``Client`` instance, except chat1, it is called through the class

.. code-block::

    from characterai import pycai

    client = pycai.Client('TOKEN')

    client.get_me()

    client.chat1.get_history('CHAR_ID')


Character
---------

.. currentmodule:: characterai.aiocai.methods.characters.Characters

.. autosummary::
    :toctree: view
    :nosignatures:

    get_char
    upvoted
    get_category
    get_recommended
    get_trending
    create_char
    update_char


Account
-------

.. currentmodule:: characterai.aiocai.methods.account.Account

.. autosummary::
    :toctree: view
    :nosignatures:

    get_me
    edit_account
    get_personas
    create_persona
    get_persona
    delete_persona
    followers
    following
    characters


Chat V1
-------

.. currentmodule:: characterai.aiocai.methods.chat1.ChatV1

.. autosummary::
    :toctree: view
    :nosignatures:

    get_histories
    get_history
    get_chat
    new_chat
    next_message
    delete_message
    send_message
    migrate


Chat V2
-------

.. currentmodule:: characterai.aiocai.methods.chat2.ChatV2

.. autosummary::
    :toctree: view
    :nosignatures:

    get_histories
    get_history
    get_chat
    new_chat
    next_message
    delete_message
    send_message
    edit_message
    pin


Chats
-----

.. currentmodule:: characterai.aiocai.methods.chats.Chats

.. autosummary::
    :toctree: view
    :nosignatures:

    search
    create_room

Recent
------

.. currentmodule:: characterai.aiocai.methods.recent.Recent

.. autosummary::
    :toctree: view
    :nosignatures:

    get_recent_chats
    get_recent_rooms
    get_recent

Users
-----

.. currentmodule:: characterai.aiocai.methods.users.Users

.. autosummary::
    :toctree: view
    :nosignatures:

    get_user

Other
-----

.. currentmodule:: characterai.aiocai.methods.other.Other

.. autosummary::
    :toctree: view
    :nosignatures:

    get_voices
    create_image
    upload_image
    ping