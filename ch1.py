from nltk import *
from nltk.book import *
from sys import argv
from numpy import *
from scipy import *

def q4():
	print "***********************************"
	print "*Question 4:" 
	
	words = [thing for thing in text2 if thing.isalpha()]
	# An alternate solution
	# words = map(lambda word: word if word.isalpha(), text2)
	print "* How many words are there in text2? -->", len(words) 
	print "* How many unique words are there? -->", len(set(words))
	print "* Lexical Diversity -->", len(set(words))/float(len(words))
	print "***********************************"

def q6():
	print "***********************************"
	print '* Remember that you need NumPy and SciPy installed for dispersion plots to work'
	text2.dispersion_plot(['Elinor','Marianne','Edward','Willoughby'])
	print 'I think Marianne and Willoughby are in a relationship.'
	print "***********************************"

def q7():
	print "***********************************"
	print "* Finding collocations in the Chat corpus"
	print "* A collocation is a sequence of words that occur together by more than chance."
	text5.collocations()
	print "***********************************"

def q14():	
	print "***********************************"
	print "* Find all instances in of 'the' in the first sentence of the Book of Genesis"
	indices = [index for index,word in enumerate(sent3) if word == 'the']
	print "* Indices of instances of 'the' -->", indices
	print "***********************************"

def q15():
	print "***********************************"
	print "* Find all words in the Chat Corpus that being with 'b'. List the results alphabetically."
	b_beginning = set([word for word in text5 if word.isalpha() and word.startswith('b')])
	print sorted(b_beginning)
	print "***********************************"

def flatten(aList): 
	return [item for sublist in aList for item in sublist]

def q18():
	print "***********************************"
	print "* Determine the vocabulary of the first sentences of all the works in the corpora."
	sent_list = ['sent1','sent2','sent3','sent4','sent5','sent6','sent7','sent8']
	vocabulary= set(filter(lambda x: x.isalpha, flatten(map(eval,sent_list))))
	#Alternate solution
	# vocabulary = set([type for type in map(eval(sent_list)) if type.isalpha()])
	print '* Vocablary --> ',vocabulary
	print "***********************************"

def q22():
	print "***********************************"
	print "* Find All 4 letter words in the Chat Corpus. Display them in order of decreasing frequency"
	four_letter_words = [word for word in text5 if word.isalpha() and len(word) == 4]
	fdist = FreqDist(four_letter_words)
	print fdist.keys()
	print "***********************************"
	
def q23():
	print "***********************************"
	print "* Printing All Words in Caps in Monty Python's Holy Grail"
	for word in text6:
		if word.isupper():
			print word
	print "***********************************"

def q24():
	print "***********************************"
	print "* Printing all words in Monty Python's Holy Grail that end with -ize"
	print [word for word in text6 if word.isalpha() and word.endswith('ize')]
	#Alternate solution:
	# print filter(lambda x: x if x.isalpha() and x.endswith('ize'),text6)
	print "* Printing all words that contain the letter 'z'"
	print [word for word in text6 if word.isalpha() and 'z' in word]
	print "* Printing all words that contain the cluster 'pt'"
	print [word for word in text6 if word.isalpha() and 'pt' in word]
	print "* Printing all words if they occur in a title"
	print [word for word in text6 if word.isalpha() and word == word.title()]
	print "***********************************"

def q27():
	print "***********************************"
	

if __name__=='__main__':
	eval('q'+''.join(argv[1:])+'()')