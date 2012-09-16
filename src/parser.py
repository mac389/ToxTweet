import nltk
import simplejson
from os import getcwd
from nltk.corpus import PlaintextCorpusReader
from nltk.text import Text
filename = 'test'
listing = open(filename,'r')
dictionary = {}

def tweettext_aslist(line):
    return  [result['text'] for result in eval(line)['results']]

for linenumber,line in enumerate(listing.readlines()):
    dictionary[str(linenumber)] = tweettext_aslist(line)

corpus = [tweets for tweets in dictionary.itervalues()]
corpus = [tweet for tweetlist in corpus for tweet in tweetlist]
savename ='cocaine.txt'

f = open(savename, 'w')
simplejson.dump(corpus,f)
f.close()

corpus_unique = set(corpus)
#Simple Semantic Analysis
lexical_diversity = len(corpus)/float(len(set(corpus)))
print 'Lexical Diversity is:',lexical_diversity

#Put a corpus    wrapper around it
corpus_legit = PlaintextCorpusReader(getcwd(),savename)

#sanitize
sanitized = [word for word in corpus_legit.words('cocaine.txt') if word.isalnum()]
print 'After sanitization, lexical diversity is',len(sanitized)/float(len(set(sanitized)))


def invalid(tweet):
    #Returns true if any of Nick's criteria are met

    #A tweet is invalid if the only time cocaine is mentioned is in somebody's handle
    handles = set(filter(lambda x: '@' in x , tweet.split(' ')))
    without_handles = [word for word in tweet.split(' ') if word not in handles]
    return not('cocaine' in without_handles or 'Cocaine' in without_handles)

f2 = open('sanitized_formatted_dev_d.txt','w')
f2.writelines(["%s\n" % tweet for tweet in corpus if not invalid(tweet)])
f2.close()

for_semantic_analysis = Text(corpus_legit.words())
for_semantic_analysis.similar('cocaine')

porter = nltk.PorterStemmer()
stemmed = map(porter.stem,corpus_legit.words())