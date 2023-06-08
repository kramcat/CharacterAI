import asyncio
from characterai import PyAsyncCAI

async def main():
    client = PyAsyncCAI('TOKEN')
    await client.start()

    history = await client.chat.get_history('CHAR')

    for h in history['messages']:
        name = h['src_char']['participant']['name']
        text = h['text']

        print(f'{name}: {text}')

asyncio.run(main())