from flask import render_template
from flask import request
from flask import Flask
import socket
import time
import requests
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 1st read image
# TODO: read image
# img = open('img1.JPG', 'rb')
# # read image as bytes
# file = img.read()
# fileSize = len(file)

def requestLabelsFromServer(file):
    # Create a TCP/IP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    host = 'pcvm2-11.lan.sdn.uky.edu'
    portNum = 6666
    server_address = (host, portNum)
    print('connecting to {} port {}'.format(*server_address))
    clientSocket.connect(server_address)
    # =============================================================================
    # Statistics Fields
    # =============================================================================
    RTT = 0  # unit s
    throughput = 0  # unit bits/s
    fileSize = len(file)
    fileSizeMsg = 'SIZE ' + str(fileSize)
    # =============================================================================
    # Classification Label Fields
    # =============================================================================
    labels = ['' for i in range(5)]  # get top 5 labels
    probability = [0.0 for i in range(5)]  # top 5 label's probabilities
    # send image bytes to server
    try:
        print('sending image as bytes with size',fileSize)
        # send image size to server node
        fileSizeMsg = bytes(fileSizeMsg,'utf-8')
        clientSocket.send(fileSizeMsg)
        # check server got the file sie
        getSizeRsp = clientSocket.recv(4096)
        sizeResponseMsg = getSizeRsp.decode(encoding='utf-8')
        print('Response from server:', sizeResponseMsg)

        # resend file size
        while sizeResponseMsg != 'Received file size':
            # send image size to server node
            fileSizeMsg = bytes(fileSizeMsg, 'utf-8')
            clientSocket.send(fileSizeMsg)
            # check server got the file sie
            getSizeRsp = clientSocket.recv(4096)
            sizeResponseMsg = getSizeRsp.decode(encoding='utf-8')
            print('Response from server:', sizeResponseMsg)

        # send image bytes to recog Node
        if sizeResponseMsg == 'Received file size':
            print('Sending image to server with type', type(file))
            startTime = time.time()
            clientSocket.send(file)
            
            getLabelRsp = clientSocket.recv(4096)
            RTT = time.time() - startTime
            throughput = (fileSize + len(getLabelRsp))/RTT
            #TODO: process label text
            # Print statistics
            print(getLabelRsp)
            print('RTT: ',RTT)
            print('Throughput: ', throughput)
    finally:
        print('Closing client socket')
        clientSocket.close()
        # close current image file
        img.close()
    return RTT, throughput, labels, probability


# TODO: send RTT, throughput, file size, labels back to HTML
app = Flask(__name__)

@app.route('/mainPage', methods = ['GET'])
def render():
    print('******** In render Func *********')
    return render_template('mainPage.html')

@app.route('/imageProcess', methods = ['POST'])
def imageProcess():
    image=request.data
    print(image)
    print('Image size: ',len(image))

    img = open('img1.JPG', 'rb')
    file = img.read()
    fileSize = len(file)
    print(file)
    print('fileSize', fileSize)

    dic = {}
    dic['result'] = 'OK'
    dic['updatedImage'] = 'apple'
    return dic


if __name__ == "__main__":
    # TODO: read image from HTML
    app.run(host='128.163.232.71', port=80)


    # test
    img = open('img1.JPG', 'rb')
    file = img.read()
    fileSize = len(file)
    print('image size:', fileSize)
    requestLabelsFromServer(file)
