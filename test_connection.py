import json
import socket

class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "96.126.118.234"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.sendall(self.name.encode())
            return json.loads(self.client.recv(2048))
        except Exception as e:
            self.disconnect(e)

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())
            return_data = ""
            while True:
                last = self.client.recv(1024).decode()
                try:
                    if last[-1] == ".":
                        return_data += last[:-1]
                        break
                except:
                    pass

                return_data += last
                
            keys = [key for key in data.keys()]
            return json.loads(return_data)[str(keys[0])]
        except socket.error as e:
            self.disconnect(e)

    def disconnect(self, msg):
        print("[EXCEPTION] Disconnected from server:", msg)
        self.client.close()

n = Network("Zach")

print(n.send({3:[]}))
print(n.send({5:[]}))
