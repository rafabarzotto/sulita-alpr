#!/bin/sh

#check privileges
if [ `id -u` -ne 0 ]; then
  echo "É preciso rodar com sudo"
  exit 1
fi

sudo apt-get -y install git
sudo apt-get -y install nodejs
sudo apt-get -y install npm
sudo apt-get -y install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get -y install liblog4cplus-dev libcurl3-dev
sudo apt-get -y install autoconf automake libtool
sudo apt-get -y install libleptonica-dev  
sudo apt-get -y install libicu-dev libpango1.0-dev libcairo2-dev  
sudo apt-get -y install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev  
sudo apt-get -y install python-dev python-numpy libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev  
sudo apt-get -y install virtualenvwrapper
sudo apt-get -y install liblog4cplus-dev
sudo apt-get -y install libcurl4-openssl-dev
sudo apt-get -y install python-beanstalkc
sudo apt-get -y install python-openalpr
sudo apt-get -y install python-opencv

git clone https://github.com/rafabarzotto/sulita-alpr