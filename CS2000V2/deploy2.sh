#!/bin/bash
mount -o remount,rw /

dguid=$1
echo ${dguid}
if [ ${dguid} -gt 00000000 -a ${dguid} -lt 100000000 ] 
then 
   echo DGU id is ${dguid}
else
   echo DGU id eror!${dguid}
   exit
fi

cd /home/root
mkdir run
mkdir conf

cd /work/data
chmod 755 preconf.sh
chmod 755 conf.sh
chmod 755 wdgpio.sh
chmod 755 cnfpga.sh
mkdir save

cd /work/data/psFPGA
chmod 755 configDriver.sh
chmod 755 fpgaUpgradApp

cd /etc/rc5.d
rm S30MainWindow 
ln -s /work/data/wdgpio.sh S21wdgpio.sh
ln -s /work/data/preconf.sh S30preconf.sh
ln -s /work/data/conf.sh S31conf.sh

cd /home/root
tar zxvf /work/data/tools.tar.gz
#tar zxvf /work/data/dgu2000V2.tar.gz

cp /work/data/hw.conf /home/root/conf/

./autoid ${dguid}
./ip 192.168.2.$[100+${dguid}%100] 255.255.255.0
./serverip 192.168.2.89
./serverport 80





