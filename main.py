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


disks=disk.getAllDisks()
for dsk in disks:
    print(dsk.toString())
    print("")
