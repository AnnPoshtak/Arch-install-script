#!/usr/bin/bash

set -e

read -p "Acount name: " name
read -sp "$name password: " password
lsblk -d -o NAME,SIZE,MODEL
read -p "disk that will be format 'dev/...': " disk

pacman -S reflector 
reflector --country 'Ukraine,Poland,Germany' --sort rate --save /etc/pacman.d/mirrorlist

wipefs -a "$disk"
sgdisk -Z "$disk"
partprobe "$disk"
sleep 3
sgdisk -n 1:0:+1G -t 1:ef00 "$disk"
sgdisk -n 2:0:0 -t 2:8300 "$disk"
partprobe "$disk"
sleep 3

if [[ $disk == *nvme* ]]; then
    efi_part="${disk}p1"
    root_part="${disk}p2"
else
    efi_part="${disk}1"
    root_part="${disk}2"
fi

mkfs.vfat $efi_part
mkfs.ext4 $root_part

mount $root_part /mnt
mkdir -p /mnt/boot/efi
mount $efi_part /mnt/boot/efi

sed -i 's/^#\?ParallelDonwloads=.*/ParallelDonwloads=35/' /etc/pacman.conf

pacstrap /mnt base base-devel linux linux-headers linux-firmware git nano vim bash-completion efibootmgr grub networkmanager ttf-ubuntu-font-family ttf-opensans ttf-hack

genfstab /mnt >> /mnt/etc/genfstab

arch-chroot /mnt
systemctl enable NetworkManager
sed -i 's/^#en_US.UTF-8/en_US.UTF-8/'
locale-gen

echo "LANG=en_US.UTF-8" > /etc/locale.conf
useradd -m $name
passwd $name
passwd root

echo "$name ALL=(ALL:ALL) ALL" >> /etc/sudoers

grub-install $disk

grub-mkconfig -o /boot/grub/grub.cfg

exit
umount -R /mnt

echo "THE SYSTEM WILL REBOOT NOW. When thw BIOS screen appes? unplug the USB drive"
sleep 3
reboot