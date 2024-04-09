######
Client
######

The main class for working with the library

It can also work as a context manager

.. code-block:: python

    async with aiocai.Client('TOKEN') as client:
        await client.get_me()

.. autoclass:: characterai.aiocai.client.aiocai.Client()

    .. autofunction:: characterai.aiocai.client.aiocai.Client.close