
######
AioCAI
######


.. image:: https://img.shields.io/pepy/dt/characterai?style=flat-square
    :target: https://pypi.org/project/characterai
    :alt: Total Downloads

.. image:: https://img.shields.io/pypi/l/characterai?style=flat-square
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/github/stars/kramcat/characterai?style=flat-square
    :target: https://github.com/kramcat/characterai
    :alt: Discord

.. image:: https://img.shields.io/discord/1120066151515422772?style=flat-square
    :target: https://discord.com/invite/ZHJe3tXQkf
    :alt: Stars


Welcome to the documentation for a synchronous/asynchronous unofficial library for CharacterAI using `curl_cffi <https://github.com/yifeikong/curl_cffi>`_


💻 Installation
---------------

.. code-block:: bash

    pip install -U characterai

.. warning::

    This version of the library is in alpha version, there may be bugs and errors. The library was developed without the participation of Character AI developers or their knowledge. To work with the library you need to know how to work with `asyncio <https://docs.python.org/3/library/asyncio.html>`_


🔥 Features
===========

- Supports logging in via email or as a guest
- Does not use web browsers like: Pypeeter, Playwright, etc.
- Supports uploading/downloading pictures
- Has detailed documentation
- Uses Pydantic
- Asynchronous


📙 Simple Example
-----------------
.. literalinclude::
    ../../examples/async/chat2.py


👥 Community
--------------
If you have any questions about our library or would like to discuss CharacterAI, LLM, or Neural Networks topics, please visit our Discord channel

`discord.gg/ZHJe3tXQkf <https://discord.com/invite/ZHJe3tXQkf>`_


📝 TODO List
------------

- Character voice work
- Community tab support
- Add logging
- Group chat support
- Improved work with uploading pictures


💵 Support
----------
| TON - ``UQBlGz8aw5tWaocR8gPppQe6SgTx-kkh5keInKtEzVOqPhdY``
| BTC - ``bc1qghtyl43jd6xr66wwtrxkpe04sglqlwgcp04yl9``
| ETH - ``0x1489B0DDCE07C029040331e4c66F5aA94D7B4d4e``
| USDT (TRC20) - ``TJpvALv9YiL2khFBb7xfWrUDpvL5nYFs8u``

You can contact me via `Telegram <https://t.me/kramcat>`_ or `Discord <https://discordapp.com/users/480976972277874690>`_ if you need help with parsing services or want to write a library. I can also create bots and userbots for Telegram


.. toctree::
    :hidden:
    :maxdepth: 3
    :caption: Getting Started

    starting
    auth

.. toctree::
    :hidden:
    :maxdepth: 3
    :caption: Working with API

    client
    methods/index
    types/index
    errors

.. toctree::
    :hidden:
    :maxdepth: 3
    :caption: More Info

    support
    qna
    changelog
