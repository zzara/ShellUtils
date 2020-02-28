#!/bin/env python3
# usage ipIntel.py www.domain.com
import urllib.request
import requests
import socket
from sys import argv
import sys
# Loading dns module.
try:
    import dns.resolver
    resolver = dns.resolver.Resolver()
    resolver.timeout = 0.10
    resolver.lifetime = 0.10
except:
    print('Error : Unable To Load dns Module.')
    print('For python3 : pip3 install dnspython3')
    print('For python2 : pip install dnspython3')
    sys.exit(0)

# set api key
SHODAN_API_KEY = "<api_key>"
VIRUSTOTAL_API_KEY = "<api_key"

# set url and ip
DOMAIN = f"{argv[1]}"
IP_Q = socket.gethostbyname(f'{DOMAIN}')

# virustotal request
headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,  My Python requests library example client or username"
  }
params = {'apikey': f'{VIRUSTOTAL_API_KEY}', 'resource':f'{DOMAIN}'}
response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=params, headers=headers)
json_response = response.json()

# shodan query
with urllib.request.urlopen(f"https://api.shodan.io/shodan/host/{IP_Q}?key={SHODAN_API_KEY}") as response:
    returnUrl = response.read()

# print base query
print(f"{json_response}") # virustotal
print(returnUrl) # shodan

# rblDict Contains the data base of all rbl autority names and their website address.
# rblDict ={ 'orgName':'orgName Site'}
rblDict = {'spam.spamrats.com': 'http://www.spamrats.com',
 'spamguard.leadmon.net': 'http://www.leadmon.net/SpamGuard/',
 'rbl-plus.mail-abuse.org': 'http://www.mail-abuse.com/lookup.html',
 'web.dnsbl.sorbs.net': 'http://www.sorbs.net',
 'ix.dnsbl.manitu.net': 'http://www.dnsbl.manitu.net',
 'virus.rbl.jp': 'http://www.rbl.jp',
 'dul.dnsbl.sorbs.net': 'http://www.sorbs.net',
 'bogons.cymru.com': 'http://www.team-cymru.org/Services/Bogons/',
 'psbl.surriel.com': 'http://psbl.surriel.com',
 'misc.dnsbl.sorbs.net': 'http://www.sorbs.net',
 'httpbl.abuse.ch': 'http://dnsbl.abuse.ch',
 'combined.njabl.org': 'http://combined.njabl.org',
 'smtp.dnsbl.sorbs.net': 'http://www.sorbs.net',
 'korea.services.net': 'http://korea.services.net',
 'drone.abuse.ch': 'http://dnsbl.abuse.ch',
 'rbl.efnetrbl.org': 'http://rbl.efnetrbl.org',
 'cbl.anti-spam.org.cn': 'http://www.anti-spam.org.cn/?Locale=en_US',
 'b.barracudacentral.org': 'http://www.barracudacentral.org/rbl/removal-request',
 'bl.spamcannibal.org': 'http://www.spamcannibal.org',
 'xbl.spamhaus.org': 'http://www.spamhaus.org/xbl/',
 'zen.spamhaus.org': 'http://www.spamhaus.org/zen/',
 'rbl.suresupport.com': 'http://suresupport.com/postmaster',
 'db.wpbl.info': 'http://www.wpbl.info',
 'sbl.spamhaus.org': 'http://www.spamhaus.org/sbl/',
 'http.dnsbl.sorbs.net': 'http://www.sorbs.net',
 'csi.cloudmark.com': 'http://www.cloudmark.com/en/products/cloudmark-sender-intelligence/index',
 'rbl.interserver.net': 'http://rbl.interserver.net',
 'ubl.unsubscore.com': 'http://www.lashback.com/blacklist/',
 'dnsbl.sorbs.net': 'http://www.sorbs.net',
 'virbl.bit.nl': 'http://virbl.bit.nl',
 'pbl.spamhaus.org': 'http://www.spamhaus.org/pbl/',
 'socks.dnsbl.sorbs.net': 'http://www.sorbs.net',
 'short.rbl.jp': 'http://www.rbl.jp',
 'dnsbl.dronebl.org': 'http://www.dronebl.org',
 'blackholes.mail-abuse.org': 'http://www.mail-abuse.com/lookup.html',
 'truncate.gbudb.net': 'http://www.gbudb.com/truncate/index.jsp',
 'dyna.spamrats.com': 'http://www.spamrats.com',
 'spamrbl.imp.ch': 'http://antispam.imp.ch',
 'spam.dnsbl.sorbs.net': 'http://www.sorbs.net',
 'wormrbl.imp.ch': 'http://antispam.imp.ch',
 'query.senderbase.org': 'http://www.senderbase.org/about',
 'opm.tornevall.org': 'http://dnsbl.tornevall.org',
 'netblock.pedantic.org': 'http://pedantic.org',
 'access.redhawk.org': 'http://www.redhawk.org/index.php?option=com_wrapper&Itemid=33',
 'cdl.anti-spam.org.cn': 'http://www.anti-spam.org.cn/?Locale=en_US',
 'multi.surbl.org': 'http://www.surbl.org',
 'noptr.spamrats.com': 'http://www.spamrats.com',
 'dnsbl.inps.de': 'http://dnsbl.inps.de/index.cgi?lang=en',
 'bl.spamcop.net': 'http://bl.spamcop.net',
 'cbl.abuseat.org': 'http://cbl.abuseat.org',
 'dsn.rfc-ignorant.org': 'http://www.rfc-ignorant.org/policy-dsn.php',
 'zombie.dnsbl.sorbs.net': 'http://www.sorbs.net',
 'dnsbl.njabl.org': 'http://dnsbl.njabl.org',
 'relays.mail-abuse.org': 'http://www.mail-abuse.com/lookup.html',
 'rbl.spamlab.com': 'http://tools.appriver.com/index.aspx?tool=rbl'
}

searchIp = f"{IP_Q}"

for rblOrg in rblDict:
  print(   '{:14}{:35}'.format(' [ Checking ]',rblOrg) , end='')
  ipRev =  '.'.join( searchIp.split('.')[::-1])
  searchQuery = ipRev+'.'+rblOrg
  try:
    resolver.query(searchQuery,'A')
    print('Listed')  
  except:
    print('Not Listed')
