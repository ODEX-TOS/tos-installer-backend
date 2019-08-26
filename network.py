import shell
import socket

# Check if we have a network connection. If we don't try to establish one
class Connector:
    def __init__(self):
        self.bIsConnected = self.HasNetwork()

    def HasNetwork(self, host="8.8.8.8", port=53, timeout=3):
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            print(ex)
        return False

    def establishConnectionCommand(self, command="wifi-menu"):
        obj=shell.Command(command).GetReturnCode()
        self.bIsConnected = self.HasNetwork()

    def establishConnection(self, ssid, password, command="nmcli device wifi connect '{}' password '{}'"):
        res=shell.Command(command.format(ssid, password)).GetStdout()
        self.bIsConnected = self.HasNetwork()
        return res

