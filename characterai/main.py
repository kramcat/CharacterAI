from characterai import PyCAI

client = PyCAI('a5c2f69274c87103925b32bd67ed45cff0b15957')

char = input('Enter CHAR: ') .lower()

if char == 'father':
    char = 'uMnXQwm3ii7GGQUUExv4yfu4v_2_wYec4u-7K3H6Mbw'


chat = client.chat.get_chat(char)

participants = chat['participants']

if not participants[0]['is_human']:
    tgt = participants[0]['user']['username']
else:
    tgt = participants[1]['user']['username']

message = 'Hi'
while message.lower() !='end chat':

    data = client.chat.send_message(
        chat['external_id'], tgt, message
    )

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    print(f"{name}: {text}")
    message = input('You: ')