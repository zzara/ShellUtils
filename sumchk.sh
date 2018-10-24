#!/bin/bash

sum1=$(md5 $1 | cut -d' ' -f4)
while true; do
    sum2=$(md5 $1 | cut -d' ' -f4)
    if [[ $sum1 != $sum2 ]]; then
        sum1=$sum2
        echo $sum1
    fi
    sleep 1
done
