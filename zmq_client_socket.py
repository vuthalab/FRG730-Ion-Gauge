"""
Client socket for reading data off the publishing zmq_server_socket.

Created by James Park and Mohit Verma.
"""
import os
import zmq
import ast
import time


class zmq_client_socket:    
    """
    A class object for a client zmq socket.
    """
    def __init__(self, connection_settings):
        """Sets up an client socket to be paired with a publishing 
        socket.
        
        Note: zmq.Context() must be run to initialize the connections
        between the sockets. It will be used to manage any sockets 
        that are connected.
        
        @type self: zmq_client_socket
        @type settings: String
        @rtype: None
        """
        self.zmq_context = zmq.Context() #initialize zmq 
        self.made_socket = False
        self.received_first_data = False
        self.load_settings(connection_settings)
        self.make_connection()
        self.current_data = self.grab_data()
        
                
    def grab_data(self):
        """Tries to see if any information from the publishing socket 
        can be retrieved. If no information can be retrieved, an 
        error message will be printed.
        
        NOTE: The data that is grabbed is in QUEUE order, so the 
        information that will be read is from the very last information
        loaded in the queue.
        
        @type self: zmq_client_socket
        @rtype: None
        """
        if self.made_socket is True:
            try:
                received_data = self.socket.recv(flags=zmq.NOBLOCK)
                self.received_first_data = True
                print(received_data)
            except zmq.ZMQError:
                if self.received_first_data is False:
                    return
                print("Data Grab failed, no information was retrieved.")
                return
            
    def read_on_demand(self):
        """
        Retrieves all the data from the publishing socket (which is
        ordered into an abstract syntax tree and returns the very last
        sent information by the publishing socket.
        
        In simple terms, returns the very last information sent by
        the publishing socket.
        
        @type self: zmq_client_socket
        @rtype: None
        """
        done = False
        num_tries = 0
        while not done:
            try:
                string = self.socket.recv(flags=zmq.NOBLOCK)
                num_tries += 1
            except zmq.ZMQError:
                if num_tries > 0:
                    done = True
    
        out = string.decode("utf-8").split(' ')
        topic, time = out[:2]
        messagedata = ast.literal_eval(' '.join(out[2:]))
    
        timestamp = float(time)
        return (timestamp, messagedata)


    def load_settings(self, connection_settings):
        """ Initializes this client zmq socket to the specified 
        settings which will be used to connect to the relevant
        publishing zmq_socket.
        
        @type self: zmq_client_socket
        @type connection_settings: Dictionary (strings and integers)
        
        @type ip_addr: String
        @type port: Integer
        @type topic: String
        @rtype: None
        """
        self.connection_settings = connection_settings

    def make_connection(self):
        """ Makes a connection to the specified publishing zmq_socket.
        
        @type self: zmq_client_socket
        @rtype: None
        """
        if self.made_socket:
            self.socket.close()
        else:
            self.made_socket = True
        self.socket = self.zmq_context.socket(zmq.SUB)  #initialized to be a zmq client socket
        #connection settings to the ip address and port.
        connection_string = "tcp://%s:%s" % (self.connection_settings['ip_addr'],
                                          self.connection_settings['port'])
        self.socket.connect(connection_string)
        self.socket.setsockopt(zmq.SUBSCRIBE, self.connection_settings['topic'].encode())
        

