# minWeZeroRPiOS
Contains Firmware for Mints Wearable Systems on the Raspberry Pi OS


## SD Card Installation 
Download Rasberry Pi Imager to your PC via this [link](https://www.raspberrypi.com/software/).


## Install DW Service 
```
wget https://dwservice.net/download/dwagent.sh
chmod +x dwagent.sh 
sudo ./dwagent.sh 
```
Follow the on screen instructions 


## Install Pi Zero SW 
```
curl http://cdn.pisugar.com/release/pisugar-power-manager.sh | sudo bash
```
After the installation finishes - Go to the http://<your raspberry ip>:8421 page and update the RTC Clock on the PI Sugar 3 

![link](https://raw.githubusercontent.com/mi3nts/minWeZeroRPiOS/main/res/piSugar3.png)

## For the IPS7100 to work on the GPIO Serial Port
To manually change the settings, edit the kernel command line with `sudo nano /boot/cmdline.txt`. Find the console entry that refers to the serial0 device, and remove it, including the baud rate setting. It will look something like `console=serial0,115200`. Make sure the rest of the line remains the same, as errors in this configuration can stop the Raspberry Pi from booting.

## New Image on the pi
- Add dwservice tag
- Start the rasberry pi via main power 
- update both the rtc as well as the pi time via the pisugar interface



## Basic Installation Steps
- Using the rasberry pi imager do an sd card image


- Using Raspi Config, enable Wi-Fi, I2C and the serial Port. 
```
sudo raspi-config
```

- Check wpa_supplimant file 
```
sudo  nano /etc/wpa_supplicant/wpa_supplicant.cpnf
```
- Reboot the Pi
```sudo reboot```

- Install dwservice 
```
https://www.dwservice.net/download/dwagent.sh
chmod +x dwagent.sh 
sudo ./dwagent.sh 
```
- clone the git repo 
```
mkdir gitHubRepos
```

- Install pisugaru SW
```
curl http://cdn.pisugar.com/release/pisugar-power-manager.sh | sudo bash
```
 - Update pisugar SW
```
curl https://cdn.pisugar.com/release/PiSugarUpdate.sh | sudo bash
```
- Add an extra I2c Pipeline 
On the to /boot/config.txt add the following lines `dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24` And connect the secondary I2C devices to gpio pins 23(16) and 24(18).
 ```
 sudo nano /boot/config.txt
 ```


- Update pi sugar
``` curl https://cdn.pisugar.com/release/PiSugarUpdate.sh | sudo bash```

 
 ```
 
 sudo reboot
   47  i2cdetect -y 1
   48  sudo apt-get update
   49  sudo apt-get install i2c-tools
   50  i2cdetect -y 1
   51  sudo hwclock -r
   52  timedatectl  status
   53  timedatectl set-timezone UTC
   54  timedatectl  status
   55  timedatectl set-local-rtc 0
   56  timedatectl set-ntp true
   57  timedatectl  status
   58  sudo nano /boot/cmdline.txt 
   59  date
   60  sudo reboot
   61  ls
   62  date
   63  clear
   64  ls
   65  cd 
   66  cd gitHubRepos/
   67  ls
   68  sudo nano 
   69  sudo nano /boot/config.txt
   70  cat /boot/config.txt
   71  sudo reboot
   72  ls
   73  cd ~
   74  ls
   75  cd gitHubRepos/
   76  ls
   77  i2cdetect -y 1
   78  i2cdetect -y 4
   79  clear
   80  ls
   81  pip3 install RPi.bme280
   82  python3
   83  sudo apt install python3-pip
   84  clear
   85  ls
   86  su teamlary
   87  git 
   88  sudo apt install git-all
   89  git
   90  git clone git@github.com:mi3nts/minWeZeroRPiOS.git
   91  cd .ssh
   92  ls
   93  cd ~
   94  cd .ss
   95  cd .ssh
   96  cat known_hosts 
   97  ls
   98  ssh-keygen
   99  pip3 install RPi.bme280
  100  clear
  101  ls
  102  cat id_rsa.pub 
  103  cd ~/gitHubRepos/
  104  git clone git@github.com:mi3nts/minWeZeroRPiOS.git
  105  cd minWeZeroRPiOS/
  106  ls
  107  cd firmware/
  108  ls
  109  cd xu4Mqtt/
  110  ls
  111  python3 ipReader.py 
  112  pip3 install netifaces
  113  python3 ipReader.py 
  114  pip3 install pyyaml
  115  python3 ipReader.py 
  116  pip3 install pyserial
  117  python3 ipReader.py 
  118  pip3 install paho-mqtt
  119  python3 ipReader.py 
  120  pip3 install getmac
  121  python3 ipReader.py 
  122  pip3 install pynmea2
  123  python3 ipReader.py 
  124  cd ~
  125  cd gitHubRepos/minWeZeroRPiOS/
  126  sudo nano .gitignore 
  127  git add . 
  128  git rm -r --cached .
  129  git add .
  130  git commit -m ".gitignore fix"
  131  git config --global user.email "lhw150030@utdallas.edu"
  132  git config --global user.name "lakithaomal"
  133  git rm -r --cached .
  134  git add .
  135  git commit -m ".gitignore fix"
  136  git push
  137  ls
  138  cd firmware/
  139  ls
  140  cd xu4Mqtt/
  141  ls
  142  python3 ips7100ReaderV1.py 
  143  clear
  144  ls
  145  python3 batteryReader.py 
  146  cat batteryReader.py 
  147  ls
  148  mv readI2c.py i2cReader.py
  149  python3 i2cReader.py 
  150  clear
  151  ls
  152  cat batteryReader.py 
  153  echo "get battery" | nc -q 1 127.0.0.1 8423
  154  echo get battery | nc -q 1 127.0.0.1 8423
  155  pip3 install pisugar
  156  from pisugar import *\
  157  python3
  158  sudo apt install netcat
  159  python3
  160  echo "get battery" | nc -q 1 127.0.0.1 8423
  161  python3 batteryReader.py 
  162  clear
  163  ls
  164  clear
  165  ls
  166  clear
  167  ls
  168  cat rasPiCron.txt 
  169  pwd
  170  crontab -e
  171  crontab -l
  172  sudo reboot
  173  history
