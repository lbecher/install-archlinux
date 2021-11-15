# install-archlinux (incomplete)
Scripts to install Arch Linux with LVM and UEFI.

## live.py (done)
Script to be runned in the live mode. Follow the step by step:

1. Configure the internet connection as described in the [official installation guide](https://wiki.archlinux.org/title/Installation_guide).

2. Install git and python3.

```
pacman -Sy git python3
```

3. Clone this repository.

```
git clone https://github.com/lbecher/install-archlinux.git
```

4. Change to install-archlinux directory.
```
cd install-archlinux
```

5. Run the live script.
```
python3 live.py
```

## arch-chroot.py (not created yet)
Script to be runned in the root of your installation (also in the live mode).


## after-reboot.py (not created yet)
Script to be runned into your installation after reboot.
