
# Config file containing default configurations in one place
# You can still override these settings

# Command for installing software
INSTALLCOMMAND = "pacman -Syu --noconfirm"


# IP to check if network is working
IP = "8.8.8.8"

# command to interactivaly connect to wifi
WIFI_CONNECT_COMMAND = "wifi-menu"

# command to connect to wifi based on a password first {} is the SSID the second {} is the password
WIFI_CONNECT_COMMAND_WITH_PASSWORD = "nmcli device wifi connect '{}' password '{}'"

# Default shell for new users
DEFAULT_SHELL = "/bin/bash"

# Command to add users| first {} is the encrypted password, second {} are all the groups, third {} is the default shell, fourth {} is the username
USERADD = "useradd -m -p {} -g users -G {} -s {} {}"

# Default groups a new user is in
GROUPS = ["audio", "lp", "optical", "storage",
          "video", "wheel", "games", "power"]

# command to generate a new users home dir
USER_HOME_BUILDER = "mkhomedir_helper {}"

# Default mount point
MOUNTPOINT = "/mnt"


# Install command for the bootloader
BOOTLOADER_EFI = "grub-install --efi-directory /boot/efi --force {}"
BOOTLOADER_DOS = "grub-install --root-directory=/boot {}"
BOOTLOADER_CONFIG = "grub-mkconfig -o /boot/grub/grub.cfg"

# default system setting
LOCALE = "en_US.UTF-8"
KEYMAP = "be-latin1"
HOSTNAME = "tos"
ROOT_PWD = "123"


# chroot command
CHROOT = "cat | arch-chroot -u {} {}"


# Logic volume/encryption
LUKS = "cryptsetup luksFormat -v -s 512 -h sha512 {}"
LUKS_OPEN = "cryptsetup open {} luks_lvm"
LUKS_NAME = "tos"  # the volume group name
LUKS_DEVICE = "/dev/mapper/luks_lvm"  # luks_lvm must be the same as LUKS_OPEN

# fstab generator
FSTAB = "genfstab -U -p {} > {}/etc/fstab".format(MOUNTPOINT, MOUNTPOINT)

HERESTRING = "EOF"

BOOTSTRAP = "pacstrap /mnt {} --noconfirm"

BOOTSTRAP_PACKAGES = ["base", "base-devel",
                      "efibootmgr", "vim", "dialog", "grub"]
