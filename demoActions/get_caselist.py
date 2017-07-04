import os

def get_caselist():	
	caselist = []
	f = open("./caseList.txt","r")
	lines = f.readlines()

	for line in lines:
		str1 = line[:-1]
		caselist.append(str1)


	norunlist = []
	for case in caselist:
		if (case not in passlist) & (case not in faillist):
			norunlist.append(case)

	print "no-run list:"
	for case in norunlist:
		print case

if __name__ == "__main__":
	caselist = get_caselist()
	print caselist
