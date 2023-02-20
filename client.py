import eventlet
import socketio
import struct
from time import sleep

sio = socketio.Client()
sio.connect('http://192.168.0.31:5000')

pot0_val = 0

@sio.event
def connect():
    print('connection established')


@sio.on('pot0_value')
def response(pot0):
    global pot0_val
    pot0_val = pot0

def use_pot0_val():
    global pot0_val
    data = pot0_val
    return data


@sio.on('pot1_value')
def response(pot1):
    print('pot1: ', pot1)

@sio.event
def disconnect():
    print('disconnected from server')
    


while True:
    val = use_pot0_val()
    print('Using pot0 value: ', val)
    
    
#Hotspot IP: 172.20.10.10
#Home IP: 192.168.0.31
    
    
