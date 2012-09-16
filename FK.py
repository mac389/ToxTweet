#Calculate FleshKincaid from Tweets

from nltk import * #Such a hack
from simplejson import load
from readabilitytests import ReadabilityTool

#Attribution: ReadabilityTests comes from NTLKs Google Project page.

formulary = ['cocaine','marijuana','bath salts','heroin','opium','lsd','valium','ativan','ecstasy','ketamine']

def clean(tweet):
    verboten = ['@','RT','http://','#']
    handles = set(filter(lambda x: 1 in [symbol in x for symbol in verboten], tweet.split(' ')))
    return ' '.join([word for word in tweet.split(' ') if word not in handles])

def getFK(text=text):
	grader=ReadabilityTool(text)
	return grader.FleschKincaidGradeLevel()

grade_level=[]
for drug in formulary:
	filename = "results_"+drug.replace(' ','_')+".txt"
	with open(filename,'r') as f:
		data = load(f)		
		grade_level.append(getFK(data[0]['results'][0]['text']))
		
print grade_level

