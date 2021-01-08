

################## Imports
#Flask Server Impt
from flask import Flask, render_template, request
import datetime
import sys

#Tello Comms Impt
import socket
import threading
import time

#Welcome Message
print("")
print(" ")

#Displays The Hosts (This Device) hostname + ip address
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    
print("Your Computer Name is:" + hostname)    
print("Your Computer IP Address is:" + IPAddr)
print(" ")
print("Starting Flask")


################## Tello Comms
host = ''
port = 9000
locaddr = (host,port) 

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)

def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print('Tello : ', data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break

#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()


################## Flask Server 
sys.path = ['./lib'] + sys.path

app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%d-%m-%Y %H:%M")
    templateData = {
      'title' : 'Tello Command',
      'time': timeString
      }
    return render_template('index.html', **templateData);




@app.route('/ajax', methods=['POST'])
def ajax():
    
    if(request.form['data'] == 'test'):
        print('Testing')
        return 'do something'

    elif(request.form['data'] == 'command'):
        command = "command"
        command = command.encode(encoding="utf-8") #command in utf-8 "\x63\x6f\x6d\x6d\x61\x6e\x64\x0a"
        sent = sock.sendto(command, tello_address)
        print('Sending Command /"command/" to the tello')
        return 'do something else'

    elif(request.form['data'] == 'takeoff'):
        takeoff = "takeoff"
        takeoff = takeoff.encode(encoding="utf-8")
        sent = sock.sendto(takeoff, tello_address) #takeoff in utf-8 "\x74\x61\x6b\x65\x6f\x66\x66"
        print('Sending Command /"takeoff/" to the tello')
        return 'do something else'

    elif(request.form['data'] == 'land'):
        land = "land"
        land = land.encode(encoding="utf-8") #land in utf-8 "\x6c\x61\x6e\x64"
        sent = sock.sendto(land, tello_address)
        print('land')
        return 'do something else'


    return 'invalid command'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
#    app.run(debug=True, host='0.0.0.0')  #Debug Mode
