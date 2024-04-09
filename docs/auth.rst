#############
Authorization
#############

To work with the library, you need a token. You can get it through authorization by email and as a guest

.. warning::

    Please do not show your token to anyone. It can only be regenerated if you delete your account and create a new one

Log In Via Email
================

This code asks the user for their email address and sends them a confirmation link. The user then enters the link they received in their email and is given a token for their account

.. code-block::

    from characterai import aiocai, sendCode, authUser
    import asyncio

    async def main():
        email = input('YOUR EMAL: ')

        code = sendCode(email)

        link = input('CODE IN MAIL: ')
        
        token = authUser(link, email)
    
        info = await aiocai.get_me(token=token)

        print(info)

    asyncio.run(main())

Log In As a Guest
=================

Guests can't chat

.. code-block::

    from characterai import aiocai, authGuest
    import asyncio
    
    async def main():
        client = aiocai.Client(authGuest())

        info = await client.get_me(token=token)
    
        print(info)
    
    asyncio.run(main())

After logging in, you can find account information by using the :obj:`~characterai.aiogram.methods.account.Account.get_me` method. If you are a guest, no information will be displayed

Alternative Auth Methods
========================

In addition to creating the ``Client`` class, you have the flexibility to work with both the class and individual functions.

Context Manager
---------------

When you create a ``Client`` class, its session will always remain active. If you don't use the library in your code later, you will need to manually close the session using the ``close()`` method

And with this option, you won't need to manually close the session, as it will automatically close when the code finishes executing or an error occurs

.. code-block::

    async with aiocai.Client('TOKEN') as client:
        print(await client.get_me())

Via Function
------------

Sometimes you only need to use 1 function from the library or another token, in that case, you can use the function without creating a new client and just specify the token

.. code-block::

    await aiocai.get_me(token='TOKEN')