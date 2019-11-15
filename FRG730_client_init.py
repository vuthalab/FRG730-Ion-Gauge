"""
This is the client sockets, which will be used to connect to the
publishing socket.

You can have multiple client sockets connected to the one publishing
socket and have them run different refreshment rates and other
parameters.

WARNING!
- if you set time.sleep in line 31 to be 0 or comment it out, you will
not have any data retrieved. time.sleep must be greater than 0.
"""

import os
os.chdir('/home/vuthalab/google_drive/code/hydrogen_control/Widgets/Objects')
import zmq
from zmq_client_socket import zmq_client_socket
import time

## Initialize Client socket Settings here! (You can run multiple clients on different shells)
connection_settings = {'ip_addr': 'localhost',  # ip address
                       'port': 5558,            # our open port
                       'update_period_ms': 10,                   # Not implemented yet
                       'logdata': False,                        # Not implemented yet
                       'topic': 'FRG730'}       # device

client_socket = zmq_client_socket(connection_settings)
client_socket.make_connection()

while True:
    client_socket.read_on_demand()
    time.sleep(1)                               # change this to depend information update rate.

