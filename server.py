# Brian Lesko 12/16/2023

import socket
import streamlit as st 
import customize_gui # streamlit GUI modifications
gui = customize_gui.gui()

def server():
    gui.clean_format()
    gui.about(text = "Receive data from another computer using TCP network protocol")
    st.title("Server app")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.1.124', 12345))  # Replace '0.0.0.0' with the server's IP address
    server.listen() # wait for client connections

    st.write("Waiting for connection...")
    client_socket, client_address = server.accept()
    st.write(f"Connected to {client_address}")
    status = st.empty()

    while True:
        try: # if the connection is established
            with status: st.write("Waiting for messages...")
            message = client_socket.recv(1024).decode()
            if message: 
                st.write(f"Client: {message}")
                reply = f'Received: {message}'
                client_socket.sendall(reply.encode())

        except: # if the connection is lost
            st.write("Client disconnected")
            client_socket.close()
            server.close()
            break

server()