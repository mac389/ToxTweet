import twitter as twitter
import nltk as nltk
import urllib as urllib
import simplejson as simplejson
import networkx as nx
import re
from matplotlib.pyplot import *


#Load Keywords
#Initial Set from Roget's Thesaurus and Urban Dictionary <-- This retrieved no tweets. Just using the word 'cocaine' for now
#What about doing both English and Spanish?
keyword_filename = 'synonyms_cocaine_devtest.txt'
delimiter = ','
keyword_file = open(keyword_filename)
keywords = keyword_file.readline().split(delimiter)
keyword_file.close()
locations = {
             'NYC':'40.665572,-73.923557'}
def format_search_string(keywords,location, radius=10, results = 100):
    header = 'http://search.twitter.com/search.json?q='
    answer = header + ' OR '.join(keywords)
    if  location in locations.keys():
        answer += ' &geocode='+locations[location]+','+str(radius)+'mi'+'&rpp='+str(results)
    return answer

def search_tweets(url):
    search = urllib.urlopen(url)
    return simplejson.loads(search.read())

#----------------Using the twitter module, find NG's tweets--------------------------------
private_key= '    Ip80obhVONbdbIBlEsXhIh8da2mTEtWbPb9QoZIA'
private_token = 'SaSNZ7iVvOwtEhFSAblCShrnI8TARZcFKm61U8KEPc'
public_key= 'JGZXNDxaF05qONatyWbG1Q'
public_token = '508152927-RB2uCho8ukfDBGZliVqeeWJtompqnB9wk6PHVaAN'

api = (twitter.Api(consumer_key = public_key, consumer_secret = private_key,
        access_token_key=public_token, access_token_secret = private_token))

result = search_tweets(format_search_string(keywords,'NYC', results=100))
text_results = text_results = [ item['text'] for item in result['results']]

#----------------Build a graph based on retweets---------------------------------------------
#----Much of this code comes from p12 of O'Reilly's Mining the Social Web

g = nx.DiGraph()
def get_rt_sources(tweet):
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    return [source.strip() for _ in rt_patterns.findall(tweet)
            for source in tuple
            if source not in ("RT","via")]
for tweet in result['results']:

    rt_sources = get_rt_sources(tweet['text'])
    if not rt_sources:continue
    for rt_source in rt_sources:
        print tweet['from_user']
        g.add_edge(rt_source, tweet['from_user'],{'tweet_id',tweet['id']})
savename = "coke.dot"
nx.draw(g)
print g.number_of_nodes()
#---------------------------------------------------------------------------------------------
##############################################################################################
#------------------Append the results to a text file for later analysis-----------------------
record_filename = 'results_cocaine_devtest.txt'
record = open(record_filename,'a')
simplejson.dump(result,record)
record.close()
print 'Saved'
#---------------------------------------------------------------------------------------------