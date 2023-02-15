#!/bin/sh

echo '***** Start: Update Script *****'

HTML_FILES="$ADAM_APP_DATA_DIR/detection.html"
#ETH_IF=eth1

BUSYBOX=busybox
alias ifconfig="$BUSYBOX ifconfig"
alias sed="$BUSYBOX sed"
alias grep="$BUSYBOX grep"

#IP_ADDRESS=$(ifconfig $ETH_IF |grep inet[^6] |sed 's/.*inet[^6][^0-9]*\([0-9.]*\)[^0-9]*.*/\1/')

echo "InstallId:  $ADAM_INSTALLID"
#echo "IP Address: $IP_ADDRESS"
echo "Setting IP Address and InstallId in html files."

for html_file in $HTML_FILES
do
	sed -i -e "s/12345678/$ADAM_INSTALLID/g" $html_file
done

echo '***** Finish: Update Script *****'

exit 0
