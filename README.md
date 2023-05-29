# walkie_talkie_v2

Walkie talkie implementation for Teton challenge!


## Walkie Talkie Server


The Walkie Talkie Server is a simple multithreaded server application that allows clients to communicate with each other using audio streaming over a local network. This application is designed to simulate a walkie talkie communication system.


### Requirements

To run the Walkie Talkie Server, you need the following:

- Python 3.6 or above
- PyAudio library
- A working network connection


### Installation

Clone the repository:
```
bash$ git clone https://github.com/your-username/walkie_talkie_v2.git
```
#### Change to the server directory:**
```
bash$ cd walkie_talkie_v2
```
#### Install the required dependencies:
```
pip install -r requirements.txt
```
Required dependencies mainly include pyaudio which can be installed using the below (homebrew & pip required)
```
brew install portaudio
pip install pyaudio
```

### Usage

Open the server.py file and replace the server_address variable with the IP address of the server machine (if testing locally) or the local network to communicate accross this.

Run the server:
```
python3 server.py
```
The server will start listening for incoming client connections.

Note: Make sure the clients are configured to connect to the correct server IP address.


## Walkie Talkie Client

The Walkie Talkie Client is a client application that connects to the Walkie Talkie Server to establish audio communication with other clients.


### Requirements
To run the Walkie Talkie Client, you need the following:

- Python 3.6 or above
- PyAudio library
- A working network connection


### Installation

Clone the repository:
```
bash$ git clone https://github.com/BEN-FLEMING/walkie_talkie_v2.git
```
Change to the client directory:
```
bash$ cd walkie_talkie_v2/client
```
Install the required dependencies:
```
pip install -r requirements.txt
```
Required dependencies mainly include pyaudio which can be installed using the below (homebrew & pip required)
```
brew install portaudio
pip install pyaudio
```

### Usage

Open the client_v2_gui.py file and replace the server_address variable with the IP address of the server machine (if testing locally) or the local network ip address to use functionally and communicate accross a network.

To operate the client - it works like a walkie talkie, by holding down the talk button you stream audio to other clients, when released it will stop streaming audio.

### Run the client:
```
python3 client_v2_gui.py
```
The client will connect to the server and start streaming audio.

Note: Make sure the server IP address is correctly specified.

