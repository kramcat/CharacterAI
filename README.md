<img src="https://raw.githubusercontent.com/kramcat/CharacterAI/main/docs/images/full_logo.png" alt="logo">

[![Downloads](https://img.shields.io/pepy/dt/characterai?style=flat-square)](https://pepy.tech/project/characterai)
[![License](https://img.shields.io/pypi/l/characterai?style=flat-square)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/kramcat/characterai?style=flat-square)](https://github.com/kramcat/characterai)
[![Discord](https://img.shields.io/discord/1120066151515422772?style=flat-square)](https://discord.com/invite/ZHJe3tXQkf)

Welcome to the documentation for a synchronous/asynchronous unofficial library for CharacterAI using [curl_cff](https://github.com/yifeikong/curl_cffi)

### 💻 Installation
```bash
pip install -U characterai
```

### ⚠️ Warning
This version of the library is in alpha version, there may be bugs and errors. The library was developed without the participation of Character AI developers or their knowledge. To work with the library you need to know how to work with [asyncio](https://docs.python.org/3/library/asyncio.html)

### 🔥 Features
- Supports logging in via email or as a guest
- Does not use web browsers like: Pypeeter, Playwright, etc.
- Supports uploading/downloading pictures
- Has detailed documentation
- Uses Pydantic
- Asynchronous

### 📙 Simple Example
You need an account to use the library. To find out your token, you must [log in through the library](https://docs.kram.cat/auth.html)
```python
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
```

### 📚 Documentation
The documentation contains all the detailed information about functions and types. If you have any questions, first of all read whether there is an answer in the documentation

**[docs.kram.cat](https://docs.kram.cat)**

### 👥 Community
If you have any questions about our library or would like to discuss CharacterAI, LLM, or Neural Networks topics, please visit our Discord channel

**[discord.gg/ZHJe3tXQkf](https://discord.com/invite/ZHJe3tXQkf)**

### 📝 TODO List
- [ ] Character voice work
- [ ] Community tab support
- [ ] Add logging
- [ ] Group chat support
- [ ] Improved work with uploading pictures

### 💵 Support
TON - `EQCSMftGsV4iU2b9H7tuEURIwpcWpF_maw4yknMkVxDPKs6v`
<br> BTC - `bc1qghtyl43jd6xr66wwtrxkpe04sglqlwgcp04yl9`
<br> ETH - `0x1489B0DDCE07C029040331e4c66F5aA94D7B4d4e`
<br> USDT (TRC20) - `TJpvALv9YiL2khFBb7xfWrUDpvL5nYFs8u`

You can contact me via [Telegram](https://t.me/kramcat) or [Discord](https://discordapp.com/users/480976972277874690) if you need help with parsing services or want to write a library. I can also create bots and userbots for Telegram
