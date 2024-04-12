from characterai import aiocai, sendCode, authUser
import asyncio

async def main():
    email  = input('Enter your email: ')

    code = sendCode(email)

    link = input('Enter the link: ')

    token = authUser(link, email)

    print(f'YOUR TOKEN: {token}')

asyncio.run(main())
