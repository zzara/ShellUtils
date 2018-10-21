#!/bin/bash
cat /Users/<user>/Downloads/file.csv | cut -d',' -f6 | sed -e 's/\"//g' | while read -r line; do 
    if [[ ${line} =~ '<start of base64 value>' ]]; then
        mid=$(echo "${arr_a[*]}" | sed -e 's/ //g' | base64 -D)
        printf '%s\n' ${mid} >>/Users/<user>/Downloads/base.txt
        arr_a=()
    fi
    arr_a+=("${line}")
done
