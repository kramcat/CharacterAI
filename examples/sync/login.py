from characterai import pycai, sendCode, authUser

email  = input('Enter your email: ')

code = sendCode(email)

link = input('Enter the link: ')

token = authUser(link, email)

info = pycai.get_me(token=token)

print(info)