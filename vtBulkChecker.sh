#!/bin/bash
# virustotal checker

# your vt api key
vtApiKey="<api_key>"

# hash array
datHash=(0f544782b7cb58d23511de446c1125952f794d7ebfda1c2f84bd6e03af9c4da8
06f1aaba68a23d85601ad069dd5ff9cff03ef4bd95000000105bd90b00700000
06f1aaba68a23d85601ad069dd5ff9cff03ef4bd95000000108be10b00700000
08721ab411fb53a19f0e1684dd7e83d73dcae6819f976807cdbc31b996e70ed0
0982782FECBF203589D4D4518B80A4D397D678DD70FE8319FCD42A8FDA96A893
0c08b64f8e08bbe2d2415f877fd2a16754dd2255beb0b70250fdb5cc3709ae78
10a8599f0f56e52b8bad253f289020bd3cd5b9558ab799af85897a54c34dff59
1419a27682de3d2f52b02f94e7add3f6a6adbb08e0faaa7d1b331b68df7cc2b1
17C3C91A7B92D3766D6D5491FB938E3FED1795E82BC288D179450E25FCD3F206)
# iteration assignment
datHashLen="${!datHash[*]}"
# set unique timestamp
dateSt=$(date +%s)
# main loop
for i in $datHashLen; do
	{
	# reset vars
	curlResult=""
	curlResultTotal=""
	curlResultPositives=""
	curlResultScanDate=""
	# main curl
	curlResult=$(curl -v --request POST --url https://www.virustotal.com/vtapi/v2/file/report -d apikey=${vtApiKey} -d "resource=${datHash[${i}]}")
	# clean result
	curlResultTotal=$(echo "${curlResult}" | grep -o '"total\"\: [0-9]\{1,3\}')
	curlResultPositives=$(echo "${curlResult}" | grep -o '\"positives\"\: [0-9]\{1,3\}')
	curlResultScanDate=$(echo "${curlResult}" | grep -o '\"scan_date\"\: \"[0-9]\{4\}\-[0-9]\{2\}\-[0-9]\{2\} [0-9]\{2\}\:[0-9]\{2\}\:[0-9]\{2\}\"')
	# output clean
	echo "${datHash[${i}]}, ${curlResultTotal}, ${curlResultPositives}, ${curlResultScanDate}" >>~/Desktop/vt_bulk_hash_${dateSt}.txt
	} &> /dev/null
done
cat ~/Desktop/vt_bulk_hash_${dateSt}.txt
