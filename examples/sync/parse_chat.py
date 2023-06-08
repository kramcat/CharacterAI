from characterai import PyCAI

client = PyCAI('TOKEN')

history = client.chat.get_history('CHAR')

for h in history['messages']:
    name = h['src_char']['participant']['name']
    text = h['text']

    print(f'{name}: {text}')