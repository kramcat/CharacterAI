###########
Quick Start
###########

To better understand how the library works, let's take a simple example of a conversation between a user and a character

I recommend using AioCAI instead of PyCAI when working with asynchronous libraries

First, you need to create a skeleton for your project. In PyCAI, this involves simply importing the library

.. tab:: AioCAI

    .. code-block::

        from characterai import aiocai
        import asyncio

        async def main():
            # YOUR CODE

        asyncio.run(main())

.. tab:: PyCAI

    .. code-block::

        from characterai import pycai

        # YOUR CODE

At the beginning of the code, we will ask the user for the character ID

.. code-block::

    char = input('CHAR: ')

And now you need to create a class :obj:`~characterai.aiocai.client.aiocai.Client`, which will be the main class you will be working with all the time

The required argument is `token`, you can find out about the rest on the class page itself

.. code-block::

    client = aiocai.Client('TOKEN')


After that, we collect information about our account through :obj:`~characterai.aiocai.methods.account.Account.get_me`, It's necessary to create a new chat that requires an author ID

.. tab:: AioCAI

    .. code-block::

        me = await client.get_me()

.. tab:: PyCAI

    .. code-block::

        me = client.get_me()

And now, let's move on to the chat. Once upon a time, c.ai had only an old version of the chat that worked via HTTPS. The new version (chat2) works via WebSockets, which means you need to maintain a connection with the server. In Python, this is done using context managers. For more information, please see the following object: `~characterai.aiocai.methods.utils.WSConnect`

.. tab:: AioCAI

    .. code-block::

        async with await client.connect() as chat:
            # YOUR CODE

.. tab:: PyCAI

    .. code-block::

        with client.connect() as chat:
            # YOUR CODE

Now, we will create a new chat and communicate directly within it. The function will always return 2 variables: information about the new chat and a welcoming message

After that, we will immediately display the greeting message for the character. If you do not wish to have this message displayed in new chats, you can set ``greeting=False`` in the function, and it will only return ``new``

.. tab:: AioCAI

    .. code-block::

        new, answer = await chat.new_chat(
            char, me.id
        )

.. tab:: PyCAI

    .. code-block::

        new, answer = chat.new_chat(
            char, me.id
        )

And in the chat itself, which will run continuously, immediately show the input from a user's message

.. code-block::

    while True:
        text = input('YOU: ')

        # YOUR CODE

After that, we receive a message and see the character's answer

.. tab:: AioCAI

    .. code-block::

        message = await chat.send_message(
            char, new.chat_id, text
        )

        print(f'{message.name}: {message.text}')

.. tab:: PyCAI

    .. code-block::

        message = chat.send_message(
            char, new.chat_id, text
        )

        print(f'{message.name}: {message.text}')

This information is enough to give you a basic understanding of the library. You can also find examples in the `examples <https://github.com/kramcat/CharacterAI/tree/main/examples>`_ folder on GitHub

For more information, please refer to the documentation. Before using a function or asking a question, make sure to read the documentation and use the search