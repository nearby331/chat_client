import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import configparser

config = configparser.ConfigParser()
config.read("client.ini")

conf = config["Main"]

init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

client_color = random.choice(colors)

SERVER_HOST = conf["host"]
SERVER_PORT = int(conf["port"])
separator_token = conf["separator"]
token = conf["token"]

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
try:
    s.connect((SERVER_HOST, SERVER_PORT))
except:
    print("[*] Incorrect host or port!")
    exit

s.send(f"Client{separator_token}{token}".encode())
print("[+] Connected.")

name = input("Enter your name: ")

def listen_for_messages():
    while True:
        try:
            message = s.recv(1024).decode()
        except:
            print("[*] Closed")
            break
        print("\n" + message)
    exit

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send = input()
    if to_send.lower() == 'q':
        break
    date_now = datetime.now().strftime('%H:%M') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    try:
        s.send(to_send.encode())
    except:
        print("[*] Closed")
        break

s.close()