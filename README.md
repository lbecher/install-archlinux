# install-archlinux (incomplete)
Scripts to install Arch Linux with LVM and UEFI.

## live.py (done)
Script to be runned in the live mode. Follow the step by step:

1. Configure the internet connection as described in the [official installation guide](https://wiki.archlinux.org/title/Installation_guide).

2. Install git and python3.

```
pacman -Sy git python3
```

3. clone this repository.

```
git clone https://github.com/lbecher/install-archlinux.git
```

## arch-chroot.py (not created yet)
Script to be runned in the root of your installation (also in the live mode).


## after-reboot.py (not created yet)
Script to be runned into your installation after reboot.
