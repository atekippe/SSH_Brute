import paramiko
import sys


def ssh_command(ssh):
    command = "cat /etc/passwd"
    guess = "1111\n"
    ssh.invoke_shell()
    stdin, stdout, stderr = ssh.exec_command(command)

    print(stdout.read())
    stdin, stdout, stderr = ssh.exec_command('ls')
    print(stdout.read())


def ssh_connect(host, suser, skey):
    try:
        s = paramiko.SSHClient()

        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('Connecting to {0}'.format(host))
        s.connect(hostname=host, username=suser, password=skey)

        return s
    except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.AuthenticationException) as e:
        print('Connection Failed to {0}'.format(host))
        print(e)


if __name__=='__main__':
    user = "cdc"
    key =  "cdc1"
    lhost = "10.1.40.28"
    ssh = ssh_connect(lhost, user, key)
    #ssh_command(ssh)
