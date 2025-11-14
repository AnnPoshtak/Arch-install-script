#!/usr/bin/bash

read -p "Acount name: " name
read -p "$name password: " password
lsblk
read -p "disk that will be format 'dev/...': " disk

wipefs -a $disk && sgdisk -Z $disk && sgdisk -n 1:0:0 -T 1:8300 $disk && mkfs.ext4 $disk

wipefs -a $disk && sgdisk -Z $disk && sgdisk -n 1:0 +2G -t 1:8300 -n 2:0:0 -t 2:8300 $disk

mkfs.vfat "${disk}1"
mkfs.ext4 "${disk}2"
