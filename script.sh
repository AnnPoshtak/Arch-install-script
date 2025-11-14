#!/usr/bin/bash

read -p "Acount name: " name
read -p "$name password: " password
lsblk
read -p "disk that will be format 'dev/...': " disk


wipefs -a $disk && sgdisk -Z $disk && sgdisk -n 1:0 +2G -t 1:ef00 -n 2:0:0 -t 2:8300 $disk

if [[ $disk == *nvme* ]]; then
    efi_part = "${disk}p1"
    root_part = "${disk}p2"
else
    efi_part = "${disk}1"
    root_part = "${disk}2"

mkfs.vfat $efi_part
mkfs.ext4 $root_part

mount $root_part /mnt
mkdir -p mnt/boot/efi
mount $efi_part /mnt/boot/efi

sed -i 's/^#\?ParalelDonwloads=.*/ParalelDonwloads=35/' /etc/pacman.conf

pacstrap /mnt base base-devel linux linux-headers linux-firmware git nano vim bash-completion efibootmgr grub networkmanager ttf-ubuntu-font-family ttf-opensans ttf-hack

genfstab /mnt >> /etc/genfstab

arch-chroot /mnt
