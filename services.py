from configparser import *
import os
import subprocess
import signal

class service:
    def __init__(self, path, ip, port, configFile=None):
        self.path = path
        self.ip = ip
        self.port = port
        self.otherConfig = {}
        self.otherConfigString = ''
        self.configFile = configFile
        self.command = ''
        self.bootloader = 1
        self.dev = True
        # self.proc = subprocess instance
        # self.pid = subprocess pid

        self.generateCommand()

        if configFile != None:
            self.loadConfig(configFile)
        

    def loadConfig(self):
        try:
            con = ConfigParser()
            con.read(self.configFile, 'utf-8')
            sections = con.sections()
            config = {}
            for section in sections:
                config[str(section)] = dict(con.items(str(section)))
            
            self.otherConfig = config
        except Exception:
            pass
    

    def generateCommand(self):
        self.command = ''
        pass

    def boot(self):
        if self.bootloader == 0:
            try:
                os.system(self.command)
                if self.dev:
                    print("Bootloader 0 succeeded.")
                return 0
            except Exception:
                return 1
        elif self.bootloader == 1:
            try:
                self.proc = subprocess.Popen(
                    self.command,
                    stdin=None,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True
                )
                self.pid = self.proc.pid
                outinfo, errinfo = self.proc.communicate()
                if dev:
                    print(outinfo.decode('utf-8'))
                    print(errinfo.decode('utf-8'))
                    print("Bootloader 1 succeeded.")
                return 0
            except Exception:
                return 1
        else:
            return 1

    def stop(self, osType="linux"):
        # stop process based on pid
        if osType == 'linux':
            try:
                os.kill(self.pid, signal.SIGINT)
                return 0
            except Exception:
                return 1
        elif osType == 'windows':
            try:
                killCommand = 'taskkill /f /pid %s' % str(self.pid)
                return 0
            except Exception:
                return 1

class filebrowser(service):
    def generateCommand(self):
        self.command = self.path + ' -p ' + self.port + ' -a ' + self.ip

class alist(service):
    def generateCommand(self):
        self.command = self.path + ' server'