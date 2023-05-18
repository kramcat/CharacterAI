# 💬 CharacterAI
[![Tag](https://img.shields.io/badge/chat-telegram-blue?style=flat&logo=Telegram)](https://t.me/characterapi)
![Tag](https://img.shields.io/github/license/kramcat/CharacterAI)
[![Downloads](https://static.pepy.tech/badge/characterai/month)](https://pepy.tech/project/characterai)

An unofficial API for Character AI for Python using Playwright

If you have any questions or just want to chat about character.ai, go to [Telegram](https://t.me/characterapi) chat

## 💻 Installation
```bash
pip install characterai
```

## 🔐 Get TOKEN
For using library, you should get token
1. Log in on character.ai
2. Go to `Network` tab in DevTools and refresh page
3. Search `/dj-rest-auth/auth0/`
4. Copy `key` value

## 🔐 Get CHAR
This is a character ID, it's very easy to get it
1. Open any chat
2. Copy `char` value from URL

## 📙 Example
#### Chatting
Simple program for chatting with character

##### Sync
```Python
from characterai import pyCAI

client = pyCAI('TOKEN')

while True:
    message = input('You: ')
    data = client.chat.send_message('CHAR', message, wait=True)
    print(f"{data['src_char']['participant']['name']}: {data['replies'][0]['text']}")
```
##### Async
```Python
import asyncio
from characterai import pyAsyncCAI

async def main():
    client = pyAsyncCAI('TOKEN')
    await client.start(headless=True)

    while True:
        message = input('You: ')
        data = await client.chat.send_message('CHAR', message, wait=True)
        print(f"{data['src_char']['participant']['name']}: {data['replies'][0]['text']}")

asyncio.run(main())
```

## 📚 Functions
### user
For information about the user, namely about you via a token, the answer is json
```python
user.info()
user.posts()
user.followers()
user.following()
```
### character
For character information, the answer is json
```python
character.trending()
character.recommended()
character.categories()
character.get_info('CHAR')
```
### chat
To work with the chat, `get_history` answer is json
```python
chat.get_history('CHAR')
chat.send_message('CHAR', 'YOUR MESSAGE')
```

## ⭐️ Features
- The only library for character.ai
- Asynchronous
- So easy to use

## ⚠️ Disclaimer
This library is written by a beginner in python, if you have any problems, write to me in [Telegram](https://t.me/kramcat)

