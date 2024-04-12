from characterai import pycai

token = 'YOUR TOKEN'

client = pycai.Client(token)

char = input('CHAR: ')

new = client.chat1.new_chat(char)

while True:
    text = input('YOU: ')

    message = client.chat1.send_message(
        new.id, new.tgt, text
    )

    print(f'{message.author}: {message.text}')