# Brian Lesko 12/16/2023

import socket
import streamlit as st 
import customize_gui # streamlit GUI modifications
from ethernet import ethernet as eth
gui = customize_gui.gui()

def main():
    gui.clean_format()
    gui.about(text = "Chat to another computer using TCP network protocol")
    st.title("Server app")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.1.124', 12345))  # Replace '0.0.0.0' with the server's IP address
    server.listen()

    st.write("Waiting for connection...")
    client_socket, client_address = server.accept()
    st.write(f"Connected to {client_address}")

    message = client_socket.recv(12345).decode()
    while message != 'exit':  # Exit condition
        if message: 
            st.write(f"Client: {message}")
            reply = st.chat_input("Reply: ")
            if reply:
                client_socket.send(reply.encode())
        message = client_socket.recv(12345).decode()

    client_socket.close()
    server.close()

main()