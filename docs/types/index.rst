Types
=====

All available server response types. Created with Pydantic, so they should be used as classes

.. code-block::

    from characterai import aiocai

    user = await aiocai.get_me('TOKEN')

    print(user.username)

.. warning:
    You may have errors due to incorrect typing. Please report it on Github or Discord

Account
-------

.. currentmodule:: characterai.types.account

.. autosummary::
    :toctree: view
    :nosignatures:

    Profile
    Persona
    PersonaShort

Character
---------

.. currentmodule:: characterai.types.character

.. autosummary::
    :toctree: view
    :nosignatures:

    Character
    CharShort
    Categories

Chat V1
-------

.. currentmodule:: characterai.types.chat1

.. autosummary::
    :toctree: view
    :nosignatures:

    Message
    UserAccount
    User
    Participants
    Messages
    NewChat
    ChatHistory
    HisMessage
    HisMessages
    History
    Migrate

Chat V2
-------

.. currentmodule:: characterai.types.chat2

.. autosummary::
    :toctree: view
    :nosignatures:

    Candidate
    BotAnswer
    TurnData
    ChatData
    History


Recent
------

.. currentmodule:: characterai.types.recent

.. autosummary::
    :toctree: view
    :nosignatures:

    Room
    Chat

User
----

.. currentmodule:: characterai.types.user

.. autosummary::
    :toctree: view
    :nosignatures:

    User


Other
-----

.. currentmodule:: characterai.types.other

.. autosummary::
    :toctree: view
    :nosignatures:

    QueryChar
    Image
    Avatar
    Voice