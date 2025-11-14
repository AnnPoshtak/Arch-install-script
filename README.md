# Arch-install-script

## ⚠️ WARNING: READ THIS FIRST ⚠️

This is my **personal** script. If you want to use it, be **very careful**.

This script is DANGEROUS. It WILL **DESTROY ALL DATA** on the target disk.

The author is **NOT responsible** for:
* **BROKEN DEVICES**
* **ANY LOST DATA**
* ...or if your **PC JUST BREAKS**.

You may not like my settings, so before using it, **I advise you to read the code to understand what it does.**

This is a script for automatic installation of Arch Linux. It helps to make this process faster. Attention! the script works only for computers/laptops on the UEFI platform. Basic information about the script's operation:
1) The disk is divided into 2 partitions. EFI - 1GB, vfat file system. Root - the rest of the disk, ext4 file system
2) During the installation of the base system, only what is needed for the first launch is installed: base base-devel linux linux-headers linux-firmware git nano vim bash-completion efibootmgr grub networkmanager
3) After installation, you will receive a ready-made tty system with an account, the data for which you specified from the very beginning of the script. For the root user, the password will be the same as for the account
4) You can set the graphical interface later

To run the script, follow these instructions:
1) Boot from a flash drive, connect to the Internet
2) Download git to access the file and clone repo
pacman -S git
git clone "https://github.com/AnnPoshtak/arch-install-script"
3) Go to the directory with the file
cd arch-install-script
4) There will be 2 files in the directory. README.md and script.sh. You need script.sh.

5) Give it launch rights
chmod +x script.sh
6) And run it. Please note that before running, you must already have an Internet connection
./script.sh