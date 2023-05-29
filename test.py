import pyaudio
import time

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def test_microphone():
    p = pyaudio.PyAudio()
    input_stream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK_SIZE)

    output_stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           output=True,
                           frames_per_buffer=CHUNK_SIZE)

    print("Recording from microphone. Press Ctrl+C to stop.")

    try:
        while True:
            data = input_stream.read(CHUNK_SIZE)
            output_stream.write(data)
    except KeyboardInterrupt:
        pass

    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()


if __name__ == '__main__':
    # Test microphone input locally
    test_microphone()