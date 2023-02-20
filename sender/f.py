import numpy as np
import scipy.signal as sig
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import struct
import collections


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi,cs)
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)

def read_potentiometer():
    data=chan0.value
    return data

alpha = 0.1  # smoothing factor
prev_output = 0  # initialize previous output

def low_pass_filter(input_value):
    global prev_output
    output = alpha * input_value + (1 - alpha) * prev_output
    prev_output = output
    return output

plt.ion()  # turn on interactive mode
fig, ax = plt.subplots()  # create a plot figure

input_values = []  # list to store input values
output_values = []  # list to store filtered output values

while True:
    input_value = read_potentiometer()  # function to read potentiometer value
    input_values.append(input_value)
    output = low_pass_filter(input_value)
    output_values.append(output)
    print('raw: ', input_value)
    print('filtred: ', output)
    
    # plot input and output values
    ax.clear()
    ax.plot(input_values, label='Raw')
    ax.plot(output_values, label='Filtered')
    ax.legend()
    plt.draw()
    plt.pause(0.01)  # wait for 10 milliseconds