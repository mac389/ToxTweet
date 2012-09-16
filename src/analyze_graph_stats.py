#Analyze graph_stats
from cPickle import load
import matplotlib.pyplot as plt
filename = 'graph_stats.p'


formulary = ['Cocaine','Marijuana','Bath salts','Heroin','Opium','LSD','Valium','Ativan','Ecstasy','Ketamine']
graph_stats = []
with open(filename,'r') as file:
	graph_stats = load(file)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.set_title('Differences in net degree and path lengths among commonly abused drugs', fontsize=15, weight='bold')
bp1 = ax1.boxplot([data[0] for data in graph_stats], notch=1,sym='+')
plt.setp(bp1['boxes'], color='black', linewidth=3)
plt.setp(bp1['whiskers'], color='black', linewidth=3)
plt.setp(bp1['fliers'], color='black', marker='+', linewidth=2)
plt.setp(bp1['medians'], color='black', marker='+', linewidth=2)
ax1.set_ylabel('Median degree', fontsize=12, weight='bold')
ax2 = fig.add_subplot(212)
bp2 = ax2.boxplot([data[1] for data in graph_stats]) 
plt.setp(bp2['boxes'], color='black', linewidth=3)
plt.setp(bp2['whiskers'], color='black', linewidth=3)
plt.setp(bp2['fliers'], color='black', marker='+', linewidth=2)
plt.setp(bp2['medians'], color='black', marker='+', linewidth=2)
ax2.set_ylabel('Median path length', fontsize=12,weight='bold')
ax2.xaxis.set_ticks(range(1,len(formulary)+1),formulary)
xtickNames = plt.setp(ax2, xticklabels=formulary)
plt.setp(ax1,xticklabels='')
plt.setp(xtickNames, rotation=45, fontsize=10, weight='bold')
plt.tight_layout()
plt.savefig('graph_summary.png',bbox_inches='tight',dpi=300)
