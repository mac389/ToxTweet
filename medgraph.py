import numpy as np
import matplotlib.pyplot as plt
from numpy import loadtxt

# creation of the data
name_list = ['day1', 'day2', 'day3', 'day4']
filename = "nduh_ape.summary"
data = loadtxt(filename, delimiter=':', dtype = {'names': ('drugs','count'),'formats':('S10','i4')})
print data
colors_list = ['0.5', 'r', 'b', 'g'] #optional

def customize_barh(data, width_bar=1, width_space=0.5, colors=None):
    
    n = len(data) #Number of different categories
    nobs = sum([x[1] for x in data])
    print nobs
    
    #some calculation to determine the position of Y ticks labels
    total_space = (n*width_bar)+(n-1)*width_space
    ind_space = n*width_bar
    step = ind_space/2.
    pos = np.arange(step, total_space+width_space, ind_space+width_space)

    # create the figure and the axes to plot the data 
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_axes([0.15, 0.15, 0.65, 0.7])

    # remove top and right spines and turn ticks off if no spine
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('right')    # ticks position on the right
    # postition of tick out
    ax.tick_params(axis='both', direction='out', width=3, length=6,
                   labelsize=24, pad=8)
    ax.spines['left'].set_linewidth(3)
    ax.spines['bottom'].set_linewidth(3)

    # plot the data
    for i,(drug,count) in enumerate(data):
        if colors == None:
            ax.barh(pos-step+i*width_bar, 100*round(count/float(nobs),2), width_bar, #facecolor='0.4',
                    edgecolor='k', linewidth=3)
        else:
            ax.barh(pos-step+i*width_bar, 100*round(count/float(nobs),2), width_bar, facecolor=colors[i],
                    edgecolor='k', linewidth=3)


    ax.set_yticks(pos)
    # you may want to use the list of name as argument of the function to be more
    # flexible (if you have to add a people)
    print [x[0] for x in data]
    ax.set_yticklabels(tuple([x[0] for x in data]))         
    ax.set_ylim((-width_space, total_space+width_space))
    ax.set_xlabel('Percentage of Tweets', size=26, labelpad=10)

customize_barh(data)
plt.savefig('perf.png')
plt.show()