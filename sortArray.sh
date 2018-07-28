#!/bin/bash
# sort elements of an array using bidirectional method
array=(1.36 0.53 0.98 1.92 3.18 -0.12)
size=${#array[@]}
for (( i = 0; i < size; i++ )); do
	# sort
	for (( j = i + 1; j < size; j++ )); do
		if [[ ${array[${i}]} > ${array[${j}]} ]]; then
			a=${array[${i}]}
			array[${i}]=${array[${j}]}
			array[${j}]=${a}
		fi
	done
done
echo "All elements of the array have been sorted:"
echo "${array[*]}"
