import socket
import threading
from cryptography.fernet import Fernet

# Load AES key
key = open("secret.key", "rb").read()
cipher = Fernet(key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 9999))
server.listen(5)

print("🚀 Server is running... Waiting for clients...")

clients = {}  # conn -> username

def send_encrypted(conn, message):
    conn.send(cipher.encrypt(message.encode()))

def broadcast(message, sender=None):
    for conn in clients:
        if conn != sender:
            send_encrypted(conn, message)

def private_message(target_username, message, sender_username):
    for conn, uname in clients.items():
        if uname == target_username:
            send_encrypted(conn, f"[DM from {sender_username}] {message}")
            return True
    return False

def handle_client(conn, addr):
    username = cipher.decrypt(conn.recv(1024)).decode()
    clients[conn] = username

    print(f"[JOIN] {username}")
    broadcast(f"{username} joined the chat!")

    while True:
        try:
            encrypted_msg = conn.recv(1024)
            if not encrypted_msg:
                break

            msg = cipher.decrypt(encrypted_msg).decode()
            print(f"[{username}] {msg}")

            # Private DM command
            if msg.startswith("/dm "):
                try:
                    # format: /dm username message
                    _, target, *dm_msg = msg.split()
                    dm_msg = " ".join(dm_msg)
                    success = private_message(target, dm_msg, username)
                    if not success:
                        send_encrypted(conn, f"User '{target}' not found.")
                except:
                    send_encrypted(conn, "Invalid DM format. Use: /dm username message")
                continue

            # Normal broadcast
            broadcast(f"{username}: {msg}", sender=conn)

        except:
            break

    print(f"[LEFT] {username}")
    broadcast(f"{username} left the chat.")
    conn.close()
    del clients[conn]

# Thread for server console input (server can send messages)
def server_console():
    while True:
        text = input()
        broadcast(f"[SERVER]: {text}")

threading.Thread(target=server_console, daemon=True).start()

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
