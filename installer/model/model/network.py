
# MIT License
# 
# Copyright (c) 2019 Meyers Tom
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import installer.shell as shell
import socket
import installer.config as config
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
