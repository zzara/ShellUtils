#!/bin/bash
# sorts elements of an integer array into ascending order
array=(1.36 0.53 0.98 1.92 3.18 -0.12)
size=${#array[@]}; n=1; y=$(($n+1))
for (( i = 0; i < ${size}; i++ )); do
	for (( j = i + 1; j < ${size}; j++ )); do
		if [[ ${array[${i}]} > ${array[${j}]} ]]; then
			a=${array[${i}]}
			array[${i}]=${array[${j}]}
			array[${j}]=${a}
		fi
	done
done
echo "All elements of the array have been sorted:"
echo "${array[*]}"
exit 0
