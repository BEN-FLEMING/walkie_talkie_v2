import socket
import threading
import pyaudio

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

connected_clients = []
lock = threading.Lock()


def handle_client(client_socket, client_address):
    print("Client connected:", client_address)
    lock.acquire()
    connected_clients.append(client_socket)
    lock.release()

    try:
        while True:
            data = client_socket.recv(CHUNK_SIZE)
            if not data:
                break
            # Broadcast received data to all other connected clients
            lock.acquire()
            for client in connected_clients:
                if client is not client_socket:
                    client.sendall(data)
            lock.release()
    except Exception as e:
        print("Error handling client:", e)

    lock.acquire()
    connected_clients.remove(client_socket)
    lock.release()
    client_socket.close()
    print("Client disconnected:", client_address)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = '127.0.0.1'
    server_port = 1234
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print("Server listening on {}:{}".format(server_address, server_port))

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK_SIZE)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()
    server_socket.close()


start_server()

