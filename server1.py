# encoding: utf-8
# Echo服务器端
from socket import  *

HOST = ''
PORT = 21567
BUFSIZ=1024
ADDR = (HOST, PORT)

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
            return cls.instance

class ForDatabase(object):
    pass

class Database(ForDatabase):
    __metaclass__ = Singleton
    database={}
    def __set__(self, newstr):
        self.database[newstr[1]]=newstr[2]
        return ('TRUE')
    def __get__(self, newstr):
        st=self.database.get(newstr[1],'The data you input is not in the database!')
        return st
    def __delete__(self, newstr):
        if newstr[1] in self.database:
            del self.database[newstr[1]]
            st='the data has already been deleted'
        else:
            st='NONE'
        return st
    def basicOperation(self, newstr):
        st=str(newstr.strip()).split()
        if st[0]=="set":
            return self.__set__(st)
        else:
            if st[0]=="get":
                return self.__get__(st)
            else:
                if st[0]=="delete":
                    return self.__delete__(st)
                else:
                    return('Illegal Input!')

class Haset(ForDatabase):
    __metaclass__=Singleton
    database = {}

    def __set__(self, newstr):
        self.database[newstr[2]] = newstr[3]
        return ('TRUE')

    def __get__(self, newstr):
        st = self.database.get(newstr[2], 'The data you input is not in the hashset!')
        return st

    def __delete__(self, newstr):
        if newstr[2] in self.database:
            del self.database[newstr[2]]
            st = 'the data has already been deleted'
        else:
            st = 'The data you want to delete is not in the hashset'
        return st

    def __keys__(self, newstr):
        return str(self.database.keys()).lstrip('dict_keys(').rstrip(')')

    def basicOperation(self, newstr):
        st = str(newstr.strip()).split()
        print(st)
        if st[0] == "hset":
            return self.__set__(st)
        else:
            if st[0] == "hget":
                return self.__get__(st)
            else:
                if st[0] == "hdel":
                    return self.__delete__(st)
                else:
                    if st[0]=="hkeys":
                        return self.__keys__(st)
                    else:
                        return('Illegal Input!')

server=socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
server.listen(5)

while True:
    print('waiting for connection...')
    client, addr=server.accept()
    stt = str('%s' % (client.recv(BUFSIZ)))
    print(stt)
    print(len(stt))
    print(type(stt))
    if stt == "b'1\\r\\n'":
        db=Database()
        print('db seted 1')
    else:
        if stt=="b'2\\r\\n'":
            db=Haset()
            print('db seted 2')
        else:
            print('noting been executed')
    while True:
        data=client.recv(BUFSIZ).decode()
        st1 = (db.basicOperation(data))
        if not data:
            break
        client.send(('%s'%st1).encode())
    client.close()
server.close()