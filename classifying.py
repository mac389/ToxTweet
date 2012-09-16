from numpy import *
from nltk import NaiveBayesClassifier, classify, FreqDist
from xlrd import open_workbook

#Load the coded data
def retrieve_tweets(drug_name):
	wb = open_workbook('coding_master.xls')
	master_sheet = wb.sheet_by_index(0)
	return zip(master_sheet.col_values(2),master_sheet.col_values(0))

def clean(tweet):
	return (filter(lambda x: len(x)>2,tweet[0].split()),tweet[1])
	
def split_by_category(categorized_tweets):
	answer = {}
	for text,rating in categorized_tweets:
		if int(rating) not in answer:
			answer[int(rating)] = text
		else:
			answer[int(rating)].extend(text)
	return answer
formulary = ['cocaine'] 
tweets = [map(clean,retrieve_tweets(drug)) for drug in formulary]

stratified_by_rating = split_by_category(tweets[0])
freq_dists = [FreqDist(text) for text in stratified_by_rating.itervalues()]
word_lists = map(lambda x:x.keys(),freq_dists)

all_together_word_list = [word for word_list in word_lists for word in word_list]

def extract_features(document):
	return  {'contains(%s)'% word: (word in set(document)) for word in all_together_word_list} 
training_set = classify.util.apply_features(extract_features,tweets[0])

classifier = NaiveBayesClassifier.train(training_set)
#print classifier.show_most_informative_features()
tweet = 'I am going to school.'
print classifier.classify(extract_features(tweet.split()))