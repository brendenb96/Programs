#! /bin/sh

if [ `getconf LONG_BIT` = "64" ]; then
	cd /home/brenden/Programs/forticlientsslvpn/64bit
	nohup ./forticlientsslvpn > /dev/null 2>&1 &
else
	cd /home/brenden/Programs/forticlientsslvpn/32bit
	./forticlientsslvpn
fi
