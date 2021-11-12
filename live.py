import os
import sys
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

storage_device = ""
boot_partition = ""
lvm_partition = ""

# General functions
def winput(string):
    return input('\n'.join(textwrap.wrap(string, width = os.get_terminal_size(0)[0], drop_whitespace = False)))


def ask_to_continue():
    print('')
    choice = winput('Continue? (Type 1 for yes or any other key for no) ')
    if choice != '1':
        sys.exit(-1)
    print('')


# Installation functions
def generate_fstab():
    os.system('clear')
    os.system('genfstab -pU /mnt >> /mnt/etc/fstab')
    ask_to_continue()
    os.system('clear')


def run_pacstrap():
    os.system('clear')
    os.system('pacstrap /mnt base base-devel linux linux-firmware openssh git nano')
    ask_to_continue()
    generate_fstab()


def mount_volumes():
    os.system('clear')
    os.system('mount /dev/mapper/archlinux-root /mnt')
    os.system('mkdir /mnt/boot')
    os.system('mount /dev/' + boot_partition + ' /mnt/boot')
    os.system('swapon /dev/mapper/archlinux-swap')
    ask_to_continue()
    run_pacstrap()


def make_filesystems():
    os.system('clear')
    os.system('mkfs.ext4 /dev/mapper/archlinux-root')
    os.system('mkfs.ext4 /dev/mapper/archlinux-extra')
    os.system('mkswap /dev/mapper/archlinux-swap')
    ask_to_continue()
    mount_volumes()


def set_lvm():
    os.system('clear')
    root_partition_size = winput('Set your root logical volume size (192G/96G/...): ')
    os.system('pvcreate /dev/mapper/' + lvm_partition + '-crypt')
    os.system('vgcreate archlinux /dev/mapper/' + lvm_partition + '-crypt')
    os.system('lvcreate -C y -L 8G -n swap archlinux')
    os.system('lvcreate -C n -L ' + root_partition_size + ' -n root archlinux')
    os.system('lvcreate -C n -l 100%FREE -n extra archlinux ')
    ask_to_continue()
    make_filesystems()


def create_luks():
    global boot_partition
    global lvm_partition
    os.system('clear')
    boot_partition = winput('Type your boot partition (sda1/nvme0n1p1/...): ')
    lvm_partition = winput('Type your lvm partition (sda2/nvme0n1p2/...): ')
    os.system('cryptsetup -c aes-xts-plain64 -s 512 -h sha512 luksFormat /dev/' + lvm_partition)
    os.system('cryptsetup luksOpen /dev/' + lvm_partition + ' ' + lvm_partition + '-crypt')
    ask_to_continue()
    set_lvm()


def format_storage_device():
    global storage_device
    os.system('clear')
    os.system('lsblk')
    storage_device = winput('Type your storage device (sda/nvme0n1/...): ')
    os.system('sed -e \'s/\s*\([\+0-9a-zA-Z]*\).*/\\1/\' << EOF | fdisk /dev/' + storage_device + partitioning_string)
    ask_to_continue()
    create_luks()


def install_packages():
    os.system('clear')
    os.system('pacman -Sy nano')
    ask_to_continue()
    format_storage_device()


# Initial functions
def menu():
    os.system('clear')
    print('Select a start point:')
    print('  1. Install nano and git')
    print('  2. Format disk')
    print('  3. Create LUKS partition')
    print('  4. Set LVM')
    print('  5. Make filesystems')
    print('  6. Mount partitions and volumes')
    print('  7. Run pacstrap')
    print('  8. Generate fstab')
    print('')


def init():
    while True:
        menu()
        choice = winput('Type your choice: ')
        if choice == '1':
            install_packages()
        elif choice == '2':
            format_storage_device()
        elif choice == '3':
            create_luks()
        elif choice == '4':
            set_lvm()
        elif choice == '5':
            make_filesystems()
        elif choice == '6':
            mount_volumes()
        elif choice == '7':
            run_pacstrap()
        elif choice == '8':
            generate_fstab()


init()
