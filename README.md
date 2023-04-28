# 💬 CharacterAPI
An unofficial API for Character AI for Python using Playwright

## Installation
```bash
pip3 install CharacterAPI
```

## Get TOKEN
For using library, you should get token
1. Log in on character.ai
2. Go to `Network` tab in DevTools and refresh page
3. Search `/dj-rest-auth/auth0/`
4. Copy `key` value

## Get CHAR
This is a character ID, it's very easy to get it
1. Open any chat
2. Copy `char=` value from URL

## Example
#### Chatting
Simple program for chatting with character
```Python
from CharacterAPI import pyCAI

token = 'TOKEN'
character = 'CHAR'

client = pyCAI(token)

while True:
    send = input('You: ')
    print(f'Hawks: {client.chat.send_message(character, send)}')
```

## Functions
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
To work with the chat, `get_history` the answer is json
```python
chat.get_history('CHAR')
chat.send_message('CHAR', 'YOUR MESSAGE')
```

## Features
- The only library for character.ai
- Asynchronous
- So easy to use

## Disclaimer
this library is written by a beginner in python, if you have any problems, write to me in [Telegram](t.me/kramcat)

