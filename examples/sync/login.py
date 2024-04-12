from characterai import pycai, sendCode, authUser

email  = input('Enter your email: ')

code = sendCode(email)

link = input('Enter the link: ')

token = authUser(link, email)

print(f'YOUR TOKEN: {token}')
