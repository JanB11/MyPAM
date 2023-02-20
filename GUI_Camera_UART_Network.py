import tkinter as tk
import picamera
import serial
import struct
from threading import Thread
import time
import eventlet
import socketio

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

class App:
    def __init__(self, master):
        self.master = master
        self.button_start = tk.Button(master, text="Start Camera", command=self.start_camera)
        self.button_stop = tk.Button(master, text="Stop Camera", command=self.stop_camera)
        self.text_box_1 = tk.Text(master, height=1, width=5)
        self.text_box_2 = tk.Text(master, height=1, width=5)
        self.slider = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL)
        self.text_box_1.pack()
        self.text_box_2.pack()
        self.slider.pack()
        self.button_start.pack()
        self.button_stop.pack()
        self.button_stop.config(state="disable")
        self.x = 0
        self.z = 0
        
        self.uart_thread = Thread(target=self._uart_function)
        self.uart_thread.start()

    def start_camera(self):
        if not hasattr(self, 'camera') or not self.camera.previewing:
            self.camera = picamera.PiCamera()
            self.camera.resolution = (640, 480)
            self.camera.start_preview()
        self.button_stop.config(state="normal")

    def stop_camera(self):
        if hasattr(self, 'camera'):
            self.camera.stop_preview()
            self.camera.close()
        self.button_stop.config(state="disable")
        self.uart_thread.join()

    def _uart_function(self):
        ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        
        while True:
            val = use_pot0_val()
            print('pot0 value: ', val)
            my_array = [1, 2, 3]
            my_array[0] = val
            my_array[1] = 1
            my_array[2] = 15
            print('array: ', my_array[0])

        while True:
            try:
                if not ser.isOpen():
                    ser.open()
                y = self.slider.get()
                my_array = [1, 2, 3]
                my_array[0] = val
                my_array[1] = y
                my_array[2] = 15
                binary_data = struct.pack('<3i', *my_array)
                ser.write(binary_data)
                
                
                data=ser.readline()
                data = data.strip(b'\n').decode("utf-8")
                numbers=data.split(',')
                
                first_number=int(numbers[0])
                second_number=int(numbers[1])
                Third_number=int(numbers[2])
                
                
                print('a = ',first_number)
                print('b = ',second_number)
                print('c = ',Third_number)
                self.master.after(1000, self._update_textbox, my_array[0], first_number)
            except serial.SerialException as e:
                print(f'An error occurred: {e}')
            finally:
                ser.close()

    def _update_textbox(self, my_array_0, first_number):
        self.text_box_1.delete("1.0", tk.END)
        self.text_box_1.insert(tk.END, my_array_0)
        self.text_box_2.delete("1.0", tk.END)
        self.text_box_2.insert(tk.END, first_number)
        time.sleep(0.01)


root = tk.Tk()
app = App(root)
root.mainloop()

