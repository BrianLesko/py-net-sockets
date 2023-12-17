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
    connected_indicator = st.empty()

    try: 
        with connected_indicator: st.write("Not connected to server")
        st.session_state.client.is_connected()
    except:
        with st.spinner("Waiting for connection..."):
            client = eth("client",'192.168.1.124', 12345)# Replace 'server_ip_address' with the server's IP address
            client.connect()  # Replace 'server_ip_address' with the server's IP address
            with connected_indicator: st.write("Connected to server")
            st.session_state.client = client

    message = st.chat_input("Type a message")
    if message: 
        st.write(f"You: {message}")
        reply = st.session_state.client.send_and_receive(message)
        if reply: 
            st.write(f'Server: {reply}' )
        else: 
                st.write("Server did Not reply")
        
main()
