import socketio
import eventlet
from flask import Flask, render_template
from flask_socketio import SocketIO
from time import sleep
from gpiozero import MCP3008
import struct
import numpy as np
from scipy.signal import butter, lfilter, filtfilt


chan0 = MCP3008(0)
chan1 = MCP3008(1)

app = Flask(__name__)
sio = SocketIO(app)

#Initiliase variables
pot0 = 0
pot1 = 0
cutoff =  # cutoff frequency
fs = 50 # sample rate


#...............Reading and Filtering Data..............#

#Butterworth low pass filter function
def butter_low_pass_filter(input_signal, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, input_signal, padlen=len(input_signal)-1)
    return filtered_signal

#Reading Potentiometer Values
def read_potentiometer0():
    analogVal0=chan0.value*360
    return analogVal0

def read_potentiometer1():
    analogVal1=chan1.value*360
    return analogVal1

#Output filtered potentiomenter values
def filtered_values(data):
    while True:
        input_signal = np.array([])
        raw_value = data
        input_signal = np.append(input_signal, raw_value)
        filtered_value = butter_low_pass_filter(input_signal, cutoff, fs)[-1]
        return int(filtered_value)


#...................Sending Data......................#
def send_sensor_readings():
    while True:
        global pot0
        global pot1
        pot0 = filtered_values(read_potentiometer0())
        pot1 = filtered_values(read_potentiometer1())
        raw0 = int(read_potentiometer0())

        sio.emit('pot0_value', pot0)
        print('filtered0: ', pot0)
        print('raw0: ', raw0)
        
#         sio.emit('pot1_value', pot1)
#         print('data1: ', pot1)
        
        sio.sleep(0.5)
            
#...................Connection......................#
@sio.on('connect')
def on_connect():
    print('Client connected')
    sio.start_background_task(send_sensor_readings)


@sio.on('disconnect')
def on_disconnect():
    print('Client disconnected')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    
    #Remember to change host according to wi-fi connection
    sio.run(app, host = '172.20.10.10', port=5000, debug = True)
    
#home IP: 192.168.0.31
#hotspot IP: 172.20.10.10

