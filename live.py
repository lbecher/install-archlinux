import os
import textwrap

partitioning_string = '''
o
n
p
1

+1024M
n
p
2


a
1
p
w
q
EOF
'''

def winput(s):
    return input('\n'.join(textwrap.wrap(s, width = os.get_terminal_size(0)[0], drop_whitespace = False)))


def ask_to_continue():
    print('')
    choice = winput('Continue? (Type 1 for yes or any other key for no) ')
    if choice != '1':
        sys.exit(-1)
    print('')


def init():
    os.system('clear')
    print('Select a start point:')
    print('  1. Install nano and git')
    print('  2. Set keys, locale and update date and time')
    print('  3. Format disk')
    print('  4. Install nano')


init()

os.system('pacman -Sy nano')

ask_to_continue()

os.system('loadkeys br-abnt2')
os.system('nano /etc/locale.gen')
os.system('timedatectl set-ntp true')

ask_to_continue()

os.system('lsblk')
storage_device = winput('Type your storage device (sda/nvme0n1/...): ')
os.system('sed -e \'s/\s*\([\+0-9a-zA-Z]*\).*/\\1/\' << EOF | fdisk /dev/' + storage_device + partitioning_string)

ask_to_continue()

boot_partition = winput('Type your boot partition (sda1/nvme0n1p1/...): ')
lvm_partition = winput('Type your lvm partition (sda2/nvme0n1p2/...): ')
os.system('cryptsetup -c aes-xts-plain64 -s 512 -h sha512 luksFormat /dev/' + lvm_partition)
os.system('cryptsetup luksOpen /dev/' + lvm_partition + ' ' + lvm_partition + '-crypt')

ask_to_continue()

os.system('pvcreate /dev/mapper/' + lvm_partition + '-crypt')
os.system('vgcreate archlinux /dev/mapper/' + lvm_partition + '-crypt')
os.system('lvcreate -C y -L 8G -n swap archlinux')
os.system('lvcreate -C n -L ' + root_partition_size + ' -n root archlinux'')
os.system('lvcreate -C n -l 100%FREE -n lfs archlinux ')

ask_to_continue()

os.system('mkfs.ext4 /dev/mapper/archlinux-root')
os.system('mkfs.ext4 /dev/mapper/archlinux-lfs')
os.system('mkswap /dev/mapper/archlinux-swap')

ask_to_continue()

