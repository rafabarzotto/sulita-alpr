#!/bin/sh

#check privileges
if [ `id -u` -ne 0 ]; then
  echo "É preciso rodar com sudo"
  exit 1
fi

cd /usr/share/openalpr
sudo mv runtime_data runtime_data_old
cd
cd sulita-alpr/
sudo cp -R runtime_data /usr/share/openalpr/
cd
mkdir img
mkdir out
mkdir img/cameras
sudo mv /etc/openalpr/openalpr.conf /etc/openalpr/openalpr.conf.bak
sudo mkdir /usr/local/bin/plateservice
cd sulita-alpr/openalpr/
sudo cp alprd.conf /etc/openalpr/
sudo cp openalpr.conf /etc/openalpr/
cd
cd sulita-alpr/servico/
sudo cp *.py /usr/local/bin/plateservice/
cd
sudo chmod -R 777 /usr/local/bin/plateservice
sudo chmod -R 777 /home/pi/img
sudo chmod -R 777 /home/pi/out
