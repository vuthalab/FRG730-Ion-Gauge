'''
Code used to perform serial communication and log data with the FRG730 Full-Range Ion Gauge
Written by: Mohit Verma
November, 2019
All informations for commands are taken from the FRG730 Operating Manual
'''
import serial
import numpy as np
import time

class FRG730:

    def __init__(self, address = '/dev/ttyUSB5'):
        self.gauge = serial.Serial(address,baudrate=9600,stopbits=1,parity='N',timeout=1)

    def read(self, Nbyte):
        return self.gauge.read(Nbyte) #Reads Nbyte bytes from values being streamed by ion gauge

    def read_all(self):
        return self.gauge.read_all()

    def write(self, command):
        self.gauge.write((command))
        #print( self.generator.readlines() )

    def read_pressure_torr(self):
        self.gauge.read_all() #Clear buffer
        data = self.gauge.read(16) #Reading enough bytes to collect a full stream of data

        synchronization_byte = 7 #byte that denotes start of output string
        data_length = 9 #9 bytes that are sent from the device every 6 ms
        output_string = []
        record_byte = False

        for byte in data:
            if byte == synchronization_byte:
                record_byte = True
            if record_byte and (len(output_string) < data_length): #Load list with one full output string
                output_string.append(byte)

        pressure = 10**((output_string[4]*256+output_string[5])/4000 - 12.625) #Conversion from manual

        #return '{:.4e}'.format(pressure) clean formatting
        return pressure

    def read_pressure_torr_clean(self):
        data = self.gauge.read(16) #Reading enough bytes to collect a full stream of data

        synchronization_byte = 7 #byte that denotes start of output string
        data_length = 9 #9 bytes that are sent from the device every 6 ms
        output_string = []
        record_byte = False

        for byte in data:
            if byte == synchronization_byte:
                record_byte = True
            if record_byte and (len(output_string) < data_length): #Load list with one full output string
                output_string.append(byte)

        pressure = 10**((output_string[4]*256+output_string[5])/4000 - 12.625) #Conversion from manual

        return '{:.4e}'.format(pressure) #clean formatting

    def read_pressure_mbar(self):
        data = self.gauge.read(16) #Reading enough bytes to collect a full stream of data

        synchronization_byte = 7 #byte that denotes start of output string
        data_length = 9 #9 bytes that are sent from the device every 6 ms
        output_string = []
        record_byte = False

        for byte in data:
            if byte == synchronization_byte:
                record_byte = True
            if record_byte and (len(output_string) < data_length): #Load list with one full output string
                output_string.append(byte)

        pressure = 10**((output_string[4]*256+output_string[5])/4000 - 12.5)

        #return '{:.4e}'.format(pressure) clean formatting
        return pressure

    def set_torr(self):
        #Sets units on gauge to torr
        command = bytes([3]) + bytes([16]) + bytes([142]) + bytes([1]) + bytes([159]) #From manual
        self.gauge.write(command)

    def set_mbar(self):
        #Sets units on gauge to mbar
        command = bytes([3]) + bytes([16]) + bytes([142]) + bytes([0]) + bytes([158]) #From manual
        self.gauge.write(command)

    def set_Pa(self):
        #Sets units on gauge to mbar
        command = bytes([3]) + bytes([16]) + bytes([142]) + bytes([1]) + bytes([159]) #From manual
        self.gauge.write(command)

    def degas_on(self):
        #Turns on degas minute for 3 minutes, should only be turned on for pressures below <3e-6 torr
        command = bytes([3]) + bytes([16]) + bytes([196]) + bytes([1]) + bytes([213]) #From manual
        self.gauge.write(command)

    def degas_off(self):
        #Spots degas before 3 minutes are up
        command = bytes([3]) + bytes([16]) + bytes([196]) + bytes([0]) + bytes([212]) #From manual
        self.gauge.write(command)
