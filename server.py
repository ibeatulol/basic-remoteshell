import socket
from colorama import Fore, Style, init

init(autoreset=True)

banner = r"""
                         _            _          _ _ 
                         | |          | |        | | |
 _ __ ___ _ __ ___   ___ | |_ ___  ___| |__   ___| | |
| '__/ _ \ '_ ` _ \ / _ \| __/ _ \/ __| '_ \ / _ \ | |
| | |  __/ | | | | | (_) | ||  __/\__ \ | | |  __/ | |
|_|  \___|_| |_| |_|\___/ \__\___||___/_| |_|\___|_|_|
                                                      
                                                      
"""

print(banner)
print(Fore.RED + "by beat" + Style.RESET_ALL)

SERVER_IP = "127.0.0.1"  # beat here- 127.0.0.1 is local all your going to do is connect to yourself
PORT = 4444

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_IP, PORT))

s.listen(1)
print(f"[+] Listening on {SERVER_IP or '0.0.0.0'}:{PORT}")

while True:
    client, addr = s.accept()
    print(f"[+] Client connected from {addr}")

    client.send(b"Connected to server.\n")

    while True:
        cmd = input(">>> ").strip()
        if not cmd:
            continue

        client.send(cmd.encode())

        if cmd.lower() in ["quit", "exit", "q", "x"]:
            print("[*] Closing client connection...")
            client.close()
            break

        result = client.recv(4096).decode(errors="ignore")
        print(result)

    choice = input("Wait for new client (y/n)? ").strip().lower() or "y"
    if choice in ["n", "no"]:
        print("[*] Shutting down server.")
        break

s.close()
