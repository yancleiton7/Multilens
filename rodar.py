import socket 
from requests import get

import os

caminho = os.getcwd()
hostname = socket.gethostname()
ip_interno = socket.gethostbyname(hostname)

os.environ["FLASK_APP"]="doceriah/app.py"
os.environ["FLASK_ENV"]="development"

print(ip_interno)

#os.system(f"set FLASK_APP ={caminho}/doceriah/app.py")
#os.system(f"set FLASK_ENV =development")
os.system(f"python -m flask run --host={ip_interno}")


#ip_externo = get('https://api.ipify.org').text

#print(f"Hostname: {hostname}")
#print(f"IP Interno: {ip_interno}")
#print(f"IP Externo: {ip_externo}")