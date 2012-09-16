import nltk
import simplejson
from os import getcwd
from nltk.corpus import PlaintextCorpusReader
from nltk.text import Text
import xlwt as xlwt
from sys import argv
#-------------------------------------------------------------------------------------
#############################HELPER FUNCTIONS#########################################
#-------------------------------------------------------------------------------------
print sys.argv
def tweettext_aslist(line):
    return  [result['text'] for result in eval(line)['results']]

def clean(tweet):
    #Returns true if any of Nick's criteria are met
    #A tweet is invalid if the only time marijuana is mentioned is in somebody's handle
    handles = set(filter(lambda x: '@' in x or 'RT' in x or 'http://' in x , tweet.split(' ')))
    without_handles = [word for word in tweet.split(' ') if word not in handles]
    print ' '.join(without_handles)
    return ' '.join(without_handles)
#-------------------------------------------------------------------------------------
#############################LOADING TWEETS & SAVING XLS##############################
#-------------------------------------------------------------------------------------
#Load the txt file that contains the twitter results in JSON format
filename = 'results_marijuana.txt'
listing = open(filename,'r')
dictionary = {}

for linenumber,line in enumerate(listing.readlines()):
    dictionary[str(linenumber)] = tweettext_aslist(line)

corpus = [tweets for tweets in dictionary.itervalues()]
corpus = [tweet for tweetlist in corpus for tweet in tweetlist]
corpus_unique = set(corpus)
#------------------------------------------------------------------------------------
#Make XLS Workbook with a sheet for everyone
xls_wbk = xlwt.Workbook()
everyone = {'Nick','Alex','Dan','Jen','Mike'}
column = 1
for person in everyone:
	sheet = xls_wbk.add_sheet(person)
	for row,tweet in enumerate(map(clean,set(corpus))):
		sheet.write(row,column,tweet)
xls_wbk.save('marijuana.xls')
#--------------------------------------------------------------------------------------
''' 
	Save just the tweet portion of the Twitter query to a new txt file. Otherwise, NLTK
	won't be able to deal with it. 
	'''
savename ='m_bathsalts.txt'
with open(savename, 'w') as f:
	simplejson.dump(corpus,f)

corpus_legit = PlaintextCorpusReader(getcwd(),savename)
sanitized = [word for word in corpus_legit.words('m_bathsalts.txt') if word.isalnum()]
#-------------------------------------------------------------------------------------
#####################################ANALYSIS#########################################
#-------------------------------------------------------------------------------------
#Lexical Diveristy
print 'Lexical Diversity is:', len(map(clean,corpus))/float(len(map(clean(set(corpus))))
#-------------------------------------------------------------------------------------
#Frequency of most common words
#-------------------------------------------------------------------------------------
for_semantic_analysis = Text(corpus_legit.words())
for_semantic_analysis.similar('bath salts')
stemmed = map(nltk.PorterStemmer().stem,corpus_legit.words())
