
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

#Building partition table
parted --script '/dev/sda' mkpart ESP fat32 1MiB 200MiB
parted --script '/dev/sda' set 1 boot on
parted --script '/dev/sda' name 1 efi
parted --script '/dev/sda' mkpart primary 200MiB 800MiB
parted --script '/dev/sda' name 2 boot
parted --script '/dev/sda' mkpart primary 800MiB 8GiB
parted --script '/dev/sda' name 3 swap
parted --script '/dev/sda' mkpart primary 8GiB 98%
parted --script '/dev/sda' set 4 lvm on
parted --script '/dev/sda' name 4 root
parted --script '/dev/sda' mkpart primary 97% 99%
parted --script '/dev/sda' name 8 offset
parted --script '/dev/sda' resizepart 9 1GB

#Formating partitions
mkfs.fat -I -F32 /dev/sda1
mkfs.ext4 -F /dev/sda2
mkfs.ext4 -F /dev/sda3
modprobe dm-crypt
modprobe dm-mod
printf 'a' | cryptsetup luksFormat -v -s 512 -h sha512 /dev/sda4 -d -
printf 'a' | cryptsetup open /dev/sda4 luks_lvm -d -
pvcreate /dev/mapper/luks_lvm
vgcreate tos /dev/mapper/luks_lvm
lvcreate -n root -L 200G tos
lvcreate -n home -L 200G tos
mkfs.ext4 -L root /dev/mapper/tos-root
mkfs.ext4 -L home /dev/mapper/tos-home
mkfs.ext4 -F /dev/sda8
mkfs.ext4 -F /dev/sda9

#Formating partitions
mkfs.fat -I -F32 /dev/sda1

#Mounting partitions
mount /dev/mapper/tos-root /mnt/
mkdir -p /mnt/home
mount /dev/mapper/tos-home /mnt/home
mkdir -p /mnt/boot
mount /dev/sda2 /mnt/boot
mkdir -p /mnt/boot/efi
mount /dev/sda1 /mnt/boot/efi
swapon /dev/sda3
swapon -a
swapon -s
mkdir -p /mnt/tmp
mount /dev/sda8 /mnt/tmp
mkdir -p /mnt/proc
mount /dev/sda9 /mnt/proc

#Establishing a network connection
if [[ $(ping -c1 8.8.8.8 | grep '0% packet loss') == '' ]]; then
	nmcli device wifi connect 'ssid' password 'passphrase'
fi

#bootstrapping system
pacstrap /mnt base base-devel efibootmgr vim dialog grub  --noconfirm

# Generate fstab
genfstab -U -p /mnt > /mnt/etc/fstab

# Executing chroot function
arch-chroot -u root /mnt <<EOF

# Setting up system parameters
timedatectl set-ntp true
hwclock --systohc
sed -i 's:^#.*en_US.UTF-8:en_US.UTF-8:' /etc/locale.gen
locale-gen
echo 'LANG=en_US.UTF-8' > /etc/locale.conf
echo KEYMAP='be-latin1' > /etc/vconsole.conf
echo 'tos' > /etc/hostname
echo -e '127.0.0.1   localhost
::1      localhost
127.0.1.1    tos.localdomain  tos' > /etc/hosts
echo 'root:123' | chpasswd
echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
pacman -Syu --noconfirm linux 

# Creating a user
useradd -m -p paN8aiEIonqJE -g users -G audio,lp,optical,storage,video,wheel,games,power -s /bin/bash alpha

# Generating the bootloader
sed -i 's:HOOKS=(\(.*\)):HOOKS=(\1 encrypt lvm2):' /etc/mkinitcpio.conf
sed -i "s;^GRUB_CMDLINE_LINUX_DEFAULT=.*;GRUB_CMDLINE_LINUX_DEFAULT=\"quiet cryptdevice=/dev/sda4:luks_lvm\";" /etc/default/grub
sed -i "s/^#GRUB_ENABLE_CRYPTODISK=y/GRUB_ENABLE_CRYPTODISK=y/" /etc/default/grub
mkinitcpio -p linux
grub-install --efi-directory /boot/efi --force /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg

EOF

# Executing chroot function
arch-chroot -u root /mnt <<EOF
su alpha <<\EOF2

# Installing software
yay -Syu --noconfirm linux grep vim linux-tos sudo nano 

# Executing custom script
 echo hello world
echo hello 2 \$USER


EOF2
EOF

# Executing custom script
 echo hello world
echo hello 2 $USER

