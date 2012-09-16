#!/usr/bin/env python
# Using twitter instead of python-twtter wrapper
import twitter
import networkx as nx
import re
import codecs
import csv
import xlwt
from httplib import BadStatusLine
class twitterQuery(object):
    def __init__ (self, drug_name):
        self.drug_name = drug_name
        try: #Look for a list of synonyms. If no list is found search Twitter jut using the drug name
            self.synonym_filename = self.drug_name + '_synonyms.csv'
            self.synonyms = [line for line in csv.reader(open(self.synonym_filename,'rt'))]
            self.synonyms = [synonym for line in self.synonyms for synonym in line]
        except IOError as e:
             self.synonyms = []
             self.synonyms.append(self.drug_name)
             # Calling list(self.drug_name) splits the string into a list of characters 
        #Assume that the synonyms are stored in a CSV file
        #Query Twitter with those synonyms-------------------------------------
        self.search = twitter.Twitter(domain="search.twitter.com")
        self.results = []
        self.page_count = 10
        self.radius = 10    
        self.locations = {'NYC':'40.665572,-73.923557'}
        self.rpp = 100
        self.query = ' OR'.join(self.synonyms)
        
        self.dial_in_tries = 4 #Sometimes Twitter's API flips a BadStatusLine error
        for attempt in range(self.dial_in_tries):
            try:
                for page in range(1,self.page_count+1): # Python countings from 0. Twitter from one.
                    self.results.append(self.search.search(q=self.query, 
                    rpp=100,page=page, geocode=self.locations['NYC']+','+str(self.radius)+'mi'))
                break
            except BadStatusLine,e:
                continue
	#self.save(format='XLS')
	self.save(format='JSON')
	
    def clean(self,tweet):
        verboten = ['@','RT','http://']
        handles = set(filter(lambda x: 1 in [symbol in x for symbol in verboten], tweet.split(' ')))
        return ' '.join([word for word in tweet.split(' ') if word not in handles])
   
    def save(self, format='XLS'):
        if format == 'XLS': #Saving to an XLS file for human rating
            import xlwt as xlwt
            corpus = [tweet['text'] for page in self.results for tweet in page['results']]
            #Make XLS Workbook with a sheet for everyone
            self.xls_wbk = xlwt.Workbook()
            self.everyone = {'Nick','Alex','Dan','Jen','Mike'}
            self.column = 1
            for person in self.everyone:
                sheet = self.xls_wbk.add_sheet(person)
                for row,tweet in enumerate(map(self.clean,set(corpus))):
                    sheet.write(row,self.column,tweet)
            self.xls_wbk.save(self.drug_name.replace(' ','_')+'_for_rating.xls')
        elif format == 'JSON': #Dumping tweets, for say graph theory analysis
            from simplejson import dump
            self.record_filename = 'results_'+self.drug_name.replace(' ','_')+'.txt'
            with open(self.record_filename,'a') as record:
                dump(self.results,record)
    
    def get_rt_sources(self,tweet):
        re_patterns = re.compile(r'(RT|via)((?:\b\W*@\w+)+)')
        return [source.strip() for entry in re_patterns.findall(tweet)
                    for source in entry if source not in ("RT","via")]
                    
    def make_graph(self,save_graph=True):
        graph = nx.DiGraph()
        all_tweets = [tweet for page in self.results for tweet in page['results']]
        for tweet in all_tweets:
            rt_sources = self.get_rt_sources(tweet["text"])
            if not rt_sources: continue 
            for rt_source in rt_sources:
                graph.add_edge(rt_source, tweet["from_user"], {"tweet_id": tweet["id"]})
        #--Calculate graph summary statistics
        if nx.is_connected(graph.to_undirected()):
            diameter  = nx.diameter(graph.to_undirected())         
            average_shortest_path = nx.average_shortest_path_length(graph.to_undirected())
            print 'Diameter: ', diameter
            print 'Average Shortest Path: ',average_shortest_path
        else:
             print "Graph is not connected so calculating the diameter and average shortest path length on all connected components."
             diameter = []
             average_shortest_path = []
             for subgraph in nx.connected_component_subgraphs(graph.to_undirected()):
                 diameter.append(nx.diameter(subgraph))
                 average_shortest_path.append(nx.average_shortest_path_length(subgraph))
             from numpy import median
             from scipy.stats import scoreatpercentile
             print 'Diameter: ',median(diameter),u'\xB1',str(scoreatpercentile(diameter,75)-scoreatpercentile(diameter,25))
             print 'Average Path Length :',median(average_shortest_path),u'\xB1',str(scoreatpercentile(average_shortest_path,75)-scoreatpercentile(average_shortest_path,25))
        degree_sequence=sorted(nx.degree(graph).values(),reverse=True) # degree sequence
           
        import matplotlib.pyplot as plt
        plt.loglog(degree_sequence,'b-',marker='o')
        plt.title("Distribution of Degrees for %s tweets" %(self.drug_name), fontsize=20)
        plt.ylabel("Degree", fontsize=20)
        plt.xlabel("Rank", fontsize=20)
        
        # draw graph in inset
        ax = plt.axes([0.35,0.25,0.55,0.55])
        plt.axis('off')
        nx.draw(graph, ax=ax, alpha=0.8, with_labels=False)
        
        plt.savefig("degree_distribution_%s.png"%(self.drug_name.replace(' ','_')), dpi=300)
        plt.close()
        if save_graph:
            output_file = self.drug_name.replace(' ','_') + '.dot'
            try:
                nx.drawing.write_dot(graph,output_file)
                print 'Graph saved as ',output_file
            except (ImportError, UnicodeEncodeError) as e:
                dot = ['"%s" -> "%s" [tweetid=%s]' % (node1,node2,graph[node1][node2]['tweet_id']) 
                        for node1,node2, in graph.edges()]
                with codecs.open(output_file,'w', encoding='utf-8') as f:
                    f.write('strict digraph G{\n%s\n}' % (';\n'.join(dot),))
                    print 'Saved ',output_file,' by brute force'
        return diameter, average_shortest_path
                    