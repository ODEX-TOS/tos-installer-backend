import argparse


import chroot
import disk
import encryption
import git
import mount
import network
import packages
import partition
import shell
import user
import partitiontable as pt
import script


# Example on how to read the disk
def diskExample():
    disks=disk.getAllDisks()
    for dsk in disks:
        print(dsk.toString())
        print("")


def PartitionTableGenExample():
    parts = []
    parts.append(pt.PartitionInfo("boot", True, "1MiB", "200MiB", False))
    parts.append(pt.PartitionInfo("lvm", False, "800MiB", "100%", False))

    table = pt.PartitionTable(pt.EPartitionTabel.MSDOS, "/dev/sda", parts)

    commands = table.generateCommand()

    for command in commands:
        print(command)

def defaultPartitions():
    table = pt.GenerateDefaultEncryptedTable("/dev/sda", pt.EPartitionTabel.GPT)

    commands = table.generateCommand()

    for command in commands:
        print(command)

def SourceScriptExample():
    print(script.executeExternalScript("shell.sh"))

def NetworkConnectExample():
    connection = network.Connector()
    print("Do we have a network connection {}".format(connection.bIsConnected))
    if not connection.bIsConnected:
        connection.establishConnectionCommand()
        print("Do we have a network connection {}".format(connection.bIsConnected))
    if not connection.bIsConnected:
        connection.establishConnection("ssid", "password")
        print("Do we have a network connection {}".format(connection.bIsConnected))

defaultPartitions()
