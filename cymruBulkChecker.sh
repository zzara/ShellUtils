#!/bin/bash
# bulk hash checker

datHash=(0f544782b7cb58d23511de446c1125952f794d7ebfda1c2f84bd6e03af9c4da8
0f728b8f0e7ff8238f1b43649ddaeb70f580a4f4a28f9c7b187c3a27bb7f4b9b
33003d010070000060c63d01007000000802ffff0000000030c63d0100700000
4404a5e764c7b087f61430e3352808f88c67f8bf11f65f8ed0c97c1ab4e7a35f
720c44dc8bfbda093d101bd4d71d6aa75f309efa42653f3e0ed9d01d45d56b18
81f0e80f38b04c4ab405ae3de6597fd2c8698fd6a7c7ef9ce34a637d82382baa
8545379af95dd8dee77db08c8d536a7d1c74f5a8e5d2626ab6431a94bc3f87da
877db2c258c8a5836045c92c3ebea19d56872612d031b01776d5b48e7e85c7c8
d7d6c97d20d8bb7032dfc62e7b411e4967dc94949d7c9aeda3db5055e4f439e4
d8b1d8556cc2ad6268c5e7f752461047260127dc4a69c2048b5419c896804aea
fef3c2b6b71af3a502bc04f597bc5d75c188d470e0eba10464555d8cadea0b42)
datHashLen="${!datHash[*]}"
if ([ $datHashLen == "40" ] || [ $datHashLen == "32" ]); then
	for i in $datHashLen; do
	whois -h hash.cymru.com ${datHash[${i}]} >>~/Desktop/cymru_hash_lookup.txt
done
cat ~/Desktop/cymru_hash_lookup.txt
else
	echo "Hashes are not md5 or sha1."
	exit 0
fi
