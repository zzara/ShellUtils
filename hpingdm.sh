#!/bin/bash
# a small (currently unfinished) chat utility to send messages in clear text on the wire.
# you can capture the icmp traffic and look for messages in the packet details
echo "       ---+---"
echo "   ---+---+---+---"
echo " ---+---+---+---+---"
echo "---- pingdm chat ----"
echo " ---+---+---+---+---"
echo "   ---+---+---+---"
echo "       ---+---"
read -p "Enter host IP: " recipient;
rec=$(ping -n -c 1 -W 0.2 -i 0.1 $recipient)
if [[ $rec != *"1 packets received"* ]]; then
	echo "HOST NOT UP!"
	echo "EXITING...."
	exit 0
fi
if [[ $rec == *"1 packets received"* ]]; then
	recc=$(echo "$rec" | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | head -1)
fi
echo "Host is online!"
sleep 1
read -p "Enter your message: " msg;
msgLow=$(echo "$msg" | awk '{print tolower($0)}')
read msgClean <<< $(grep -o . <<<$msgLow)
msgHex=$(echo "$msgClean" | sed 's/ //g' | od -t x1 | grep -oE '([0-9a-z]{2}\s){1,}' | sed '1d;$d' | tr '\n' ' ' | sed 's/ //g')
msgCnt=$(echo "$msgHex" | awk '{print length}')
msgLen=$((($msgCnt/16)+1))
pingP=$msgHex
#cut length of message down to 16 length strings and ping for each
while [[ $msgLen != 0 ]]; do
	png=$(echo "$pingP" | cut -c 1-16)
	ping -n -c 1 -W 0.2 -i 0.1 -p $png $recipient
	pingP=$(echo "$pingP" | cut -c 17-)
	msgLen=$(($msgLen-1))
done
