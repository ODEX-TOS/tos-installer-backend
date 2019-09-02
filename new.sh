
#Building partition table
parted --script '/dev/sda' mklabel gpt
parted --script '/dev/sda' mkpart ESP fat32 1MiB 200MiB
parted --script '/dev/sda' set 1 boot on
parted --script '/dev/sda' name 1 efi
parted --script '/dev/sda' mkpart primary 200MiB 8GiB
parted --script '/dev/sda' name 2 swap
parted --script '/dev/sda' mkpart primary 8GiB 100%
parted --script '/dev/sda' set 3 lvm on
parted --script '/dev/sda' name 3 root

#Formating partitions
mkfs.fat -I -F32 /dev/sda1
mkfs.ext4 -F /dev/sda2
modprobe dm-crypt
modprobe dm-mod
printf 'a' | cryptsetup luksFormat -v -s 512 -h sha512 /dev/sda3 -d -
printf 'a' | cryptsetup open /dev/sda3 luks_lvm -d -
pvcreate /dev/mapper/luks_lvm
vgcreate tos /dev/mapper/luks_lvm
lvcreate -n root -L 200G tos
lvcreate -n home -L 200G tos
mkfs.ext4 -L root /dev/mapper/tos-root
mkfs.ext4 -L home /dev/mapper/tos-home

#Formating partitions
mkfs.fat -I -F32 /dev/sda1

#Mounting partitions
mount /dev/mapper/tos-root /mnt/
mkdir -p /mnt/home
mount /dev/mapper/tos-home /mnt/home
mkdir -p /mnt/boot/efi
mount /dev/sda1 /mnt/boot/efi
swapon /dev/sda2
swapon -a
swapon -s

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
sed -i "s;^GRUB_CMDLINE_LINUX_DEFAULT=.*;GRUB_CMDLINE_LINUX_DEFAULT=\"quiet cryptdevice=/dev/sda3:luks_lvm\";" /etc/default/grub
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
echo hello 2


EOF2
EOF

# Executing custom script
 echo hello world
echo hello 2

