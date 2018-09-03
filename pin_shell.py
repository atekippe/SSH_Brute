# Script prompts for a pin.  Used to test SSH_Brute_Pin.py
# set in the /etc/ssh/sshd_config to run -> ForceCommand /home/cdc/pin.py

#!/usr/bin/python3

f = open('/tmp/pin_debug', 'a')

while 1 is 1:
    p = 9999
    pin = int(input("Pin: "))
    f.write(str(pin) + "\n")
    if pin == p:
        print("Correct")
        exit()
    else:
        print("Incorrect")
