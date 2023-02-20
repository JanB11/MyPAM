import numpy as np
from scipy.signal import butter, filtfilt, lfilter
import matplotlib.pyplot as plt
from matplotlib import animation
from time import sleep
import time
import busio
import digitalio
import board
from gpiozero import MCP3008
import csv
import os

chan0 = MCP3008(0)
chan1 = MCP3008(1)





#Initiliase variables
pot0 = 0
pot1 = 0
cutoff = 3.33 # cutoff frequency
fs = 150 # sample rate
order = 5
start_time=time.time() #Get start time in seconds

test = 0
while os.path.exists(f'potentiometer values_{test}.csv'):
    test += 1
    
filename = f'potentiometer_values{test}.csv'


def butter_low_pass_filter(input_signal, cutoff, fs, order):
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
        filtered_value = butter_low_pass_filter(input_signal, cutoff, fs, order)[-1]
        return int(filtered_value)


with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    
    if file.tell == 0:
        writer.writerow(['time', 'raw_pot1', 'filtered_pot1'])
    
    for i in range(20):
        elapsed_time = time.time() - start_time
        timestamp = round(elapsed_time * 2)/2
        raw_pot1 = int(read_potentiometer0())
        filtered_pot1 = filtered_values(read_potentiometer0())
        writer.writerow([timestamp, raw_pot1, filtered_pot1])
        print('raw: ', raw_pot1)
        print('filtered ', filtered_pot1)
        print('--------------------------')
        time.sleep(0.5)
        
        




# plt.ion()
# fig, ax = plt.subplots()
# input_signal = np.array([])
# 
# while True:
#     raw_value = read_potentiometer()
#     input_signal = np.append(input_signal, raw_value)
#     filtered_signal = butter_low_pass_filter(input_signal, cutoff, fs)
#     
#     print('raw: ', raw_value)
#     print('filtered: ', filtered_signal[len(filtered_signal)-1])
#     
# #   plot input and output values
#     ax.clear()
#     ax.plot(input_signal, label='Raw')
#     ax.plot(filtered_signal, label='Filtered')
#     ax.legend()
#     plt.draw()
#     plt.pause(0.01)  # wait for 10 milliseconds

