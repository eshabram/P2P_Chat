# Server.py
# We will need the following module to generate randomized lost packets
import random
from socket import socket, AF_INET, SOCK_DGRAM

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('master2', 12000))
print("Waiting for Client....")
i = 1
while True:
    # Generate random number5 in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    # If rand is less is than 4, we consider the packet lost and do not respond
    modifiedMessage = message.decode().upper();
    if rand < 4:
        continue
    print('\nPING {} Received'.format(i))
    print('Mesg rcvd:' + message.decode())
    print('Mesg sent: ' + modifiedMessage)
    # Otherwise, the server responds
    serverSocket.sendto(modifiedMessage.encode(), address)
    i += 1

