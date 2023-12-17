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
    server.listen() # wait for client connections

    st.write("Waiting for connection...")
    client_socket, client_address = server.accept()
    st.write(f"Connected to {client_address}")

    if client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) == 0: # if the connection is established
        message = client_socket.recv(12345).decode()
        if message: 
            st.write(f"Client: {message}")
            reply = st.chat_input("Reply: ")
            client_socket.send(reply.encode())

    client_socket.close()
    server.close()

main()