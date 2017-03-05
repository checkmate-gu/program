#Echo服务器端
from socketserver import TCPServer as TCP, StreamRequestHandler as SRH  
  
HOST = ''  
PORT = 21567  
ADDR = (HOST, PORT)  
  
class MyRequestHandler(SRH):  
    def handle(self):  
        print('...connected from:', self.client_address)  
        self.wfile.write(('%s' %(self.rfile.readline().decode())).encode())  
  
tcpServ = TCP(ADDR, MyRequestHandler)  
print('waiting for connection...')  
tcpServ.serve_forever()  