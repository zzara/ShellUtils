#!/bin/bash
# create a "matrix" of values using multiple dynamic array creation
# basic operation: ./matrix.sh 25 5
# ex. ./matrix.sh <row> <column> 

# matrix size delaration
mxRow=$1
mxColumn=$2

# matrix value declaration algorithm
function mxValueAlgoritm(){
	valueArray=( [0]='a' [1]='b' [2]='c' [3]='d' [4]='e' [5]='f' [6]='g' [7]='h' [8]='i' [9]='j' [10]='k' [11]='l' [12]='m' [13]='n' [14]='o' [15]='p' [16]='q' [17]='r' [18]='s' [19]='t' [20]='u' [21]='v' [22]='w' [23]='x' [24]='y' [25]='z' [26]='A' [27]='B' [28]='C' [29]='D' [30]='E' [31]='F' [32]='G' [33]='H' [34]='I' [35]='J' [36]='K' [37]='L' [38]='M' [39]='N' [40]='O' [41]='P' [42]='Q' [43]='R' [44]='S' [45]='T' [46]='U' [47]='V' [48]='W' [49]='X' [50]='Y' [51]='Z' [52]='0' [53]='1' [54]='2' [55]='3' [56]='4' [57]='5' [58]='6' [59]='7' [60]='8' [61]='9' )
	uniqArray="${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}-${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}-${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}${valueArray[$(($RANDOM % 61))]}"
	echo "${uniqArray}"
}

# array/matrix creation loop
for i in `seq 0 $((${mxRow}-1))`; do
	keyValue=0
	for j in `seq 1 ${mxColumn}`; do
		declare -a m${i}r[${keyValue}]="$(mxValueAlgoritm)"
		((++keyValue))
	done
done

# test output
for i in `seq 0 $((${mxRow}-1))`; do
	eval echo "\${m${i}r[*]}"
done

exit 0
