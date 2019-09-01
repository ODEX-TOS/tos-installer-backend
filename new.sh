
#Building partition table
parted --script '/dev/sda' mklabel msdos
parted --script '/dev/sda' mkpart primary 1MiB 200MiB
parted --script '/dev/sda' set 1 boot on
parted --script '/dev/sda' name 1 boot
parted --script '/dev/sda' mkpart primary 200MiB 100%
parted --script '/dev/sda' name 2 root

#Formating partitions
mkfs.ext4 -F /dev/sda1
mkfs.ext4 -F /dev/sda2

#Mounting partitions
mount /dev/sda2 /mnt
mkdir -p /mnt/boot
mount /dev/sda1 /mnt/boot

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
echo 'arch' > /etc/hostname
echo -e '127.0.0.1   localhost
::1      localhost
127.0.1.1    arch.localdomain  arch' > /etc/hosts
echo 'root:123' | chpasswd
echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
pacman -Syu --noconfirm linux 

# Creating a user
useradd -m -p paN8aiEIonqJE -g users -G audio,lp,optical,storage,video,wheel,games,power -s /bin/bash alpha

# Generating the bootloader
mkinitcpio -p linux
grub-install /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg

EOF
