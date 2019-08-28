## model/*
A representation of the object eg partitions have a name, filesystem, size, mountpoint etc
Make a simple model that doesn't have any functionality

## shell.py
A utility to interface with the system command line

## gen/*
Uses a model and make it possible to generate them
eg partition.py -> generates a partition model from something such as generate partition based on mount point.
eg disk.py -> generates a disk model from something such as a filelocation or generate an array of all detected disks
eg user.py -> generate a user based on some settings

## build/*
Do something with a given model
eg disk.py -> build a partition table based on a disk model
eg user.py -> build a unix user based on the user model

