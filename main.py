import argparse
import model.model.partition as partition
import model.model.disk as disk
import model.gen.disk as gen
import model.build.disk as builder

disks = gen.getAllDisks()

for dsk in disks:
    print(dsk.toString())


partitions = []
partitions.append(partition.partition("/dev/sda1", "efi",
                                      "/boot/efi", "fat32", "1MiB", "200MiB"))
partitions.append(partition.partition("/dev/sda2", "boot",
                                      "/boot", "ext4", "200MiB", "800MiB"))
partitions.append(partition.partition(
    "/dev/sda3", "swap", "", "swap", "800MiB", "8GiB"))
partitions.append(partition.partition(
    "/dev/sda4", "root", "/", "ext4", "8GiB", "100%"))


ptabledisk = disk.disk("/dev/sda", "466G", partitions, False)

table = builder.buildPartitionTable(ptabledisk)

for command in table:
    print(command)
