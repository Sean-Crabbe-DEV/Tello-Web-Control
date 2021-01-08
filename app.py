
################## Imports
#Flask Server Impt
from flask import Flask, render_template, request
import datetime
import sys

#Tello Comms Impt
import socket
import threading
import time

Tello1_Addr = (' ', 9986)
Tello2_Addr = (' ', 9986)
Tello3_Addr = (' ', 9986)

host = ''
port = 9000
local_address = (host, port)

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

##
##Tello1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##Tello1_socket.connect((Tello1_Addr))
##
##Tello2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##Tello2_socket.connect((Tello2_Addr))
##
##Tello3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##Tello3_socket.connect((Tello3_Addr))
##

#local_address = (host, port) # This is the address of the device running the code
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creates a socket that is used for the tello to drone two way communication
sock.bind(local_address)

################## Receive Drone Reply
def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518) # Tells the code where to look for the drones reply
            # print(data.decode(encoding="utf-8"))
            droneData = data.decode(encoding="utf-8") # Decodes the data from utf-8 to text that can be understood by a human
            print(droneData) # Prints the decoded drone data in the python shell
        except Exception:
            print('\nExit . . .\n')
            break


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
        Tello1 = sock.sendto(command, Tello1_Addr)
        Tello2 = sock.sendto(command, Tello2_Addr)
        Tello3 = sock.sendto(command, Tello3_Addr)
        print('Sending Command /"command/" to the tello')
        return 'do something else'

    elif(request.form['data'] == 'takeoff'):
        takeoff = "takeoff"
        takeoff = takeoff.encode(encoding="utf-8") #takeoff in utf-8 "\x74\x61\x6b\x65\x6f\x66\x66"
        Tello1 = sock.sendto(command, Tello1_Addr)
        Tello2 = sock.sendto(command, Tello2_Addr)
        Tello3 = sock.sendto(command, Tello3_Addr) 
        print('Sending Command /"takeoff/" to the tello')
        return 'do something else'

    elif(request.form['data'] == 'land'):
        land = "land"
        land = land.encode(encoding="utf-8") #land in utf-8 "\x6c\x61\x6e\x64"
        Tello1 = sock.sendto(command, Tello1_Addr)
        Tello2 = sock.sendto(command, Tello2_Addr)
        Tello3 = sock.sendto(command, Tello3_Addr)
        print('land')
        return 'do something else'


    return 'invalid command'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
#    app.run(debug=True, host='0.0.0.0')  #Debug Mode
