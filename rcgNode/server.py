#!/usr/bin/env python

import socket, select
import os
from recognition import image_recognition

imgcounter = 1
basename = "image%s.jpg"

# HOST = '128.163.232.64'
host_name = socket.gethostname()
host_addr = socket.gethostbyname(host_name)
print("Host name: %s" % host_name)
print("Host address: %s" % host_addr)
PORT = 6666

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host_addr, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)

while True:
    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])
    for sock in read_sockets:
        if sock == server_socket:
            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)
        else:
            try:
                data = sock.recv(40960000)
                txt = str(data)
                trimmed = txt[2:-1]
                if data:
                    if trimmed.startswith('SIZE'):
                        tmp = trimmed.split()
                        size = int(tmp[1])

                        print("Size is %s" % size)

                        sock.sendall("Received file size".encode(encoding='utf-8'))
                    elif trimmed.startswith('Received'):
                        print(txt)

                        # Delete buffered image
                        if os.path.exists(basename % imgcounter):
                            os.remove(basename % imgcounter)
                        else:
                            print("The file does not exist")

                        print("Transfer complete, shutting down connection")
                        sock.shutdown(socket.SHUT_RDWR)
                    else :
                        print("Image received")
                        print(data)
                        imgcounter += 1

                        # Write the image to disk for buffering
                        myfile = open(basename % imgcounter, 'wb')
                        myfile.write(data)

                        amount_received = len(data)
                        print("Received %s bytes of data" % amount_received)

                        while amount_received < size:
                            data = sock.recv(40960000)
                            amount_received += len(data)

                            print("Received %s bytes of data" % amount_received)

                            if not data:
                                break

                            myfile.write(data)
                        myfile.close()

                        # Image recognition and serialization
                        serialized_dict = image_recognition(basename % imgcounter)
                        sock.sendall(serialized_dict.encode(encoding='utf-8'))

                        # Wait for response from the client
                        # data = sock.recv(4096)
                        # rsp = str(data)[2:-1]
                        # print(rsp)

                        # Shut down the connection
                        # print("Transfer complete, shutting down connection")
                        # sock.shutdown(socket.SHUT_RDWR)
            except socket.error as error:
                print(error)
                sock.close()
                connected_clients_sockets.remove(sock)
                continue
server_socket.close()