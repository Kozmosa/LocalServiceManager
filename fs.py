import socket
import os
import subprocess
import configparser
import services

# global vars and config
configPath = 'fsconfig.ini'
dev = True

# bootloader
# 0 for os.system, 1 for subprocess

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

# main program
def main():
    ip = get_ip()

    # useConf = str(input("Use config file?(0 for N, else for Y):"))


    # if useConf == 0:
    #     print("Have detected host ip address: " + str(ip) + ", do you agreed to use this address as host ip?")
    #     choice = str(input("(0 for N, else for Y):"))
    #     if choice == '0':
    #         content = os.system("ipconfig")
    #         print("ipconfig command returned that: \n" + content + "\n")
    #         ip = str(input("Please enter an ip address instead:"))
    #     else:
    #         print("IP confirmed.")

    #     choice = ''
    #     choice = str(input('Using 80 port for file server as default, do you agree with that? (0 for N, else for Y):'))
    #     if choice == '0':
    #         port = str(input('Enter an port instead:'))
    #     else:
    #         port = '80'
    # else:
    con = readConfig(configPath)
    sections = con.sections()
    instances = []
    try:
        for section in sections:
            config = dict(con.items(section))
            if section == 'filebrowser':
                instances.append(services.filebrowser(port=config['port'], path=config['path'], ip=ip))
            elif section == 'alist':
                instances.append(services.alist(port=config['port'], path=config['path'], ip=ip))
            else:
                continue
    except Exception:
        pass
    
    # booting instances
    for instance in instances:
        instance.boot()
        print("Service `" + instance.getName() + '` was running on ' + str(instance.ip) + ':' + str(instance.port) + ', whose pid is ' + str(instance.pid) + '.')
    return 0

    