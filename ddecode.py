#!/usr/bin/python

'''
	This is ascii <-> shellcode encode / decoder tool
		--------------------------------------------------------------
		how to use :
		--------------------------------------------------------------
		what do you want to do ? encode / decode / b64hex
		--> encode
		Please input data : /bin
		shellcode --> \x2f\x62\x69\x6e
		--------------------------------------------------------------
		what do you want to do ? encode / decode / b64hex
		--> decode
		Please input data : \x2f\x2f\x73\x68
		hex       -->  2f2f7368
		plaintext --> //sh
		--------------------------------------------------------------
		what do you want to do ? encode / decode / b64hex
		--> b64hex
		Please input data : kfdHFIG=
		plaintext --> //sh
		--------------------------------------------------------------
		
	warning ! this is not disassemble tool !

	you will also probably need to remove the limit for characters being pasted into the terminal with this command: stty -icanon

'''

import binascii, sys, time, base64

RED = '\033[31m'
WHITE = '\033[37m'
GREEN = '\033[32m'
RESET = '\033[0;0m'

def main():
	print "\r\n"
	print "*******************************"
	print "SHELLCODE HEX ENCODER & DECODER"
	print "*******************************"
	print "\r\n"
	q = ''
	while not (q == 'encode' or q =='decode' or q == 'b64hex'):
		print "Please select one of the following options:\r\n 1)  %sencode%s - encodes string to a hex value\r\n 2)  %sdecode%s - decodes hex value to a string\r\n 3)  %sb64hex%s - decodes base65 to hex to sting values" % (RED, RESET, WHITE, RESET, GREEN, RESET)
		q = raw_input("--> ")
	else:
		if q == "encode":#enc
			inputtype = raw_input("Please input data : ")
			print "\r\nshellcode --> ",
			for encoded in inputtype:
				print "\b\\x"+encoded.encode("hex"),
				sys.stdout.flush()
			print "\r\n"

		elif q == "decode":
			inputtype = raw_input("Please input data : ")
			cleaninput = inputtype.replace("\\x","")
			print "hex       --> ",cleaninput
			print "plaintext -->  ",
			print "\b"+cleaninput.decode("hex")

		elif q == "b64hex":
			inputtype = raw_input("Please input data : ")
			based = base64.b64decode(inputtype)
			cleaninput = based.replace("\\x","")
			print "hex       --> ",cleaninput
			print "plaintext -->  ",
			print "\b"+cleaninput.decode("hex")

if __name__ == '__main__':
	main()
