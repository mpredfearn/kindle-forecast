
# Setting Up the Kindle

## Jailbreak

First, you will need to Jailbreak your kindle. I have a 4th Generation Kindle, so I followed the instructions here:
http://wiki.mobileread.com/wiki/Kindle4NTHacking
http://www.mobileread.com/forums/showthread.php?t=191158
I used kindle-k4-jailbreak-1.8.N.zip 

# Kindle USB network

Next, you're going to need to establish communications with Linux running on the Kindle, which you can set up with USB networking as described here:
http://www.mobileread.com/forums/showthread.php?t=88004
I used kindle-usbnetwork-0.57.N-k4.zip

Once you've installed USB networking, you can ssh to the Kindle as follows:
* Disconnect the USB cable.
* Enter the following on the Kindle keyboard:
* **;debugon**
* **~usbnetwork**
* **;debugoff**

* Reconnect the USB cable. The USB storage screen will not appear this time.
* Find the name of the USB network adaptor that has been created. This would normally be usb0 but on my machine systemd (grrrr) renamed it to enp0s20u1.
* Run the following commands:
* $ sudo ip addr add 192.168.15.201 dev enp0s20u1
* $ sudo ip route add 192.168.15.0/24 dev enp0s20u1
* $ ssh root@192.168.15.244
```
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.15.244' (ECDSA) to the list of known hosts.

Welcome to Kindle!

root@192.168.15.244's password: 
#################################################
#  N O T I C E  *  N O T I C E  *  N O T I C E  # 
#################################################
Rootfs is mounted read-only. Invoke mntroot rw to
switch back to a writable rootfs.
#################################################
[root@kindle root]# 
```
Yay! We are now logged in anf can make changes to the Kindle's filesystem

* Mount / read-write:
[root@kindle root]# mntroot rw
* Add an extra rule to cron:
[root@kindle root]# nano /etc/crontab/root
* Add the following line to refresh the display every 10 minutes:
*/10 * * * * /mnt/us/weather/display-weather.sh

In another terminal, copy the weather directory to the Kindle:
* scp -r kindleweatherfiles/weather/ root@192.168.15.244:/mnt/us/weather/

And back on the Kindle, make the script executable:
* chmod +x /mnt/us/weather/display-weather.sh

That's it - reboot the Kindle to activate the cron job and it should start pulling images from your configured server every 10 minutes.
