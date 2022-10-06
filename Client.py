from socket import *
import time

serverName = 'master2'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
t_out = 1.0
min_rtt = 1
max_rtt = 0
avg_rtt = 0
count_rtt = 0
packet_loss = 0.0
a = .125
b = .25
estimated_rtt = 0
dev_rtt = 0

# ping and wait for response or timeout
for i in range(10):
    message = 'Ping' + str(i + 1)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    time_sent = time.time()  # store the time message was sent
    try:
        clientSocket.settimeout(t_out)
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        time_recv = time.time()  # store time for message received
        rtt = (time_recv - time_sent) * 1000
        rttString = str(rtt)
        print("\nMesg sent: " + message)
        print("Mesg rcvd: " + modifiedMessage.decode())
        print("PONG {} RTT: {}ms".format(str(i + 1), rttString))
        avg_rtt += rtt
        count_rtt += 1

        # calculation for EstimatedRTT
        estimated_rtt = (1 - a) * estimated_rtt + a * rtt

        # calc for deviation Rtt
        dev_rtt = (1 - b) * dev_rtt + b * abs(rtt - estimated_rtt)

        # check for min and max value
        if rtt < min_rtt:
            min_rtt = rtt
        elif rtt > max_rtt:
            max_rtt = rtt

    except TimeoutError as e:
        print("\nMesg sent: " + message)
        print("No Mesg rcvd")
        print("PONG " + str(i + 1) + " Request Timed out")
        packet_loss += 1.0
        continue

# put some RTT math HERE
avg_rtt /= count_rtt
a = 0.125
b = 0.25
packet_loss = packet_loss / 10 * 100

timeout = estimated_rtt + 4 * dev_rtt
# estimated_rtt = (1 - a)*
# dev_rtt =

print('\nMin RTT:         {} ms'.format(min_rtt))
print('Max RTT:         {} ms'.format(max_rtt))
print('Avg RTT:         {} ms'.format(avg_rtt))
print('Packet Loss:     {} '.format(packet_loss))
# print('Estimated RTT:   {} ms'.format())
# print('Dev RTT:         {}'.format())
# print('Timeout Interval:{}'.format())
clientSocket.close()
