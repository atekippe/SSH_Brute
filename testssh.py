import sys
import paramiko


def ssh_command(ssh):
    command = "cat /etc/passwd"
    guess = "1111\n"
    ssh.invoke_shell()
    stdin, stdout, stderr = ssh.exec_command(command)

    print(stdout.read())
    stdin, stdout, stderr = ssh.exec_command('ls')
    print(stdout.read())



def ssh_connect(host, user, key):
    try:
        ssh = paramiko.SSHClient()
        print('Calling paramiko')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=key)

        ssh_command(ssh)
    except Exception as e:
        print('Connection Failed')
        print(e)


if __name__=='__main__':
    user = "cdc"
    key =  "cdc"
    host = "10.1.40.28"
    ssh_connect(host, user, key)

