# Brian Lesko 12/16/2023
# Implements a client to send data to a server, it is built only on the socket and streamlit library

import socket
import streamlit as st 
import customize_gui # streamlit GUI modifications
from ethernet import ethernet as eth
gui = customize_gui.gui()

def client():
    gui.clean_format()
    gui.about(text = "Wirelessly send data to a computer using TCP network protocol")
    st.title("Client app")

    if 'client' not in st.session_state:
         st.session_state.client = eth("client",'192.168.1.124', 12345)
         st.session_state.client.connect()

    message = st.chat_input("Type a message")
    if message: 
        st.write(f"You: {message}")
        reply = st.session_state.client.send_and_receive(message)
        if reply: 
            st.write(f'Server: {reply}' )
        else: 
                st.write("Server did Not reply")
        
client()
