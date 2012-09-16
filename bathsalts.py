import twitter as twitter
import nltk as nltk
import urllib as urllib
import simplejson as simplejson
import numpy


#Load Keywords 
keyword_filename = 'synonyms_bathsalts.txt'
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

#----------------Query Twitter using your private token--------------------------------
private_key= '    Ip80obhVONbdbIBlEsXhIh8da2mTEtWbPb9QoZIA'
private_token = 'SaSNZ7iVvOwtEhFSAblCShrnI8TARZcFKm61U8KEPc'
public_key= 'JGZXNDxaF05qONatyWbG1Q'
public_token = '508152927-RB2uCho8ukfDBGZliVqeeWJtompqnB9wk6PHVaAN'

api = (twitter.Api(consumer_key = public_key, consumer_secret = private_key, 
        access_token_key=public_token, access_token_secret = private_token))

result = search_tweets(format_search_string(keywords,'NYC', results=100))
text_results = text_results = [ item['text'] for item in result['results']]
#---------------------------------------------------------------------------------------------
##############################################################################################
#------------------Append the results to a text file for later analysis-----------------------
record_filename = 'results_bathsalts.txt'
record = open(record_filename,'a')
simplejson.dump(result,record)
record.close()
print 'Saved'