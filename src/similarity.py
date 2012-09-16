from numpy import * 
from scipy import *
from numpy.random import randint
from numpy.linalg import norm
from matplotlib.pyplot import *
from matplotlib import rcParams
from xlrd import open_workbook

rcParams['text.usetex'] = True

'''
	Compare the similarity of tweets in a 26-dimensional space. Than ask if that angle is more than what
	could be expected from chance. Here, the random process must generate symbols with the same 
	distribution as the language in question. Otherwise, all tweets will be clustered together because
	they are all (hopefully) more like English than garbage. The assumption behind this is that tweets
	about a specific drug belong to a subcluster that has a unique frequency of symbols. There are
	better ways to project tweets onto a vector space, I'm sure. For now, though, let's try this
'''

#generate random letters
alphabet = list('abcdefghijklmnopqrstuvwxyz@?#')

def tweet_to_vector(tweet):
	answer = zeros((len(alphabet),))
	for position,letter in enumerate(alphabet):
		answer[position] = tweet.count(letter)
	return answer

def angle(first,second):
	return  dot(first,second)/(norm(first)*norm(second))

def similarity(tweets):
	return [[angle(tweet_to_vector(first),tweet_to_vector(second)) for first in tweets] for second in tweets]
	

#Load the coded data
def retrieve_tweets(drug_name):
	wb = open_workbook('../coding_master.xls')
	master_sheet = wb.sheet_by_index(0)
	return master_sheet.col_values(2)

#get actual_tweets				  
cocaine_tweets = retrieve_tweets('cocaine')
coke_similarity = similarity(cocaine_tweets)

tweet_length = 120
tweet_count = len(cocaine_tweets)
random_tweets = [''.join([alphabet[randint(len(alphabet))] for character in range(tweet_length)]) 
				  for tweet in range(tweet_count)]
	  
random_similarity = similarity(random_tweets) 
'''
figure()
imshow(random_similarity, interpolation='nearest', aspect='auto');colorbar()
title('Random Tweets')
xlabel('Tweet')
ylabel('Tweet')

figure()
imshow(coke_similarity, interpolation='nearest', aspect='auto');colorbar()
title('Cocaine Tweets')
xlabel('Tweet')
ylabel('Tweet')
'''

figure()
imshow(array(coke_similarity)-array(random_similarity), interpolation='nearest', aspect='auto');colorbar()
title('Difference in Similarity between pairs of cocaine tweets and random counterparts')
xlabel('Tweet')
ylabel('Tweet')

figure()
hist(tril(array(coke_similarity)-array(random_similarity)))
axvline(x=0,linewidth=3,color='r')
show()	