import socket
import threading
from cryptography.fernet import Fernet

# Load AES key
key = open("secret.key", "rb").read()
cipher = Fernet(key)

server_ip = input("Enter server IP: ")
username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, 9999))

# Send username encrypted
client.send(cipher.encrypt(username.encode()))

def receive_messages():
    while True:
        try:
            encrypted = client.recv(1024)
            msg = cipher.decrypt(encrypted).decode()
            print("\n" + msg)
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

print("\nType messages normally.")
print("To DM someone use: /dm username message")

while True:
    text = input()
    encrypted = cipher.encrypt(text.encode())
    client.send(encrypted)

