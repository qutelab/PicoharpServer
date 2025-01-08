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
sn.initDevice(MeasMode.T3)
# set the configuration for your device type
sn.loadIniConfig("PicoharpConfig\PH330_Edge.ini")

# Saving path
scan_dir = None
working_dir = None

def run_hist(identifer):
    """

    :param identifer: String ID for histogram to be saved with
    :return: 0 for success, -1 for failure
    """

    if scan_dir is None:
        raise RuntimeError("Image directory not set!")

    sn.histogram.measure(acqTime=45000,savePTU=False)

    counts, bins = sn.histogram.getData()
    counts = counts[1] # 0 is sync, 1 is ch1, 2 is ch2, etc

    rst = np.zeros((len(counts), 2))
    rst[:, 1] = counts
    rst[:, 0] = bins
    np.savetxt(working_dir + f"{identifer}-hist.txt", rst)

    return 0

def get_histog_cps():
    """

    :return: Histogram cps
    """
    cnt = sn.getCountRates() # Not sure if this is correct count rate. Is this the same as histog CPS?
    return cnt[1]  # 0 is sync, 1 is ch1, 2 is ch2, etc


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
                        scan_dir = path + "/"
                    elif cmd == "new:line":
                        if param == "":
                            raise RuntimeError("No parameter provided for new:line")
                        if scan_dir is None:
                            raise RuntimeError("Must call new:img before new:line")
                        path = scan_dir + f"line{param}"
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