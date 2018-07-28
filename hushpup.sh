clear
# cat * | xxd -p file.tar.bz2 | dd *
# gen base 4 == base4=({0..3}{0..3}{0..3}{0..3}); for i in `seq 1 256`; do echo "${base4[$i]}"; done
# cat file1.jpg file2.zip >>newfile.jpg --- unzip newfile.jpg
# IMAGE_BASE64="$(base64 zzz.jpg)" --- echo "IMAGE_BASE64" | base64 --decode > pic2.jpg
arrW=([0000]='painter' [0001]='smash' [0002]='round' [0003]='referee' [0010]='polite' [0011]='cross' [0012]='birthday' [0013]='define' [0020]='arrest' [0021]='scholar' [0022]='secure' [0023]='disgrace' [0030]='progress' [0031]='speed' [0032]='consumption' [0033]='chalk' [0100]='telephone' [0101]='coup' [0102]='similar' [0103]='yearn' [0110]='desire' [0111]='hunting' [0112]='texture' [0113]='entertainment' [0120]='distinct' [0121]='palm' [0122]='jockey' [0123]='word' [0130]='will' [0131]='stain' [0132]='woman' [0133]='brave' [0200]='range' [0201]='manual' [0202]='conclusion' [0203]='panic' [0210]='girl' [0211]='sheet' [0212]='science' [0213]='replace' [0220]='private' [0221]='preparation' [0222]='metal' [0223]='hypothesize' [0230]='number' [0231]='central' [0232]='location' [0233]='donor' [0300]='firefighter' [0301]='belong' [0302]='construct' [0303]='deserve' [0310]='coal' [0311]='defendant' [0312]='vegetable' [0313]='facility' [0320]='mile' [0321]='film' [0322]='pass' [0323]='shiver' [0330]='tent' [0331]='formulate' [0332]='sense' [0333]='sand' [1000]='favour' [1001]='tree' [1002]='pilot' [1003]='voter' [1010]='policy' [1011]='advertise' [1012]='nuance' [1013]='linger' [1020]='marriage' [1021]='judge' [1022]='kidney' [1023]='motivation' [1030]='hunter' [1031]='needle' [1032]='ring' [1033]='venture' [1100]='jury' [1101]='script' [1102]='recession' [1103]='concert' [1110]='medal' [1111]='cooperation' [1112]='tradition' [1113]='company' [1120]='mist' [1121]='guerrilla' [1122]='thin' [1123]='credibility' [1130]='tired' [1131]='profile' [1132]='radical' [1133]='salad' [1200]='tense' [1201]='boom' [1202]='heel' [1203]='track' [1210]='polish' [1211]='crouch' [1212]='stem' [1213]='distort' [1220]='fling' [1221]='wrap' [1222]='prediction' [1223]='jump' [1230]='pawn' [1231]='clock' [1232]='stamp' [1233]='economy' [1300]='stress' [1301]='insist' [1302]='option' [1303]='official' [1310]='mosquito' [1311]='dull' [1312]='outlet' [1313]='glance' [1320]='chain' [1321]='corn' [1322]='hypnothize' [1323]='piece' [1330]='relate' [1331]='provoke' [1332]='mutual' [1333]='regret' [2000]='steward' [2001]='ash' [2002]='feather' [2003]='boot' [2010]='knock' [2011]='general' [2012]='orthodox' [2013]='request' [2020]='week' [2021]='bridge' [2022]='random' [2023]='adventure' [2030]='return' [2031]='confidence' [2032]='sword' [2033]='spokesperson' [2100]='glove' [2101]='waist' [2102]='photocopy' [2103]='pot' [2110]='engagement' [2111]='haircut' [2112]='partner' [2113]='fuss' [2120]='cemetery' [2121]='skeleton' [2122]='strange' [2123]='race' [2130]='limit' [2131]='guideline' [2132]='rugby' [2133]='emotion' [2200]='tumble' [2201]='operational' [2202]='laser' [2203]='fare' [2210]='bubble' [2211]='predator' [2212]='elaborate' [2213]='distortion' [2220]='sale' [2221]='command' [2222]='earthflax' [2223]='draft' [2230]='spite' [2231]='diagram' [2232]='liver' [2233]='reference' [2300]='committee' [2301]='restless' [2302]='petty' [2303]='nerve' [2310]='community' [2311]='plug' [2312]='blue jean' [2313]='retiree' [2320]='stream' [2321]='expression' [2322]='fruit' [2323]='rhythm' [2330]='superintendent' [2331]='native' [2332]='disk' [2333]='ivory' [3000]='communication' [3001]='kinship' [3002]='racism' [3003]='knit' [3010]='accent' [3011]='astonishing' [3012]='loose' [3013]='secular' [3020]='competition' [3021]='trench' [3022]='value' [3023]='tendency' [3030]='cheek' [3031]='flex' [3032]='houseplant' [3033]='reluctance' [3100]='queue' [3101]='jurisdiction' [3102]='trolley' [3103]='abbey' [3110]='printer' [3111]='bold' [3112]='father' [3113]='mirror' [3120]='ideology' [3121]='study' [3122]='posture' [3123]='charge' [3130]='disability' [3131]='suffering' [3132]='bathtub' [3133]='gregarious' [3200]='joke' [3201]='middle' [3202]='circumstance' [3203]='issue' [3210]='census' [3211]='separation' [3212]='pit' [3213]='declaration' [3220]='fool' [3221]='curriculum' [3222]='forestry' [3223]='king' [3230]='mountain' [3231]='monstrous' [3232]='neck' [3233]='timetable' [3300]='intermediate' [3301]='owner' [3302]='relation' [3303]='solution' [3310]='lead' [3311]='realism' [3312]='revival' [3313]='recover' [3320]='address' [3321]='total' [3322]='medicine' [3323]='competence' [3330]='gown' [3331]='high' [3332]='officer' [3333]='reception')
arrR=([1]='I used to have a' [2]='We should get a' [3]='OMG!! YES. My' [4]='Check it out!!' [5]='TOTES. New' [6]='Everyone should have a' [7]='WHy NOT?!' [8]='Not thrilled... my' [9]='new new new YES!' [10]='Found a' [11]='Random!' [12]='SO RANDOM!!' [13]='Ummmm... No way:' [14]='Really?' [15]='huh.. so this is a thing:')
arrD=('./file.txt' 'file2.txt' './file3.txt')
for file in "${arrD[@]}"; do
	arrV=();arrCnt=();arrB=();arrS=();
	IFS=$'\n' arrV+=( $(cat $file | gzip -cf) )
	#uncompress
	#$echo "hello text" | gzip -cf > /tmp/myfile
	#$cat /tmp/myfile |gunzip -cf
	for h in "${arrV[@]}"; do
		xxc=$(echo "$h" | xxd -b | grep -o "[0-1]\{8\}")
		for i in $xxc; do 
			aa=$(echo "ibase=2;obase=4; $i" | bc)
			aa=$(printf "%04d\n" $aa)
			arrB+=("$aa")
		done
	done
	for i in "${arrB[@]}"; do
		rand=$(( ( RANDOM % 15 ) + 1 ))
		bb=$(printf "${arrR[$rand]} ${arrW[$i]}.")
		arrS+=("$bb")
	done
	sa=0
	arrCnt=$(echo "${#arrS[@]}")
	while [[ arrCnt != "" ]]; do
		if [[ $arrCnt -le 0 ]]; then
			break
		fi
		sb=$(($sa+1));sc=$(($sa+2));sd=$(($sa+3));
		printf "${arrS[*]:$sa:1} ${arrS[*]:$sb:1} ${arrS[*]:$sc:1} ${arrS[*]:$sd:1}"
		printf '%s\n' ""
		sa=$(($sa+4))
		arrCnt=$((arrCnt-4))
	done
	printf '%s\n\n' ""
done
printf '%s\n' ""
