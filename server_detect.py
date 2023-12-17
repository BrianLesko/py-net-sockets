import socket
import streamlit as st
import customize_gui  # streamlit GUI modifications
from ethernet import ethernet as eth
gui = customize_gui.gui()

def main():
    gui.clean_format()
    gui.about(text="Chat to another computer using TCP network protocol")
    st.title("Client app")

    # Broadcasting to discover servers
    broadcast_address = "255.255.255.0"  # Broadcast address for the local network
    broadcast_port = 12345  # Broadcast port number
    discovery_message = "SERVER_DISCOVERY"

    # Create a UDP socket for broadcasting
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send a broadcast message to discover servers
    broadcast_socket.sendto(discovery_message.encode(), (broadcast_address, broadcast_port))

    # Receive responses from servers
    servers = []
    while True:
        try:
            broadcast_socket.settimeout(1)  # Set a timeout for receiving responses
            data, server_address = broadcast_socket.recvfrom(1024)
            servers.append(server_address[0])
        except socket.timeout:
            break

    # Display discovered servers
    if servers:
        selected_server = st.selectbox("Select a server", servers)
        if selected_server:
            client = eth("client", selected_server, 12345)
            client.connect()

            message = st.chat_input("You: ")
            if message:
                reply = client.send_and_receive(message)
                if reply is None:
                    st.write("No reply")
                else:
                    st.write(f"Server: {reply}")

            client.close()
    else:
        st.write("No servers found on the network")

    # Close the broadcast socket
    broadcast_socket.close()

main()