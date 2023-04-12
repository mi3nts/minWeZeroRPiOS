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
