
from nltk import *
from simplejson import load

formulary = ['cocaine','marijuana','bath salts','heroin','opium','lsd','valium','ativan','ecstasy','ketamine']

twits = {}
#For FK any tweet will do
for drug in formulary:
	filename = "results_"+drug.replace(' ','_')+".txt."
	with open(filename) as f:
		search_results = load(f)
		print 'Reading tweets for '+drug
		twits[drug] = [r['text'] for result in search_results for r in result['results']]


print '***********************************'
print 'Tweets Extracted into a dictionary called twits'
print 'To get all the tweets for cocaine type'
print "twits['cocaine']"
print "Available Drugs are: " 
print formulary
print '***********************************'
