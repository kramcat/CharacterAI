from characterai import pycai

char = input('CHAR ID: ')

client = pycai.Client('TOKEN')

me = client.get_me()

with client.connect() as chat:
    new, answer = chat.new_chat(
        char, me.id
    )

    print(f'{answer.name}: {answer.text}')

    while True:
        text = input('YOU: ')

        message = chat.send_message(
            char, new.chat_id, text
        )

        print(f'{message.name}: {message.text}')