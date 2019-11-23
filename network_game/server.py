import socket
from threading import *
import pickle


should_exit = False
connection_data = {}

class ClientConnection(Thread):
    def __init__(self, socket, client_address):
        Thread.__init__(self)
        self.socket = socket
        self.addr = client_address
        print("type of address:", type(client_address), str(client_address))
        connection_data[self.socket] = None
        self.start()

    def run(self):
        global should_exit
        while not should_exit:
            try:
                received = self.socket.recv(1024)
                unpickled = pickle.loads(received)
                if unpickled == 'quit':
                    del connections[self.socket]
                    del connection_data[self.socket]
                    print("client quit: ", self.addr)
                    break
                connection_data[self.socket] = unpickled
                to_send_obj = {}
                for sock, data in connection_data.items():
                    if sock != self.socket and data:
                        address = connections[sock]
                        to_send_obj[str(address)] = data
                self.socket.send(pickle.dumps(to_send_obj))

            except:
                should_exit = True

connections = {}
class SocketListenerServer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "192.168.1.28"
        port = 8000
        max_num_clients = 5
        aceptance_timeout = 1
        print ("Sever host = ", host)
        print ("Server port = ", port)
        serversocket.bind((host, port))
        serversocket.listen(max_num_clients)
        serversocket.settimeout(aceptance_timeout)
        global should_exit
        while not should_exit:
            try:
                clientsocket, client_address = serversocket.accept()
                connections[clientsocket] = client_address
                print("# of connections=", len(connections))
                ClientConnection(clientsocket, client_address)
            except:
                pass

sv = SocketListenerServer()
print ('server started and listening')
while True:
    str = input("type 'quit' to exit:")
    if str == 'quit':
        print("Existing now")
        should_exit = True
        exit(1)
