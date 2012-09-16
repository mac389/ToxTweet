from nltk import *
from csv import reader
from numpy import *

#Need to make training set
#load 1st and 3rd columns of coding master

#drug_mule = reader(open('coding_master.csv', 'rb'), delimiter=',', quotechar='|')
drug_mule = genfromtxt('astext.txt',delimiter=' ', usecols = (1,2))