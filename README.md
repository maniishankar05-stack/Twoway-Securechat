# SecureChat – Encrypted Multi-Client Chat Application

SecureChat is a Python-based encrypted chat application that enables multiple users to communicate securely in real time. It uses AES (Fernet) encryption to protect all messages and supports multiple clients at once using TCP sockets and threading. Users can choose unique usernames, broadcast messages to everyone, or send private direct messages (DMs) to specific users.

---

## 🔐 Features

- AES Encrypted Messaging (Fernet)
- Multi-Client Support using threading
- Username system
- Private Direct Messages with `/dm username message`
- Server Broadcast (admin messages)
- Real-time communication
- Socket stability using SO_REUSEADDR

---

## 📂 Project Structure
SecureChat/
│
├── SecureServer.py
├── SecureClient.py
├── keygen.py
├── secret.key
└── README.md

## ⚙️ Setup Instructions

### 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

### 2. Install dependencies

pip install cryptography

### 3. Generate encryption key
python3 keygen.py

---

## ▶️ Run the Server
python3 SecureServer.py

## ▶️ Run the Clientpython3 SecureClient.py
Enter server IP: 127.0.0.1
Enter your username:

---

## 💬 Private Messaging

Use:
/dm username message
---

## 🔒 Security Notes

- Do not share `secret.key` publicly
- Use a secure network
- AES encryption protects all messages

---

## 📜 License
MIT License

## ✨ Author
Developed by Mani Shankar
