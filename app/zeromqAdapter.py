import numpy as np
import requests
import zmq


class ZmqAdapter:
    def __init__(self, signal_address, endpoint_address):
        self.signal_address = signal_address
        self.endpoint_address = endpoint_address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(self.signal_address)
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.running = True

    def run(self):
        while self.running:
            signal = self.socket.recv()
            signal_array = self.convert_signal(signal)
            self.send_signal(signal_array)
            self.running = False

    def convert_signal(self, signal):
        signal_array = np.frombuffer(signal, dtype=np.complex64)
        real_part = signal_array.real
        imag_part = signal_array.imag
        signal_array_split = np.stack((real_part, imag_part), axis=-1)        
        return signal_array_split

    def send_signal(self, signal_array):
        headers = {"Content-Type": "application/json"}
        data = signal_array.tolist()
        response = requests.post(self.endpoint_address + '/recieve_signal', json=data, headers=headers)
        if response.status_code == 200:
            print("Signal sent successfully!")
        else:
            print("Failed to send signal.")
