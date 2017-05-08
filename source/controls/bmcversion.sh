#!/bin/sh

PKG_FILE=/etc/os-release



echo " "
echo "--------------------------------------------------------"
echo " "
if [ -f $PKG_FILE ];
then
	sed '1,4'd $PKG_FILE > /etc/vfile
	sed 's/!/ /' /etc/vfile > /etc/vfile2
	echo "  Package version    :" $(cat /etc/vfile2 | awk '{-F="PRETTY_NAME=\"";print $2}')
	echo " "
	rm /etc/vfile
	rm /etc/vfile2
fi
echo " "
echo "--------------------------------------------------------"
echo " "
