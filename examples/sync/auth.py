from characterai import pycai

# Usually
client = pycai.Client('TOKEN')

print(client.get_me())

client.close()

# Via context manager
with pycai.Client('TOKEN') as client:
    print(client.get_me())

# Via the function
print(pycai.get_me(token='TOKEN'))