import numpy as np
from datetime import datetime
import os
from snAPI.Main import *
import socket

# Socket parameters
HOST = '127.0.0.1'
PORT = 65432

# Setup Picoharp
# select the device library
sn = snAPI()
# get first available device
sn.getDevice()
sn.setLogLevel(logLevel=LogLevel.DataFile, onOff=True)
# initialize the device
sn.initDevice(MeasMode.T2)
# set the configuration for your device type
sn.loadIniConfig("PicoharpConfig\HH.ini")

# Saving path
working_dir = None

def run_hist(identifer):
    """

    :param identifer: String ID for histogram to be saved with
    :return: 0 for success, -1 for failure
    """

    if working_dir is None:
        raise RuntimeError("Image directory not set!")

    sn.histogram.measure(acqTime=1000,savePTU=True)

    data, bins = sn.histogram.getData()
    data = data[0]

    rst = np.zeros((len(data), 2))
    rst[:, 0] = data
    rst[:, 1] = bins
    np.savetxt(working_dir + f"{identifer}-hist.txt", rst)

    return 0

def get_histog_cps():
    """

    :return: Histogram cps
    """

    return np.random.randint(500000, 1000000)

if __name__ == '__main__':
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            try:
                print("Waiting for command...")
                conn, addr = s.accept()
                with conn:
                    #print('Connected by', addr)
                    data = conn.recv(1024).decode()
                    print(f"Received: {data}")
                    split = data.split(" ")
                    cmd = split[0]
                    if len(split) == 2:
                        param = data.split(" ")[1]
                    else:
                        param = ""
                    print(f"Command: {cmd}, param: {param}")

                    if cmd == 'run:hist':
                        if param == "":
                            print("No parameter provided for run:hist")
                            rst = -1
                        else:
                            rst = run_hist(param)
                        response = f'{cmd}={rst}'
                        print(f"Sending response: {response}")
                        conn.sendall(response.encode())
                    elif cmd == 'get:hcps':
                        response = f'{cmd}={get_histog_cps()}'
                        print(f"Sending response: {response}")
                        conn.sendall(response.encode())
                    elif cmd == 'new:img':
                        path = "output/scans/" + str(datetime.now().strftime("%Y%m%d%H%M%S"))
                        os.mkdir(path)
                        working_dir = path + "/"
                    elif cmd == "new:line":
                        if param == "":
                            raise RuntimeError("No parameter provided for new:line")
                        if working_dir is None:
                            raise RuntimeError("Must call new:img before new:line")
                        path = working_dir + f"line{param}"
                        os.mkdir(path)
                        working_dir = path + "/"
                    else:
                        print(f"Unknown command: {cmd}")
                        response = f'{-1}'
                        conn.sendall(response.encode())

            except KeyboardInterrupt:
                if conn:
                    print("Closing connection")
                    conn.close()
                print("Closing server")