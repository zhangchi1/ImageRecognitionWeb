#!/bin/bash
echo "updating apt-get"
apt-get update
echo "updating apache2"
apt-get -y install apache2
echo "installing dependencies"
apt-get install python3-pip
apt-get install wget
echo "downloading webserver codes"
wget https://raw.githubusercontent.com/zhangchi1/ImageRecognitionWeb/master/webNode/www/html