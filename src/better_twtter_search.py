#!/usr/bin/env python
# Using twitter instead of python-twtter wrapper
import twitter
import networkx as nx
import re
import codecs
#---------------------------Helper Functions--------------------------------
###########################################################################
def get_rt_sources(tweet):
	'''
		get_rt_sources finds the tweet(s) to which the tweet passed to the function responds
	'''
	re_patterns = re.compile(r'(RT|via)((?:\b\W*@\w+)+)')
	return [source.strip() for entry in re_patterns.findall(tweet)
				for source in entry if source not in ("RT","via")]
#---------------------------------------------------------------------------
############################################################################
#------------------------Query Twitter--------------------------------------
search = twitter.Twitter(domain="search.twitter.com")
results = []
page_count = 10

locations = {'NYC':'40.665572,-73.923557'}
keywords = ['Hi','There']
radius = 10    
for page in range(1,page_count+1): # Python begins counting from 0. Twitter begins from one.
    results.append(search.search(q=' OR '.join([word for word in keywords]), \
					rpp=100,page=page, geocode=locations['NYC']+','+str(radius)+'mi')) 
#---------------------------------------------------------------------------
############################################################################
#-----------------------Build Graph-----------------------------------------
graph = nx.DiGraph()
all_tweets = [tweet for page in results for tweet in page['results']]
for tweet in all_tweets:
	rt_sources = get_rt_sources(tweet["text"])
	if not rt_sources: continue 
	for rt_source in rt_sources:
		graph.add_edge(rt_source, tweet["from_user"], {"tweet_id": tweet["id"]})
#---------------------Visualize Graph---------------------------------------
output_file = 'test_graph.dot'
try:
	nx.drawing.write_dot(graph,output_file)
	print 'Graph saved as ',output_file
except ImportError, e:
	dot = ['"%s" -> "%s" [tweetid=%s]' % (node1,node2,graph[node1][node2]['tweet_id']) 
			for node1,node2, in graph.edges()]
	with codecs.open(output_file,'w', encoding='utf-8') as f:
		f.write('strict digraph {\n%s\n}' % (';\n'.join(dot),))
		print 'Saved ',output_file,' by brute force'