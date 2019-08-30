import argparse
import config
import model.model.partition as partition
import model.model.disk as disk
import model.gen.disk as gen
import model.build.disk as builder
import model.build.partition as pb
import model.build.mount as mb
import model.build.encryption as e
import model.model.software as sw
import model.build.software as swb
import model.model.script as script
import model.model.chroot as chroot
import model.model.user as user
import model.build.user as userb
import parser.parse as parse
import system
from converter import convertYamlToCommands


def concat(list1, list2):
    newlist = list1
    for item in list2:
        newlist.append(item)
    return newlist


def functionExample():
    disks = gen.getAllDisks()

    for dsk in disks:
        print(dsk.toString())

    volumes = []
    volumes.append(partition.logicvolume("root", "200G", "/home"))
    volumes.append(partition.logicvolume("home", "200G", "/"))

    partitions = []
    partitions.append(partition.partition("/dev/sda1", "efi",
                                          "/boot/efi", "fat32", "1MiB", "200MiB"))
    partitions.append(partition.partition("/dev/sda2", "boot",
                                          "/boot", "ext4", "200MiB", "800MiB"))
    partitions.append(partition.partition(
        "/dev/sda3", "swap", "swap", "ext4", "800MiB", "8GiB"))
    partitions.append(partition.partition(
        "/dev/sda4", "root", "/", "luks", "8GiB", "100%", True, volumes))

    ptabledisk = disk.disk("/dev/sda", "466G", partitions, False)

    table = builder.buildPartitionTable(ptabledisk)

    print("# build partition table")
    # build partition table
    for command in table:
        print(command)

    print("\n\n# format the partitions")

    # format partitions
    for part in partitions:
        for command in pb.format(part):
            print(command)

    print("\n\n# mount the partitions")
    # mount partitions
    mounts = mb.mountAll(partitions)
    for command in mounts:
        print(command)

    print("\n\n# bootstrapping base system")
    software = sw.software("pacstrap --noconfirm /mnt", packages=[
        "base", "base-devel", "efibootmgr", "vim", "dialog", "xterm", "grub"])
    for command in swb.installSoftware(software):
        print(command)

    print("\n\n# generating fstab")
    print(script.script(payload=config.FSTAB).payload)

    # preparing all the chroot commands

    usr = user.user("alpha", "123")
    usercommands = concat(swb.installSoftware(sw.software(
        packages=["git", "sudo", "base-devel", "zsh"])), userb.makeUnixUser(usr))

    rootcommands = concat(system.system().setup(),
                          ["printf '[tos]\nSigLevel = Optional TrustAll\nServer = https://repo.pbfp.xyz\n' >> /etc/pacman.conf"])
    rootcommands = concat(rootcommands, usercommands)
    # add mkinitcpio commands to the root commands
    # add bootloader commands to the root commands
    rootcommands = concat(rootcommands, script.bootloader(shell="",
                                                          device=ptabledisk.device, bIsGPT=ptabledisk.bIsGPT).exec())

    # install yay

    # install software
    softwarecommands = swb.installSoftware(sw.software(
        packages=["a", "b", "c", "d"]))

    print("\n\n# chrooting as root")
    print(chroot.chroot().start(command=rootcommands))

    print("\n\n# chrooting as user")
    print(chroot.chroot(user="alpha").start(command=softwarecommands))


def configExample():
    parsed = parse.parse("parser/example.yaml").execution
    commands = convertYamlToCommands(parsed)

    for command in commands:
        print(command)


configExample()
