import tkinter as tk
import socket
import threading
import pyaudio

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class WalkieTalkieClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Walkie Talkie Client")

        self.label = tk.Label(master, text="Hold the 'Talk' button to speak")
        self.label.pack(pady=10)

        self.talk_button = tk.Button(master, text="Talk", bg="lightgray", width=10, relief=tk.RAISED)
        self.talk_button.pack(pady=10)
        self.talk_button.bind('<ButtonPress>', self.start_audio_stream)
        self.talk_button.bind('<ButtonRelease>', self.stop_audio_stream)

        self.status_label = tk.Label(master, text="Status: Not Talking")
        self.status_label.pack(pady=10)

        self.is_talking = False
        self.send_audio_flag = threading.Event()

        self.client_socket = None
        self.audio_stream = None

        # Connect to the server on startup
        threading.Thread(target=self.connect_to_server).start()
        threading.Thread(target=self.receive_audio).start()

    def start_audio_stream(self, event):
        self.is_talking = True
        self.status_label.config(text="Status: Talking")
        threading.Thread(target=self.send_audio).start()

    def stop_audio_stream(self, event):
        self.is_talking = False
        self.status_label.config(text="Status: Not Talking")

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = '127.0.0.1'  # Replace with the server IP address
        server_port = 1234
        self.client_socket.connect((server_address, server_port))
        print("Connected to server.")

    def send_audio(self):
        p = pyaudio.PyAudio()
        input_device_index = 0  # Specify the index of the desired input device
        self.audio_stream = p.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   input=True,
                                   frames_per_buffer=CHUNK_SIZE,
                                   input_device_index=input_device_index)

        self.send_audio_flag.set()

        try:
            while self.is_talking and self.send_audio_flag.is_set():
                data = self.audio_stream.read(CHUNK_SIZE)
                if self.client_socket:
                    self.client_socket.sendall(data)
        except Exception as e:
            print("Error sending audio:", e)

        self.audio_stream.stop_stream()
        self.audio_stream.close()
        p.terminate()

    def receive_audio(self):
        p = pyaudio.PyAudio()
        output_stream = p.open(format=FORMAT,
                               channels=CHANNELS,
                               rate=RATE,
                               output=True,
                               frames_per_buffer=CHUNK_SIZE)

        try:
            while True:
                if self.client_socket:
                    data = self.client_socket.recv(CHUNK_SIZE)
                    output_stream.write(data)
        except Exception as e:
            print("Error receiving audio:", e)

        output_stream.stop_stream()
        output_stream.close()
        p.terminate()

    def cleanup(self):
        self.send_audio_flag.clear()
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.client_socket:
            self.client_socket.close()

if __name__ == '__main__':
    root = tk.Tk()
    walkie_talkie_client = WalkieTalkieClientGUI(root)
    root.protocol("WM_DELETE_WINDOW", walkie_talkie_client.cleanup)
    root.mainloop()
