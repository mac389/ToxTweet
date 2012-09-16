#Calculate FleshKincaid from Tweets

from nltk import * 
from simplejson import load

formulary = ['cocaine','marijuana','bath salts','heroin','opium','lsd','valium','ativan','ecstasy','ketamine']

tweets = []
#For FK any tweet will do
for drug in formulary:
	filename = "results_"+drug.replace(' ','_')+".txt"
	with open(filename,'r') as f:
		data = load(f)		
		tweets.append(getFK(data[0]['results'][0]['text']))
		
print tweets

