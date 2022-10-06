from socket import *
import time

serverName = 'master2'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
timeout = 1.0
min_rtt = 1
max_rtt = 0
avg_rtt = 0
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

        # calculation for EstimatedRTT
        if count_rtt < 1:
            estimated_rtt = sample_rtt
        else:
            estimated_rtt = (1 - a) * estimated_rtt + a * sample_rtt

        # calc for deviation Rtt
        dev_rtt = (1 - b) * dev_rtt + b * abs(sample_rtt - estimated_rtt)

        print("Ping {}: sample_rtt = {:.3f} ms, estimated_rtt = {:.3f} ms, dev_rtt = {:.3f} ms".format(
              i, sample_rtt, estimated_rtt, dev_rtt))
        count_rtt += 1

        # calc timeout for next transmission
        timeout = estimated_rtt + 4 * dev_rtt
        # check for min and max value
        if sample_rtt < min_rtt:
            min_rtt = sample_rtt
        elif sample_rtt > max_rtt:
            max_rtt = sample_rtt

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
