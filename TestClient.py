import socket
import time

HOST = '127.0.0.1'
PORT = 65432

def send_command(cmd):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(cmd.encode())
        data = s.recv(1024)
        print(data)
        s.close()

        time.sleep(0.5)

send_command('new:img')
send_command('new:line 1')
send_command('run:hist 234')
send_command('get:hcps')
