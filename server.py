# encoding: utf-8
# Echo服务器端
from socketserver import TCPServer as TCP, StreamRequestHandler as SRH

HOST = ''
PORT = 21567
ADDR = (HOST, PORT)

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
            return cls.instance

class MyRequestHandler(SRH):
    def handle(self):
        print('...connected from:', self.client_address)
        st = ('%s' % (self.rfile.readline().decode())).encode()
        db=Database()
        print(db.basicOperation(st))
        st1 = (db.basicOperation(st)).encode()
        self.wfile.write(st1)

class Database(object):
    __metaclass__=Singleton
    def __init__(self):
        self.database={}
    def __set__(self, newstr):
        self.database[newstr[1]]=newstr[2].rstrip('\'')
        print(self.database)
        return ('TRUE')
    def __get__(self, newstr):
        print(newstr[1].rstrip('\''))
        st=self.database.get(newstr[1].rstrip('\''),'The data you input is not in the database!')
        return st
    def __delete__(self, newstr):
        print(newstr[1].rstrip('\''))
        if newstr[1].rstrip('\'') in self.database:
            del self.database[newstr[1].rstrip('\'')]
            st=1
        else:
            st='NONE'
        return st
    def basicOperation(self, newstr):
        st=str(newstr.strip()).split()
        if st[0]=="b'set":
            return self.__set__(st)
        else:
            if st[0]=="b'get":
                return self.__get__(st)
            else:
                if st[0]=="b'delete":
                    return self.__delete__(st)
                else:
                    return('Illegal Input!')

tcpServ = TCP(ADDR, MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()
