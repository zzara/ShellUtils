#!/bin/bash
# encode or decode base64 multiple times
# usage:
# bash base64multi.sh encode 3 -i ~/Desktop/file.txt -o ~/Desktop/file2.txt
# bash base64multi.sh decode 3 -i ~/Desktop/file.txt -o ~/Desktop/file2.txt
if [[ ${3} == "-i" ]]; then
    flagz=$( cat ${4} )
else
    flagz="${3}"
fi
case $1 in 
    encode )
        for i in `seq 1 ${2}`; do
            flagz=$( echo "${flagz}" | base64 )
        done
        ;;
    decode )
        for i in `seq 1 ${2}`; do
            flagz=$( echo "${flagz}" | base64 -D)
        done
        ;;
    *) echo "Invalid option  -- takes 'encode' or 'decode' as first arg"; exit;;
esac
echo "${flagz}"
if [[ $4 == "-o" ]]; then
    echo "${flagz}" >>${5}
elif [[ $5 == "-o" ]]; then
    echo "${flagz}" >>${6}
fi
