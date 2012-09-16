import twitterQuery as tQ
import numpy as np
import matplotlib.pyplot as plt
from cPickle import dump, load


#--Formulary lists the "drugs" to search for on Twitter

#formulary = ['cocaine','marijuana','bath salts','heroin','lsd','valium','ativan','ecstasy','ketamine']
formulary = ['coffee','beer']


graph_stats = []
for count,drug in enumerate(formulary):
	print 'Querying Twitter for ',drug,' and writing the results to an XLS file.'
	query = tQ.twitterQuery(drug)
	degree,path_length = query.make_graph()
	print 'Finding the Retweet Graph. Saving it and a rank-sorted histogram of the degrees of its nodes.'
	graph_stats.append((degree,path_length))

with open('graph_stats.p','wb') as file:
	dump([formulary,graph_stats],file)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.boxplot([data[0] for data in graph_stats])
ax2 = fig.add_subplot(212)
ax2.boxplot([data[1] for data in graph_stats]) 
plt.title('Graph theoretic differences among commonly abused drugs.')
ax2.xaxis.set_ticks(range(1,len(formulary)+1),formulary)

plt.savefig('summary.png',dpi=300)
plt.show()