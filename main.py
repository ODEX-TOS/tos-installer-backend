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
print(swb.installSoftware(software))


print("\n\n# generating fstab")
print(script.script(payload=config.FSTAB).payload)

print("\n\n# chrooting as root")
print(chroot.chroot().start(command=["echo hello world", "echo hi"]))
