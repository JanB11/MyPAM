import eventlet
import socketio
import RPi.GPIO as GPIO
import struct
from time import sleep


sio = socketio.Client()

@sio.event
def connect():
    print('connection established')


@sio.on('pot0_value')
def response(pot0)
    print('pot0: ', pot0)
    
    
@sio.on('pot1_value')
def response(pot1):
    print('pot1: ', pot1)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://172.20.10.10:5000')

    
    
    