# ImageRecognitionWeb
Python Flask web-based recognition App
This is an image recognition web service. 
Users can open the website and upload an image, 
then the website will display the top three predicted class labels with probabilities of the uploaded image

# Instruction
1. Running environment: the server end of our application needs to be run on machines with Python 3.5 or higher version
2. Download this repository 
3. Setting up Geni servers by creating a slice and adding resources with the Rspec file in this project repository ‘rspec.xml’. 
Click ‘Reserve Resources’ button and wait until the nodes are ready. You will see two nodes: webNode and RecogNode.
4. Log on the RecogNode. Upload ‘rcgnode_setup.sh’ onto the RecogNode and run it. This script will install relevant packages and download our source files. After setup finishes, you will see a folder named ‘rcgNode’. Navigate into ‘rcgNode’ folder and use command: ‘sudo python3 server.py’ to start the server.
5. Log on the WebNode. Upload ‘webNode_setup.sh’ onto the webNode and run it “sudo webNode_setup.sh”. This script will install Apache2 for an HTTP server and other required packages. Navigate to the http root directory using “cd /var/www/html”, and make sure you put all files in the webNode repo under this directory. After setup is complete, use command ‘sudo python3 main.py’ to start the webNode server.
6. Open http://128.163.232.71/mainPage with your Google Chrome browser and start using the website.
