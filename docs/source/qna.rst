####################
Answers to Questions
####################

What's ``author_id``?
=====================

This is your account ID, needed to create a new chat in chat2. It can be found in :obj:`~characterai.aiocai.methods.account.Account.Account.get_me()`.

What's ``tgt``?
===============

This is an old character ID type, needed for chat1. You can get it in :obj:`~characterai.types.character.Character.Character.get_char` under ``identifier``.

What's the difference between chat1 and chat2?
==============================================

For the average user there are no significant differences except that you can't send pictures in chat2 (actually you can, the library allows it, but not on the site)

But on the server side there are huge differences. First of all, chat1 works via HTTPS requests, while chat2 works via WebSockets. Secondly, the requests and their responses are very different, and accordingly their logic is very different

chat2 is currently the newest version of chat2, hardly worth waiting for chat3

.. note::

    You can migrate chat1 to chat2 with :obj:`~characterai.aiocai.methods.chats.Chats.migrate`

What's the difference between AioCAI and PyCAI?
===============================================

AioCAI is the asynchronous version, PyCAI is the synchronous version

Both versions support the same types and methods, just in PyCAI you don't need to use ``asyncio`` and write ``await`` and ``async``