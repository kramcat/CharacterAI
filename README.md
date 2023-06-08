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

## 📙 Example
Simple code for chatting with character
```Python
from characterai import PyCAI

client = PyCAI('TOKEN')

while True:
    message = input('You: ')
    
    data = client.chat.send_message('CHAR', message)
    
    message = data['replies'][0]['text']
    name = data['src_char']['participant']['name']
    
    print(f"{name}: {message}")
```

## 📚 Documentation
The library has [documentation](https://pycai.gitbook.io/welcome/)! It says everything about this library

## ⭐️ Features
- The only library for character.ai
- Asynchronous
- So easy to use

## ⚠️ Disclaimer
This library is written by a beginner in python, if you have any problems, write to me in [Telegram](https://t.me/kramcat)

