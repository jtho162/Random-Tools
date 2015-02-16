#!/usr/bin/python3

from netaddr import IPNetwork, iter_iprange, glob_to_iprange 
import re
import sys
import os.path

'''
The program now has support for the following.  Allows for , and ; as a means to break the rows.
Note:  When CIDR notation is used, the program removes the network and broadcast address.
192.168.1.1
192.168.1.1-192.168.1.3
192.168.1.1/24
192.168.1.1-50
192.168.1.*
'''
def process(i):

	if re.search('-', i):
		dash2(i)
		withdash(i)
        
	elif re.search('/',i):
		for ip in IPNetwork(i).iter_hosts():
			print(ip)

	elif re.search('^/s*$', i):
		pass

	elif re.search('\*+', i):
		for ips in glob_to_iprange(i):
			print(ips)

	elif len(i) == 0:
		pass

	else:
		print(i.lstrip().rstrip())


def withdash(j):
    try:
        c = j.split('-')

        firstip, secondip  = c[0].lstrip().rstrip(), c[1].lstrip().rstrip()

        listfirstip, listsecondip = list(firstip.split('.')), list(secondip.split('.'))

        start, end = int(listfirstip[3]), int(listsecondip[3])

        first_3_octects = listfirstip[0:3]
        first_3 = (".".join(str(dot) for dot in first_3_octects))

        while start <= end:
            print(first_3 + "." + str(start))
            start = start + 1
    except IndexError:
        pass

def dash2(j):
    try:
        c = j.split('-')
        if len(c[1]) <= 3:
            firstip, secondip  = c[0].lstrip().rstrip(), c[1].lstrip().rstrip()
            listfirstip, listsecondip = list(firstip.split('.')), list(secondip.split('.'))
            start, end = int(listfirstip[3]), int(listsecondip[0])
            first_3_octects = listfirstip[0:3]
            first_3 = (".".join(str(dot) for dot in first_3_octects))
        
            while start <= end:
                print(first_3 + "." + str(start))
                start = start + 1

    except IndexError:
        pass

def usage():
	print("\n" + "Example Usage is:  ./ipparser.py \"nameoffile.txt\"" + "\n")

def main():
	try:
		filename = sys.argv[1]
		if os.path.isfile(filename):
			pass
		else:
			print("File not found")

		with open(filename, 'r') as f:
			newlist = [line.strip() for line in f]
		
		for i in newlist:

			if re.search(',', i):
				j = i.split(',')
				for k in j:
					process(k)
			
			elif re.search(';', i):
				j = i.split(';')
				for k in j:
					process(k)

			else:
				process(i)        

	except:
		print( "You must supply a file to parse")
		usage()

	sys.exit(2)

if __name__ == "__main__":
    main()
