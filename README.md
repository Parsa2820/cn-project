# cn-project
Computer Networks Course Project

## Install requirements
```bash
pip install -r requirements.txt
```
On GNU/Linux you should also install `portaudio` using your package manager. For example, on Ubuntu you can install it with the following command:
```bash
sudo apt-get install portaudio19-dev
```

## Run the Server
```bash
cd server
python main.py server
```
For test purposes, you can run the server in command line mode.
```bash
python main.py cli
```

## Run the Client
```bash
cd client
python main.py [server_ip]
```
If no server IP is provided, the client will connect to the localhost.