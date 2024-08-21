import socket
import os
import subprocess
import configparser

# global vars and config
configPath = 'fsconfig.json'
fb_path = ".\\SupportDevice\\filebrowser\\filebrowser.exe "
dev = True
fb_bootloader = 1
# 0 for os.system, 1 for subprocess

def readConfig(configPath):
    con = configparser.ConfigParser()
    con.read(configPath, 'utf-8')
    sections = con.sections()
    config = {}
    for section in sections:
        config[str(section)] = dict(con.items(str(section)))
    return config

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def boot(command, bootloader):
    if bootloader == 0:
        os.system(command)
    elif bootloader == 1:
        proc = subprocess.Popen(
            command,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        outinfo, errinfo = proc.communicate()
        if dev:
            print(outinfo.decode('utf-8'))
            print(errinfo.decode('utf-8'))

def generateCommand



# main program
def main():
    ip = get_ip()

    useConf = str(input("Use config file?(0 for N, else for Y):"))


    if useConf == 0:
        print("Have detected host ip address: " + str(ip) + ", do you agreed to use this address as host ip?")
        choice = str(input("(0 for N, else for Y):"))
        if choice == '0':
            content = os.system("ipconfig")
            print("ipconfig command returned that: \n" + content + "\n")
            ip = str(input("Please enter an ip address instead:"))
        else:
            print("IP confirmed.")

        choice = ''
        choice = str(input('Using 80 port for file server as default, do you agree with that? (0 for N, else for Y):'))
        if choice == '0':
            port = str(input('Enter an port instead:'))
        else:
            port = '80'
    else:
        con = readConfig(configPath)
        fb_path = con['path']['filebrowser']
        alist_path = con['path']['alist']
        fb_port = con['port']['filebrowser']
        alist_port = con['port']['alist']

    command = fb_path + ' -a ' + ip + " -p " + port

    if dev: 
        print("Command string: " + command)

    try:
        boot(command, fb_bootloader)
    except Exception:
        print("Filebrowser booting failed.")

