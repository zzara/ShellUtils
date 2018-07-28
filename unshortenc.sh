#!/bin/sh
# curls incoming email report from splunk
# This is limited by 10 hits per hour by IP
#emlFnd=$(find /Users/tclausen/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Messages/ -type f -mtime -12 -exec grep 'shortened_urls' {} \; | grep -o '[A-Z0-9]\{8\}-.*olk15Message')
emlAtt=$(find /Users/<usernamename>/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Message\ Attachments/ -type f -mmin -55 -exec grep 'shortened_urls' {} \; -exec strings {} \; | grep -o "[A-Za-z0-9+/]\{18,\}[=]\{0,2\}" | grep -v "Containers\|Office\|Profile\|Attachments\|olk15MsgAttachment\|/Users/\|[A-F0-9]\{32\}")
fieldNum=$(echo $emlAtt | grep -o " " | wc -l); fieldNum=$(( $fieldNum + 1))
baseOut=$(echo $emlAtt | cut -f1-${fieldNum} -d" " | sed -e "s/ //g" )
urlArr+=( $(base64 -D <<< $baseOut) )
urlArrClean+=( $(printf '%s\n' "${urlArr[@]}" | sed -e "s/,2*//g" -e "s/ / /g" -e "s/^ / /g" | grep "/" | tr -d '\r') )
randName=$(echo ${RANDOM}-${RANDOM}-${RANDOM})
for i in "${urlArrClean[@]}"; do curl https://unshorten.me/s/${i} >>~/Desktop/tab/unshortUrls-${randName}.txt ;	done
