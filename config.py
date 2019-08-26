
# Config file containing default configurations in one place
# You can still override these settings

# Command for installing software
INSTALLCOMMAND="pacman -Syu --noconfirm"


# These AUR configurations are only needed for arch linux based systems
AURHELPER="https://aur.archlinux.org/yay.git"
AURHELPERDIR="yay"

# Packagename for git on your distro
GITPACKAGE="git"

# IP to check if network is working
IP="8.8.8.8"

# command to interactivaly connect to wifi
WIFI-CONNECT-COMMAND="wifi-menu"

# command to connect to wifi based on a password first {} is the SSID the second {} is the password
WIFI-CONNECT-COMMAND-WITH-PASSWORD="nmcli device wifi connect '{}' password '{}'"

# Default shell for new users
DEFAULT_SHELL="/bin/bash"

# Command to add users| first {} is the encrypted password, second {} are all the groups, third {} is the default shell, fourth {} is the username
USERADD="useradd -m -p {} -g users -G {} -s {} {}"

# Default groups a new user is in
GROUPS=["audio", "lp", "optical", "storage", "video", "wheel", "games", "power"]

# command to generate a new users home dir
USER_HOME_BUILDER="mkhomedir_helper {}"
