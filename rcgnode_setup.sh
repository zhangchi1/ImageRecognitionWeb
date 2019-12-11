#!/bin/bash
echo "updating apt-get"
apt-get update
echo "installing dependencies"
apt-get install python3-pip
apt-get install wget
python3 -m pip install --upgrade google-cloud-vision
echo "downloading python codes"
mkdir rcgNode
cd rcgNode
wget https://raw.githubusercontent.com/zhangchi1/ImageRecognitionWeb/master/rcgNode/recognition.py
wget https://raw.githubusercontent.com/zhangchi1/ImageRecognitionWeb/master/rcgNode/server.py
wget https://raw.githubusercontent.com/ThisIsNotAValidUserName/Geni-mini-project/master/CS655FinalKey.json
