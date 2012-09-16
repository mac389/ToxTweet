from sys import argv

#Sanitize text
delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())


def lexdiv(aList):
	return len(set(aList))/float(len(aList))
'''
if argv[1]:
	filename = argv[1]
	with open(filename,'r') as f:
		text = f.readlines()[0]
	cleaner = [word.translate(None, delchars).lower() for word in text.split()]
	print round(lexdiv(cleaner),3)
'''
def ld(filename):
	with open(filename,'r') as f:
		text = f.readlines()[0]
	cleaner = [word.translate(None, delchars).lower() for word in text.split()]
	return round(lexdiv(cleaner),3)