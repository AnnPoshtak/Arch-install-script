# Arch-install-script

## ⚠️ WARNING: READ THIS FIRST ⚠️

This is my **personal** script. If you want to use it, be **very careful**.

This script is DANGEROUS. It WILL **DESTROY ALL DATA** on the target disk.

The author is **NOT responsible** for:
* **BROKEN DEVICES**
* **ANY LOST DATA**
* ...or if your **PC JUST BREAKS**.

You may not like my settings, so before using it, **I advise you to read the code to understand what it does.**
<hr>
![Arch Linux](https://img.shields.io/badge/Arch%20Linux-1793D1?logo=arch-linux&logoColor=white)
![Shell Script](https://img.shields.io/badge/Shell_Script-121011?logo=gnu-bash&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
This is a script for automatic installation of Arch Linux. It helps to make this process faster.  
Attention! The script works only for computers/laptops on the UEFI platform.

Basic information about the script:

1. The disk is divided into 2 partitions:
   - EFI — 1GB, vfat
   - Root — rest of disk, ext4

2. Installed packages:
```
base base-devel linux linux-headers linux-firmware git nano vim bash-completion efibootmgr grub networkmanager
```

3. After installation, you receive a ready TTY system with a user account.  
   The root password = user password.

4. You can install a graphical interface later.

---

## How to run the script

1. Boot from USB and connect to the Internet  
2. Install git and clone repo:

```bash
pacman -S git
git clone "https://github.com/AnnPoshtak/arch-install-script"
```

3. Go to directory:

```bash
cd arch-install-script
```

4. Make script executable:

```bash
chmod +x script.sh
```

5. Run script:

```bash
./script.sh
```