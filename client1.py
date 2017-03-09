# encoding: utf-8
# Echo客户端
from socket import *

HOST = '127.0.0.1'
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

class ChooseType(object):
    @staticmethod
    def ChooseWhatType():
        print('What kind of data structure you want to choose?')
        print('You can choose normal database as 1, hashset as 2, list as 3')
        t=input('input your number here:')
        print(t)
        typ = str(t).strip()
        if int(t) == 1:
            print("You must obey the following rules to input:")
            print('set data: set a 1')
            print('get data: get a')
            print('delete data: delete a')
            print('other input will not be executed!')
            client.send(('%s\r\n' % typ).encode())
        else:
            if int(t)==2:
                print("You must obey the following rules to input:")
                print('set data: hset hash a 1')
                print('get data: hget hash a')
                print('delete data: hdel hash a')
                print('get all keys: hkeys hash')
                print('other input will not be executed!')
                client.send(('%s\r\n' % typ).encode())
            else:
                if int(t)==3:
                    print("You must obey the following rules to input:")
                    print('set the last data: rpush a 1')
                    print('get the first data: lpush a 1')
                    print('delete the first data: lpop a')
                    print('delete the last data: rpop a')
                    print('get the list length:llen a')
                    print('get the data from a to b:lrange a 0 5')
                    print('other input will not be executed!')
                    client.send(('%s\r\n' % typ).encode())
                else:
                    print('Illegal input')

ChooseType().ChooseWhatType()

while True:
    data = input('input here:')
    if not data:
        break
    client.send(('%s\r\n' % data).encode())
    data = client.recv(BUFSIZE).decode()
    if not data:
        break
    print(data.strip())
client.close()