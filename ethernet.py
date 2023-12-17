# Brian Lesko
# Ethernet communication class

import socket
import pandas as pd

class ethernet:

    def __init__(self, name, IP, PORT, SUBNETMASK = "MASK"):
        self.name = name
        self.IP = IP
        self.PORT = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        messages = []
        try: 
            self.s.connect((self.IP, self.PORT))
            messages.append(f'The connection with *{self.name}* established.')
            self.connected = True
        except socket.error as e:
            messages.append(f'Sorry, the connection with *{self.name}* was not established.')
            messages.append(e)
        return messages
    
    def disconnect(self): 
        self.s.close()
        return f"The connection with *{self.name}* was closed."

    def send_and_receive(self, command):
        bytes = command.encode()
        self.s.sendall(bytes)
        response = self.s.recv(1024) # Max amount of bytes to receive
        if response:
            return response.decode()
        else:
            return None 
    
    def to_df(self):
        df = pd.DataFrame({'name': [self.name], 'ipv4': [self.IP], 'port': [self.PORT]})
        return df
    
    # For the keyence instance of an ethernet connection 
    def prime_print(self,print):
        command_2 = 'PR' + ',1' + '\r' # set the program number
        command = 'SB' + '\r' # we acquire the system status to check if we are ready to print
        command_3 = 'BK' + ',1,0,' + print + '\r' # change the string to print
        commands = [command, command_2, command_3]
        responses = []
        messages = []
        for command in commands:
            message = f"Sending to *{self.name}*: {command}"
            response = self.send_and_receive(command)
            message2 = f"The response from *{self.name}* is: "
            messages.append(message + "\n" + message2)
            responses.append(response)
        return responses, messages
    
    @classmethod
    def from_excel(cls, excel_file_name):
        # To create a list of ethernet objects from an excel file
        ethernets = []
        data_types = {
            'ipv4': str,
            'port': int,
            'subnetmask': str
        }
        external_connections = pd.read_excel(excel_file_name, index_col=None)
        external_connections = external_connections.astype(data_types)
        for i in range(len(external_connections)):
            name = external_connections['name'][i]
            IP = external_connections['ipv4'][i]
            PORT = external_connections['port'][i]
            ethernet = cls(name, IP, PORT)
            ethernets.append(ethernet)
        return ethernets
    
    # WIP - need to test this
    def get_local_ip():
        # This will only work on Linux
        import subprocess
        IP= subprocess.run(["hostname", "-I"],stdout=subprocess.PIPE,text=True).stdout
        return IP

    def get_subnet_mask():
        netmask = "255.255.255.0"
        return netmask
    
    def check_connection_compatibility(self):
        if self.get_local_ip().split('.')[0:3] == self.IP.split('.')[0:3]:
            response = 'Your computer and *{self.name}* are ready to connect.'
            errors = False
        else: 
            response = 'Your host computer and *{self.name}* cannot communicate.' + "\n" + """
                - Are the IP addresses in the same range? 
                - Is the printer connected on the same ethernet as the computer?
                - Do the port and IP specified above match the printer settings?
                """
            errors = True
        return response, errors
