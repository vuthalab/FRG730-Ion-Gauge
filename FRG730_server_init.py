"""

NOTE
Use time.sleep to determine your data upload speed. If your
pub_init time.sleep is < your client_init time.sleep, then your client
socket will read less data than
"""
import os
import time
os.chdir('/home/vuthalab/google_drive/code/hydrogen_control/Widgets/Objects')
from zmq_server_socket import zmq_server_socket
from FRG730_Ion_Gauge import FRG730

topic = "FRG730"                        # Change this to whatever device you're going to use.
port = 5558                             # If port is in use, enter a different 4 digit port number.

delay_time = 0.1 #s, between measurements

##Initialize Device
topic_device = FRG730('/dev/ttyUSB3')   # Change this to whatever device you want to connect with the zmq socket.
if topic_device is None:
    print("No device was loaded.")
    exit()

## Create a Publisher for the given Topic and Port.
publisher = zmq_server_socket(port, topic)
counter = 0

while True:
    pressure = topic_device.read_pressure_torr()
    data_dict = {'pressure' : pressure}
    publisher.send(data_dict)
    time.sleep(delay_time)                     # change time.sleep to determine upload speed

    counter += 1
    if counter == 10:
        print('{:.4e}'.format(float(publisher.current_data[38:-1]))) #Prints pressure in scientific notation
        counter = 0
publisher.close()

