import socket
import threading
import time
from player import Player
from game import Game
from queue import Queue

def player_thread(conn, ip, name):
    pass

def authentication(conn, ip):
    try:
        data = conn.recv(2048)
    except Exception as e:
        print("[EXCEPTION] ", e)
    threading.Thread(target=player_thread, args=(ip))

def connection_thread():
    server = ""
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen()
    print("Waiting for a connection, Server Started")

    while True:
        conn, addr = s.accept()
        print("[CONNECT] New connection!")

        authentication(addr)


if __name__ == "__main__":
    connection_thread()
