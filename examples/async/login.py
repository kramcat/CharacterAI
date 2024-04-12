from characterai import aiocai, sendCode, authUser
import asyncio

async def main():
    email  = input('Enter your email: ')

    code = sendCode(email)

    link = input('Enter the link: ')

    token = authUser(link, email)

    info = await aiocai.get_me(token=token)

    print(info)

asyncio.run(main())