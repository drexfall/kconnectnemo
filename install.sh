#!/bin/sh

ROOTUID="0"
dir="usr/share/nemo/actions/"
sudo="sudo"

if [ "$(id -u)" -ne "$ROOTUID" ] ; then
    dir="$HOME/.local/share/nemo/actions/"
    sudo=""
fi

echo "Installing at" $dir

$sudo pacman -S kdeconnect libnotify --noconfirm
$sudo apt-get kdeconnect libnotify4

cp ./kconnectnemo.nemo_action $dir
cp ./kde_share_action.py $dir

echo "Done!"
