#!/bin/bash
# call arrays to reference other arrays
# usage: ./<script>.sh command 1
# commands == config || setting || command
arrcommand=( [0]='ls\s-l' [1]='pwd' [2]='w' [3]="top\s|\shead\s-n1" )
arrconfig=( [0]='--no-Log' [1]='-VV' [2]='transmit:always' [3]='max-threads:200' )
arrsetting=( [0]='user:admin' [1]='ip:192.168.1.1' [2]='type:smtp' [3]='remote-host:domain.example.com' )

popLoop="arr$1[@]"
popArr=( $(echo "${!popLoop}") )

for i in `seq 0 $(echo "${#popArr[@]}")`; do
	vvv=$(echo "${popArr[${i}]}" | sed -e 's/\\s/ /g')
	array333+=( "$vvv" )
done
if [[ $1 == "command" ]]; then
	eval ${array333[${2}]}

elif [[ $1 != "command" ]]; then
	echo "${array333[${2}]}"
fi

exit 0
