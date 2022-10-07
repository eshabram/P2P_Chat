from socket import *
import socket as s
import time

serverName = '10.0.0.1' # h2 ip # 10.0.0.1
serverPort = 12000
clientSocket = s.socket(s.AF_INET, s.SOCK_DGRAM)
timeout = 1.0
min_rtt = 1.0
max_rtt = -1.0
avg_rtt = 0.0
count_rtt = 0
packet_loss = 0.0
a = .125
b = .25
sample_rtt = 0.0
estimated_rtt = 0.0
dev_rtt = 0.0

# ping and wait for response or timeout
for i in range(10):
    message = 'Ping' + str(i + 1)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    time_sent = time.time()  # store the time message was sent
    try:
        clientSocket.settimeout(timeout)
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        time_recv = time.time()  # store time for message received
        sample_rtt = (time_recv - time_sent) * 1000
        rttString = str(sample_rtt)
        avg_rtt += sample_rtt

        # calculation for EstimatedRTT and Deviation
        if count_rtt < 1:
            estimated_rtt = sample_rtt
            dev_rtt = sample_rtt/2
        else:
            estimated_rtt = (1 - a) * estimated_rtt + a * sample_rtt
            dev_rtt = (1 - b) * dev_rtt + b * abs(sample_rtt - estimated_rtt)

        # find min and max
        if sample_rtt < min_rtt:
            min_rtt = sample_rtt
        if sample_rtt > max_rtt:
            max_rtt = sample_rtt

        print("Ping {}: sample_rtt = {:.3f} ms, estimated_rtt = {:.3f} ms, dev_rtt = {:.3f} ms".format(
              i+1, sample_rtt, estimated_rtt, dev_rtt))
        count_rtt += 1

        # calc timeout for next transmission
        timeout = estimated_rtt + 4 * dev_rtt
        print("Estimated: {}".format(estimated_rtt))
        print('Dev_rtt: {}'.format(dev_rtt))
    # catch timeout and record that a packet was lost
    except TimeoutError as e:
        print("Ping " + str(i + 1) + ": Request Timed out")
        packet_loss += 1.0
        continue

avg_rtt /= count_rtt
packet_loss = packet_loss / 10 * 100

print("Summary values:")
print('min_rtt: = {:.3f} ms'.format(min_rtt))
print('max_rtt: = {:.3f} ms'.format(max_rtt))
print('avg_rtt: = {:.3f} ms'.format(avg_rtt))
print('Packet Loss: = {:.2f}% '.format(packet_loss))
print('Timeout Interval: {:.3f} ms'.format(timeout))
clientSocket.close()
