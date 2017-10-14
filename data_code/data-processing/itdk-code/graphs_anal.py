import sys, gzip, bz2
import networkx as nx
import pickle
import matplotlib.pyplot as plt


#############
## Check how the properties of the graph are correlated to the privacy


ds='2016-03'
G = nx.read_gpickle("World.cc."+ds+".gpickle.gz")
print(nx.info(G))
print(G.nodes())

#nx.draw(G,with_labels = True)
#plt.show()
