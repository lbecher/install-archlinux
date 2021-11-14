import os
import sys
import textwrap

fdisk_partition_disk_string = '''
g
n
1

+1024M
y
n
2


y
t
1
1
w
EOF
'''

storage_device = ''

boot_partition = ''
lvm_partition = ''

swap_partition_enable = ''
home_partition_enable = ''
lfs_partition_enable = ''

swap_partition_size = ''
home_partition_size = ''
lfs_partition_size = ''

# General functions
def winput(string):
    return input('\n'.join(textwrap.wrap(string, width = os.get_terminal_size(0)[0], drop_whitespace = False)))


def ask_to_continue():
    print('')
    choice = winput('Continue? (Type 1 for yes or any other key for no) ')
    if (choice != '1'):
        sys.exit(-1)
    print('')


# Getting storage informations from user
def get_storage_device():
    global storage_device
    global boot_partition
    global lvm_partition
    os.system('clear')
    os.system('lsblk')
    storage_device = winput('Type your storage device (sda|nvme0n1|...): ')
    if (storage_device[0:3] == 'nvme'):
        boot_partition = storage_device + 'p1'
        lvm_partition = storage_device + 'p2'
    else:
        boot_partition = storage_device + '1'
        lvm_partition = storage_device + '2'
    print('Boot partition: /dev/' + boot_partition)
    print('LVM partition:  /dev/' + lvm_partition)
    ask_to_continue()


def get_logical_volumes_configuration():
    global swap_partition_enable
    global home_partition_enable
    global lfs_partition_enable
    global swap_partition_size
    global home_partition_size
    global lfs_partition_size
    os.system('clear')
    swap_partition_enable = winput('Do you want to have a dedicated logical volume to swap? (Type 1 for yes or any other key for no) ')
    if (swap_partition_enable == '1'):
        swap_partition_size = winput('Set your swap logical volume size (4G/8G/...): ')
    home_partition_enable = winput('Do you want to have a dedicated logical volume to home? (Type 1 for yes or any other key for no) ')
    if (home_partition_enable == '1'):
        home_partition_size = winput('Set your home logical volume size (64G/128G/...): ')
    lfs_partition_enable = winput('Do you want to have a dedicated logical volume to build a Linux From Scratch project? (Type 1 for yes or any other key for no) ')
    if (lfs_partition_enable == '1'):
        lfs_partition_size = winput('Set your lfs logical volume size (16G/24G/...): ')
    ask_to_continue()


# Installation functions
def generate_fstab():
    os.system('clear')
    os.system('genfstab -pU /mnt >> /mnt/etc/fstab')
    ask_to_continue()
    os.system('clear')


def run_pacstrap():
    os.system('clear')
    os.system('pacstrap /mnt base base-devel linux linux-firmware openssh git nano python3')
    ask_to_continue()
    generate_fstab()


def mount_volumes():
    if (storage_device == ''):
        get_storage_device()
    if (swap_partition_enable == ''):
        get_logical_volumes_configuration()
    os.system('clear')
    os.system('mount /dev/mapper/archlinux-root /mnt -v')
    os.system('mkdir /mnt/boot -v')
    os.system('mount /dev/' + boot_partition + ' /mnt/boot -v')
    if (swap_partition_enable == '1'):
        os.system('swapon /dev/mapper/archlinux-swap -v')
    if (home_partition_enable == '1'):
        os.system('mkdir /mnt/home -v')
        os.system('mount /dev/mapper/archlinux-home /mnt/home -v')
    ask_to_continue()
    run_pacstrap()


def set_lvm_and_filesystems():
    if (storage_device == ''):
        get_storage_device()
    if (swap_partition_enable == ''):
        get_logical_volumes_configuration()
    os.system('clear')
    os.system('pvcreate /dev/mapper/' + lvm_partition + '-crypt')
    os.system('vgcreate archlinux /dev/mapper/' + lvm_partition + '-crypt')
    if (swap_partition_enable == '1'):
        os.system('lvcreate -C y -L ' + swap_partition_size + ' -n swap archlinux')
        os.system('mkswap /dev/mapper/archlinux-swap')
    if (home_partition_enable == '1'):
        os.system('lvcreate -C y -L ' + home_partition_size + ' -n home archlinux')
        os.system('mkfs.ext4 /dev/mapper/archlinux-home')
    if (lfs_partition_enable == '1'):
        os.system('lvcreate -C n -L ' + lfs_partition_size + ' -n lfs archlinux')
        os.system('mkfs.ext4 /dev/mapper/archlinux-lfs')
    os.system('lvcreate -C n -l 100%FREE -n root archlinux')
    os.system('mkfs.ext4 /dev/mapper/archlinux-root')
    os.system('mkfs.vfat -F32 /dev/' + boot_partition)
    ask_to_continue()
    make_filesystems()


def create_luks():
    if (lvm_partition == ''):
        get_storage_device()
    os.system('clear')
    os.system('cryptsetup -c aes-xts-plain64 -s 512 -h sha512 luksFormat /dev/' + lvm_partition)
    os.system('cryptsetup luksOpen /dev/' + lvm_partition + ' ' + lvm_partition + '-crypt')
    ask_to_continue()
    set_lvm()


def format_storage_device():
    if (storage_device == ''):
        get_storage_device()
    os.system('clear')
    os.system('sed -e \'s/\s*\([\+0-9a-zA-Z]*\).*/\\1/\' << EOF | fdisk /dev/' + storage_device + fdisk_partition_disk_string)
    ask_to_continue()
    create_luks()


def set_keyboard_layout():
    os.system('clear')
    layout = winput('Set your keyboard layout (us|uk|br-abnt2): ')
    os.system('loadkeys ' + layout)
    ask_to_continue()
    format_storage_device()


# Initial functions
def menu():
    os.system('clear')
    print('Select a start point:')
    print('  1. Set keyboard layout')
    print('  2. Format disk')
    print('  3. Create LUKS partition')
    print('  4. Set LVM')
    print('  5. Make filesystems')
    print('  6. Mount partitions and volumes')
    print('  7. Run pacstrap')
    print('  8. Generate fstab')
    print('')


def init():
    os.system('clear')
    while True:
        menu()
        choice = winput('Type your choice: ')
        if choice == '1':
            set_keyboard_layout()
        elif choice == '2':
            format_storage_device()
        elif choice == '3':
            create_luks()
        elif choice == '4':
            set_lvm_and_filesystems()
        elif choice == '5':
            mount_volumes()
        elif choice == '6':
            run_pacstrap()
        elif choice == '7':
            generate_fstab()


init()
