# Brian Lesko 12/16/2023

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('server_ip_address', 12345))  # Replace 'server_ip_address' with the server's IP address

while True:
    message = input("You: ")
    client.send(message.encode())
    reply = client.recv(1024).decode()
    if not reply:
        break
    print(f"Server: {reply}")

client.close()
