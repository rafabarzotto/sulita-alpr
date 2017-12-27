#!/bin/sh

#check privileges
if [ `id -u` -ne 0 ]; then
  echo "É preciso rodar com sudo"
  exit 1
fi

sudo apt-get update
sudo apt-get upgrade
sudo reboot