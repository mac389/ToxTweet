from lexdiv import ld
from pprint import pprint
filenames = ['ketamine','cocaine','bathsalts','ativan','MDMA','heroin','marijuana','lsd']
suffix = '1A'
diversity = [ld('.'.join([file,suffix])) for file in sorted(filenames)]

results = {filename:diverse for (filename,diverse) in zip(sorted(filenames),diversity)}
print 'Drug :::::::::: Lexical Diversity'
pprint(results.items())