import os
import sys
import textwrap

hosts_string = '''
127.0.0.1    localhost
::1          localhost
127.0.1.1    
'''

# General functions
def winput(string):
    return input('\n'.join(textwrap.wrap(string, width = os.get_terminal_size(0)[0], drop_whitespace = False)))


def ask_to_continue():
    print('')
    choice = winput('Continue? (Type 1 for yes or any other key for no) ')
    if (choice != '1'):
        sys.exit(-1)
    print('')


# Installation functions
def set_user():
    os.system('clear')
    os.system('passwd')
    username = winput('Type your username (kate | lucas | ana | ...): ')
    os.system('useradd -mG wheel ' + username)
    os.system('passwd ' + username)
    ask_to_continue()


def install_base_packages():
    os.system('clear')
    os.system('pacman -Sy os-prober grub efibootmgr networkmanager wireless_tools wpa_supplicant dialog linux-headers xdg-utils xdg-user-dirs lvm2')
    ask_to_continue()
    set_user()


def set_host():
    os.system('clear')
    hostname = winput('Type your hostname (arch | my-linux | home-desktop | ...): ')
    os.system('echo ' + hostname + ' >> /etc/hostname')
    os.system('echo "' + hosts_string + hostname + '.localdomain ' + hostname + '" >> /etc/hosts')
    ask_to_continue()
    install_base_packages()


def set_locale():
    os.system('clear')
    locale = winput('Type your locale (en_US | pt_BR | ...): ')
    os.system('mv /etc/locale.gen /etc/locale.gen.backup')
    os.system('echo "' + locale + '.UTF-8 UTF-8" >> /etc/locale.gen')
    os.system('locale-gen')
    os.system('echo LANG=' + locale + '.UTF-8 >> /etc/locale.conf')
    print('')
    layout = winput('Set up your keyboard layout (us | br-abnt2 | ...): ')
    os.system('echo KEYMAP=' + layout + ' >> /etc/vconsole.conf')
    ask_to_continue()
    set_host()


def set_timezone():
    os.system('clear')
    timezone = winput('Type your timezone (America/New_York | America/Sao_Paulo | Europe/Berlim | ...): ')
    os.system('ln -sf /usr/share/zoneinfo/' + timezone + ' /etc/localtime')
    os.system('hwclock --systohc')
    ask_to_continue()
    set_locale()


set_timezone()
