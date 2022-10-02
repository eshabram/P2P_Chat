from socket import *
import time

serverName = 'master2'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
t_out = 3.59710304346

# ping and wait for response or timeout
for i in range(10):
    message = 'Ping' + str(i+1)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    time_sent = time.time()  # store the time message was sent
    try:
        clientSocket.settimeout(t_out)
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        time_recv = time.time()  # store time for message received
        rtt = str(time_recv - time_sent)
        print("\nMesg sent: " + message)
        print("Mesg rcvd: " + modifiedMessage.decode())
        print("PONG {} RTT: {}ms".format(str(i+1), rtt[:13]))
    except TimeoutError as e:
        print("\nMesg sent: " + message)
        print("No Mesg rcvd")
        print("PONG " + str(i+1) + " Request Timed out")
        continue

# put some RTT math HERE

# print('\nMin RTT:         {} ms'.format())
# print('Max RTT:         {} ms'.format())
# print('Avg RTT:         {} ms'.format())
# print('Packet Loss:     {} ms'.format())
# print('Estimated RTT:   {} ms'.format())
# print('Dev RTT:         {}'.format())
print('Timeout Interval:{}'.format(t_out))
clientSocket.close()