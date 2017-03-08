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

class Database(object):
    __metaclass__ = Singleton
    database={}
    def __set__(self, newstr):
        self.database[newstr[1]]=newstr[2].rstrip('\'')
        return ('TRUE')
    def __get__(self, newstr):
        st=self.database.get(newstr[1].rstrip('\''),'The data you input is not in the database!')
        return st
    def __delete__(self, newstr):
        if newstr[1].rstrip('\'') in self.database:
            del self.database[newstr[1].rstrip('\'')]
            st='the data has already been deleted'
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

class MyRequestHandler(SRH):
    def handle(self):
        print('...connected from:', self.client_address)
        st = ('%s' % (self.rfile.readline().decode())).encode()
        db = Database()
        st1 = (db.basicOperation(st)).encode()
        self.wfile.write(st1)

tcpServ = TCP(ADDR, MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()



