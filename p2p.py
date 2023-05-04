"""
This is a P2P chat script that functions as both client and server.
It utilizes threading to synchronize between the two. It is currently
only usable in a static network where the packets make it to their destination.
"""

import socket
import threading
from mininet.log import info, error
import time
import select


HOST = ''  # Listen on all interfaces
PORT = 8080  # Arbitrary port number
sem1 = threading.Semaphore(1)


class static:  # a home for the static variables
    dest = None
    flag = False
    track = 0


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))

    print(f'Server listening on {HOST}:{PORT}')

    while True:
        try:
            client_socket, address = server_socket.recvfrom(1024)

            if client_socket.decode() == 'ACK':
                print('\033[33m*Message Confirmed*\033[0m')
                static.flag = False
                # sem1.acquire()
                # static.track += 1
                # sem1.release()
                continue

            static.dest = address[0]
            print(f'\033[31m\n*****From:{address[0]}: {client_socket.decode()}\033[0m')
            # send an ACK
            ack_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ack_socket.sendto(b'ACK', (static.dest, PORT))
            ack_socket.close()

            # start new response thread
            if not static.flag:
                client_thr = threading.Thread(target=start_client)
                client_thr.start()
        except socket.error as e:
            error(f'Error accepting client connection: {e}\n')


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            if static.dest is None:
                sem1.acquire()
                static.dest = '10.0.0.' + input('Choose Station (enter an int 1-n): ')
                sem1.release()
            try:
                client_socket.settimeout(3.0)
                while static.flag:
                    continue
            except TimeoutError as e:
                print

            print('\033[32m' + 'Enter your message: ' + '\033[0m', end='')
            message = input()
            static.flag = True
            client_socket.sendto(message.encode(), (static.dest, PORT))
        except socket.error as e:
            error(f'Error sending message: {e}\n')


if __name__ == '__main__':

    print('Starting server...')
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    print('Starting client...')
    client_thread = threading.Thread(target=start_client)
    client_thread.start()
