import shell
import socket
import config
import os
import sys
sys.path.append("...")  # set all imports to root imports


class Connector:
    """
    A connector object holds the current network connection
    If there is no connection. We will try to make a network connection
    If there is a connection it will simply return that state
    """

    def __init__(self):
        self.bIsConnected = self.HasNetwork()

    def HasNetwork(self, host=config.IP, port=53, timeout=3):
        """
        Access the network and see if a connection exists
        This discards DNS requests and focuses entirely on ip packets
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (host, port))
            return True
        except socket.error as ex:
            print(ex)
        return False

    def establishConnectionCommand(self, command=config.WIFI_CONNECT_COMMAND):
        """
        Try to interactivaly make a connection
        """
        obj = shell.Command(command).GetReturnCode()
        self.bIsConnected = self.HasNetwork()

    def establishConnection(self, ssid, password, command=config.WIFI_CONNECT_COMMAND_WITH_PASSWORD):
        """
        Try to make a basic network connection by ssid, password
        """
        res = shell.Command(command.format(ssid, password)).GetStdout()
        self.bIsConnected = self.HasNetwork()
        return res

    def getShellCommand(self, ssid, password, command=config.WIFI_CONNECT_COMMAND_WITH_PASSWORD, config=None):
        commands = [
            "if [[ $(ping -c1 {} | grep '0% packet loss') == '' ]]; then".format(config["IP"])]
        commands.append("\t"+command.format(ssid, password))
        commands.append("fi")
        return commands

    # TODO: implement a ethernet connection interface eg for PPPoE
