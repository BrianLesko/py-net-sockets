# Brian Lesko 12/16/2023

import socket
import streamlit as st 
import customize_gui # streamlit GUI modifications
from ethernet import ethernet as eth
gui = customize_gui.gui()

def main():
    gui.clean_format()
    gui.about(text = "Chat to another computer using TCP network protocol")
    st.title("Client app")
    
    with st.spinner("Waiting for connection..."):
        connected_indicator = st.empty()
        client = eth("client",'192.168.1.124', 12345)# Replace 'server_ip_address' with the server's IP address
        client.connect()  # Replace 'server_ip_address' with the server's IP address

    message = st.chat_input("You:", key="user_input")

    while client.is_connected():
        with connected_indicator: st.write("Connected to server")
        reply = client.send_and_receive("Hello World")

        """ 
        if message: 
            st.chat_message("User").write(f"You: {message}")
            reply = client.send_and_receive(message)
            with st.chat_message("Server"):
                st.write(f"Server: {reply}") """

    client.disconnect()
        
main()
