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

#disks=disk.getAllDisks()
#for dsk in disks:
#    print(dsk.toString())
#    print("")

parts = []
parts.append(pt.PartitionInfo("boot", True, "1MiB", "200MiB", False))
parts.append(pt.PartitionInfo("lvm", False, "800MiB", "100%", False))

table = pt.PartitionTable(pt.EPartitionTabel.MSDOS, "/dev/sda", parts)

commands = table.generateCommand()

for command in commands:
    print(command)
