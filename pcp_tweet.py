#from tweepy import *
import twitter as twitter
import nltk as nltk
import urllib as urllib
import simplejson as simplejson

#---------------------Helper Functions--------------------------------------------------------
def search_tweets(url):
	search = urllib.urlopen(url)
	dict = simplejson.loads(search.read())
	return dict
def get_words_tweets(tweets):
	return [words for words,_sentiment in tweets] 
	#Tuple unpacking in a list comprehension is faster than a for-loop

def get_words_features(word_list): return nltk.FreqDist(word_list).keys()
	#Is this better as an anonymous function?

def extract_features(document): #Cannot explicitly pass all inputs because this function			
	document_words = set(document)	#is mainly used as an input to a mapping function			
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document)
	return features
#---------------------------------------------------------------------------------------------
##############################################################################################
#----------------Using the twitter module, find NG's tweets--------------------------------
private_key= '	Ip80obhVONbdbIBlEsXhIh8da2mTEtWbPb9QoZIA'
private_token = 'SaSNZ7iVvOwtEhFSAblCShrnI8TARZcFKm61U8KEPc'
public_key= 'JGZXNDxaF05qONatyWbG1Q'
public_token = '508152927-RB2uCho8ukfDBGZliVqeeWJtompqnB9wk6PHVaAN'

api = (twitter.Api(consumer_key = public_key, consumer_secret = private_key, 
		access_token_key=public_token, access_token_secret = private_token))

search_string = 'http://search.twitter.com/search.json?q=PCP OR pcp smoked OR smoke OR smoking &geocode=40.665572,-73.923557,10mi'
result = search_tweets(search_string)
text_results = text_results = [ item['text'] for item in result['results']]
print text_results
#---------------------------------------------------------------------------------------------
##############################################################################################
'''
#---------------------Test Data-------------------------------------------------------------
pcp_tweets = [ #more efficient coding although probably slower to use regular expressions unless 
			   #the words branch heavily
			('PCP','positive'),
			('pcp', 'positive')]

#For such a small example, filtering is not necessary		
#---------------------------------------------------------------------------------------------
##############################################################################################
#----------------------------Extract features ------------------------------------------------
word_features = get_words_features(get_words_tweets(tweets))
#---------------------------------------------------------------------------------------------
##############################################################################################
#----------------------------Decide which features are relevant-------------------------------
training_set = nltk.classify.apply_features(extract_features, tweets)
#---------------------------------------------------------------------------------------------
##############################################################################################
#----------------------------Classify Bayesian classifier-------------------------------------
classifier = nltk.NaiveBayesClassifier.train(training_set) 
'''
