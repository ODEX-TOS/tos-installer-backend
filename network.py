import shell
import socket
import config

# Check if we have a network connection. If we don't try to establish one
class Connector:
    def __init__(self):
        self.bIsConnected = self.HasNetwork()

    def HasNetwork(self, host=config.IP, port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            print(ex)
        return False

    def establishConnectionCommand(self, command=config.WIFI_CONNECT_COMMAND):
        obj=shell.Command(command).GetReturnCode()
        self.bIsConnected = self.HasNetwork()

    def establishConnection(self, ssid, password, command=config.WIFI_CONNECT_COMMAND_WITH_PASSWORD):
        res=shell.Command(command.format(ssid, password)).GetStdout()
        self.bIsConnected = self.HasNetwork()
        return res

