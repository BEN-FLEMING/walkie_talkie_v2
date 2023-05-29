import socket
import pyaudio
import threading
import tkinter as tk


CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Streaming Client")
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        self.status_label = tk.Label(root, text="Status: Not Connected")
        self.status_label.pack(pady=10)

        self.connect_button = tk.Button(root, text="Connect", command=self.connect)
        self.connect_button.pack(pady=5)

        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.pack(pady=5)

        self.p = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = '127.0.0.1'  # Replace with the server IP address
        server_port = 1234
        self.client_socket.connect((server_address, server_port))

        self.input_stream = self.p.open(format=FORMAT,
                                        channels=CHANNELS,
                                        rate=RATE,
                                        input=True,
                                        frames_per_buffer=CHUNK_SIZE)

        self.output_stream = self.p.open(format=FORMAT,
                                         channels=CHANNELS,
                                         rate=RATE,
                                         output=True,
                                         frames_per_buffer=CHUNK_SIZE)

        self.status_label.config(text="Status: Connected")
        self.connect_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.NORMAL)

        send_thread = threading.Thread(target=self.send_audio)
        receive_thread = threading.Thread(target=self.receive_audio)

        send_thread.start()
        receive_thread.start()

    def disconnect(self):
        if self.client_socket:
            self.client_socket.shutdown(socket.SHUT_WR)
            self.client_socket.close()

        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()

        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()

        self.p.terminate()

        self.status_label.config(text="Status: Not Connected")
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)

    def send_audio(self):
        try:
            while True:
                data = self.input_stream.read(CHUNK_SIZE)
                print("sending audio")
                self.client_socket.sendall(data)
        except KeyboardInterrupt:
            pass

    def receive_audio(self):
        try:
            while True:
                data = self.client_socket.recv(CHUNK_SIZE)
                print("recieving audio")
                self.output_stream.write(data)
        except KeyboardInterrupt:
            pass

    def on_window_close(self):
        self.disconnect()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    client_gui = ClientGUI(root)
    root.mainloop()
