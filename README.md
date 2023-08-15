# 💬 CharacterAI
![Tag](https://img.shields.io/github/license/kramcat/CharacterAI)
[![Downloads](https://static.pepy.tech/badge/characterai/month)](https://pepy.tech/project/characterai)

An unofficial API for Character AI for Python using Playwright

### Discord Server
If you have any questions/problems/suggestions or you just want to talk about AI and CharacterAI - welcome to my new Discord server

[**discord.gg/CZdQWzMV**](https://discord.gg/CZdQWzMV)

 ᅠ 

## 💻 Installation
```bash
pip install characterai
```
If you don't have Playwright installed, it will install automatically. But installing Playwright via pip is not enough, you need to install browsers
```bash
python -m playwright install
```
Also, if you have Linux, you will need to install additional packages
```bash
python -m playwright install-deps
```

 ᅠ 

## 📚 Documentation
The library has [documentation](https://pycai.gitbook.io/welcome/)! It says everything about this library

 ᅠ 

## 🔑 Get Token
DO NOT SHARE IT
The token is needed for authorization and operation of requests from your account
1. Open DevTools in your browser
2. Go to Storage -> Local Storage -> char_token
3. Copy `value`

 ᅠ 

## 📙 Example
```Python
from characterai import PyCAI

client = PyCAI('TOKEN')
client.start()

char = input('Enter CHAR: ')

chat = client.chat.get_chat(char)

participants = chat['participants']

if not participants[0]['is_human']:
    tgt = participants[0]['user']['username']
else:
    tgt = participants[1]['user']['username']

while True:
    message = input('You: ')

    data = client.chat.send_message(
        chat['external_id'], tgt, message
    )

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    print(f"{name}: {text}")
```

 ᅠ 

## ⚠️ Issues
First, you should add `headless=False` in `client.start()` and describe what happens in the browser and take screenshot of the browser
Also, you should have a screenshot of your error and code
Describe how to cause an error, when the error is called, how often, whether it was before, etc.
You can write about the error in Github Issues, and you can also write to Discord server
