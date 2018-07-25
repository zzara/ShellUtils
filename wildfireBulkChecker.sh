#!/bin/bash
# wildfire hash checker

# paypal api key
wildfireApiKey="<api_key>"

# hash array
datHash=(06f1aaba68a23d85601ad069dd5ff9cff03ef4bd95000000105bd90b00700000
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
for i in $datHashLen; do
	{
	# reset vars
	curlResult=""
	curlResultTotal=""
	curlResultPositives=""
	curlResultScanDate=""
	# main curl
	curlResult=($(curl -F "hash=${datHash[${i}]}" -F "apikey=${wildfireApiKey}" -F 'format=xml' 'https://wildfire.paloaltonetworks.com/publicapi/get/verdict'))
	curlResult=$(echo "${curlResult[*]}")
	# clean result
	curlResultVerdict=$(echo "${curlResult}" | grep -o -m 1 '<verdict>[0-9\-]\{1,4\}<\/verdict>' | awk -F'(<[/]?verdict>)' '{print $2;exit}')
	# output clean
	echo "${datHash[${i}]}, Verdict: ${curlResultVerdict}" >>~/Desktop/wildfire_bulk_hash_${dateSt}.txt
	} &> /dev/null
done
echo '0: benign || 1: malware || 2: grayware || 4: phishing || -100: pending, the sample exists, but there is currently no verdict || -101: error || -102: unknown, cannot find sample record in the database || -103: invalid hash value'
echo
cat ~/Desktop/wildfire_bulk_hash_${dateSt}.txt
