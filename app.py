# Brian Lesko 12/16/2023

import socket
import streamlit as st 
import customize_gui # streamlit GUI modifications
from ethernet import ethernet as eth
gui = customize_gui.gui()

def main():
    gui.clean_format()
    gui.about(text = "Chat to another computer using TCP network protocol")
    st.title("Chat app using sockets")

    
    IPS = ['192.168.1.124']
    PORTS = 1025

    with st.chat_message("assistant"):
        IP = st.selectbox("Select IP address", IPS) 
        if IP: 
            eth1 = eth("PI", IP, PORTS)
            with st.spinner("Connecting..."):
                try:
                    messages = eth1.connect()
                    for message in messages:
                        st.write(message)
                except:
                    st.write("Connection failed")

    if eth1.connected: 
        message = st.chat_input("Enter message")
        if message: 
            response = eth1.send_and_receive(message)
            if response:
                st.write(response)
            else:
                st.write("No response")


main() 