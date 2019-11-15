# FRG730-Ion-Gauge
Simple python interface to communicate with the Agilent FRG-730 Ion Gauge

## How to use
```python
>>> from FRG730_Ion_Gauge import FRG370
>>> ion_gauge = FRG730('/dev/ttyUSB3') 

>>> ion_gauge.read_pressure_torr()
0.00010933268155833919

>>> ion_gauge.read_pressure_torr_clean()
'1.0933e-04'

>>> ion_gauge.set_torr() #Set units of gauge to torr, pa or mbar
```

The ion gauge is also coded into a python socket which allows for data streaming on a server that can be read by multiple clients at the same time. To use this, run FRG730_server_init.py to start the server. A client can be initiated using the following:

```python
from zmq_client_socket import zmq_client_socket
connection_settings = {'ip_addr': 'localhost',  # ip address of server
                       'port': 5558,            # port of server
                       'update_period_ms': 10,                   # Not implemented yet
                       'logdata': False,                        # Not implemented yet
                       'topic': 'FRG730'}       # device of server

FRG730_socket = zmq_client_socket(connection_settings)
FRG730_socket.make_connection()

print('The current pressure is ' + str('{:.4e}'.format(FRG730_socket.read_on_demand()[1]['pressure'])) + " torr")
```
