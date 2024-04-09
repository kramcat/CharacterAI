from characterai import aiocai
import asyncio

async def main():
    char = input('CHAR ID: ')

    client = aiocai.Client('TOKEN')

    me = await client.get_me()

    async with await client.connect() as chat:
        new, answer = await chat.new_chat(
            char, me.id
        )

        print(f'{answer.name}: {answer.text}')
        
        while True:
            text = input('YOU: ')

            message = await chat.send_message(
                char, new.chat_id, text
            )

            print(f'{message.name}: {message.text}')

asyncio.run(main())