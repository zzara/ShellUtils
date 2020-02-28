#!/bin/bash
# arg $1, pass the path to the folder where the files are kept:
# example: ./script /Users/<user>/Desktop/tmp/ir/
# this wll iterate through all the files in the folder, grep the log lines for each record, decode the payload, and echo the results
# java.deserialization.extract.payload
# point the script at a folder of web logs to look for paylaods and decrypt them
loadBaseVar=$(cat $1*.* | grep -o '^.*\/DATA\/[a-zA-Z0-9\-_!]\{10,\}.*')
parseBaseVar=$(echo $loadBaseVar | sed -e 's/" [0-9]\{3\} [0-9]\{4,5\}/,/g')
countBaseVar=$(echo $parseBaseVar | tr -cd , | wc -c)
for i in `seq 0 $((${countBaseVar}-1))`; do
	loadBaseArray+=( "$(echo $parseBaseVar | cut -d',' -f$((${i}+1)))" )
	loadTimestampArray+=( "$(echo ${loadBaseArray[${i}]} | grep -o '^[0-9]\{1,3\}.\{41\}')" )
	zlibPayloadArray+=( "$(echo ${loadBaseArray[${i}]} | grep -o '\/DATA\/.*' | sed -e 's/ HTTP\/.*//g' -e 's/\/DATA\///g' -e 's/ //g' -e '/^\s*$/d' | sed -e 's/_/=/g' -e 's/-/+/g' -e 's/!/\//g')" )
	pythonPayloadArray+=( "$(python -c "import base64,zlib,sys;print repr(zlib.decompress(base64.b64decode(\"${zlibPayloadArray[${i}]}\")))")" )
	echo "\"${loadTimestampArray[${i}]}\" ${pythonPayloadArray[${i}]}"
	echo
done
exit 0
