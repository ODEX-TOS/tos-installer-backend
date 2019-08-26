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
import filesystem
import bootloader
import helper

# Simple example of how to interact with this api
def GeneralIdea():
    disks = disk.getAllDisks()
    chosenDisk = disks[0] # in a real installer this should be chosen by the user
    pttype = pt.EPartitionTabel.GPT # user should choose this
    
    # Object of the partition table
    table = pt.GenerateDefaultEncryptedTable(chosenDisk, pttype)
    commands = table.generateCommands()

    # Execute the commands
    for command in commands:
        if shell.Command(command).GetReturnCode() != 0:
            break # an error happend when building the partition table

    # Find all partitions that are created
    partitions = disk.getPartitionsByDisk(table.disk)

    # Set the mountpoints and type of the partitions A user should do this

    # Create filesystem for each partition based on type
    for part in partitions:
        filesystem.CreateFilesystem(aprt).makefs()
    
    # Mount our partitions
    mount.Mounter(chosenDisk).mountAll()
    
    # bootstrap filesystemi and generate fstab
    # TODO: implement functionality
    
    # Update mkinitcpio based on the partitions
    encrypted=False
    for part in table.partitions:
        if part.bIsEncrypted:
            encrypted=True
    if encrypted:
        helper.changeLineInFile("^HOOKS.*", "HOOKS=(base udev autodetect modconf block encrypt lvm2 etc)")
    else:
        helper.changeLineInFile("^HOOKS.*", "HOOKS=(base udev autodetect modconf block  lvm2 etc)")

    # chroot into filesystem
    chroot.chroot().start("python3 main.py --chroot-root {}".format(table.type)) # run this script as a chroot user


# This gets ran as a chrooted user
def chroot-root():
   # Add tos repo to pacman.conf
   helper.appendToFile("""
   """, "/etc/pacman.conf") 
    
    packages.Installer(packages=["udev", "linux", "linux-tos"]).exec()
    shell.Command("mkinticpio -p linux").GetReturnCode()
    packages.Installer(packages=["grub"]).exec()
    
    helper.changeLineInFile('^GRUB_DISTRIBUTOR="Arch"$', 'GRUB_DISTRIBUTOR="TOS"')
    helper.removeFiles(["/etc/issue", "/etc/os-release"])

    helper.createFileWithContent("/etc/os-release", """
NAME="Tos Linux"
PRETTY_NAME="Tos Linux"
ID=tos
BUILD_ID=rolling
ANSI_COLOR="0;36"
HOME_URL="https://tos.pbfp.xyz/"
LOGO=toslinux 
    """)


    boot = bootloader.bootloader(partitiontype)
    boot.install()

    packages.Installer(packages=["git", "sudo", "base-devel", "zsh"]).exec()
    shell.Command("echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers").GetReturnCode()

    # ask what the user and password is
    user="alpha"
    password="123"
    
    usr = user.user(user, password, shell="/bin/zsh")
    usr.createUser()

    chroot.chroot(user=user).start("python3 main.py --chroot-user")

# This is ran as the normal user
def chroot-user():
    packages.AURHandler().build() # install yay
    install = packages.Installer(basecommand="yay -Syu --noconfirm")
    install.ExecFromFile("NeededPackages.txt") # install packages per line in the file

    # Custom install such as wayland. This is up to the user

    git.git("https://github.com/ODEX-TOS/tools.git", "bin").init()
    helper.removeFiles(".config")
    git.git("https://github.com/ODEX-TOS/dotfiles.git", ".config").init()
    git.git("https://github.com/ODEX-TOS/Pictures.git", "Pictures").init()

    # install zsh and more


    # setup graphical interface
    helper.appendToFile("xrdb ~/.Xauthority \nexec i3", "~/.xinitrc")


    script.executeExternalScript("multi-installer.sh")

    # Done we have installed everything


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

def CreateUserExample():
    usr= user.user("name", "Password")
    usr.createUser() # create the user <user> with the password <Password>
    usr.createHome() # Create the home directory for the user

