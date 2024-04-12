from characterai import aiocai
import asyncio

token = 'YOUR TOKEN'

async def main():
    client = aiocai.Client(token)

    char = input('CHAR: ')
    
    new = await client.chat1.new_chat(char)

    while True:
        text = input('YOU: ')

        message = await client.chat1.send_message(
            new.id, new.tgt, text
        )

        print(f'{message.author}: {message.text}')

asyncio.run(main())