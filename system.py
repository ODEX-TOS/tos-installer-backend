import shell
import config
# TODO: add localtime generator
# shell command is as followed ln -sf /usr/share/zoneinfo/"$continent"/"$capital" /etc/localtime
# where $continent is in  /usr/share/zoneinfo/*
# where $capital is in /usr/share/continent/*


class system:
    def __init__(self, locale=config.LOCALE, keymap=config.KEYMAP, hostname=config.HOSTNAME, password_root=config.ROOT_PWD):
        self.locale = locale
        self.keymap = keymap
        self.hostname = hostname
        self.password_root = password_root

    def setup(self):
        commands = [
            "timedatectl set-ntp true",
            "location-generator",
            "hwclock --systohc",
            "sed -i 's:^#.*{}:{}' /etc/locale.gen".format(
                self.locale, self.locale),
            "locale-gen",
            "echo 'LANG={}' > /etc/locale.conf".format(self.locale),
            "echo KEYMAP='{} > /etc/vconsole.conf".format(self.keymap),
            "echo '{}' > /etc/hostname".format(self.hostname),
            "echo -e '127.0.0.1   localhost\n::1      localhost\n127.0.1.1    {}.localdomain  {}' > /etc/hosts".format(
                self.hostname, self.hostname),
            "passwd < {}".format(self.password_root),
            "echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers"
        ]
        return commands


# TODO: return all locals
def getAllLocals():
    return

# TODO: return all keymaps


def getAllKeyMaps():
    return
