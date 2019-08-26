import shell
import config
# TODO: add default system settings eg sync time, setup root, local generator etc

class system:
    def __init__(locale=config.LOCALE, keymap=config.KEYMAP, hostname=config.HOSTNAME, password_root=config.ROOT_PWD):
        self.locale = locale
        self.keymap = keymap
        self.hostname = hostname
        self.password_root = password_root

# TODO: return all locals
def getAllLocals():
    return

# TODO: return all keymaps
def getAllKeyMaps():
    return

