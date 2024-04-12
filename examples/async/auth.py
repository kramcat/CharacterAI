from characterai import aiocai
import asyncio

async def main():
    # Usually
    client = aiocai.Client('TOKEN')

    print(await client.get_me())

    await client.close()

    # Via context manager
    async with aiocai.Client('TOKEN') as client:
        print(await client.get_me())

    # Via the function
    print(await aiocai.get_me(token='TOKEN'))

asyncio.run(main())