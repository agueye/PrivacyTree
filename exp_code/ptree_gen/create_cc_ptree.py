# This code imports a list of country code (cc) paths and produces a privacy
# tree for each country. The node name for the root of each country privacy
# tree is the cc name. All trees are descendents under a master 'Root' node.

import pickle
import networkx as nx
from networkx.readwrite import json_graph
import json


#fileobject1=open('ccpaths.pkl','r')
#ccpaths=pickle.load(fileobject1)
#ccodes=pickle.load(fileobject1)
#ccpaths.sort() # the algorithm relies on the data being sorted
#fileobject1.close()

#ccpaths=ccpaths[0:100]
#print ccpaths

def gen_ptrees(ccpaths,ccodes):
    G=nx.DiGraph()
    G.add_node('Root')
    cclevel={}
    relabelmap={}
    count=0
    for path in ccpaths:
        #if path[0]=='US':
        #    print path
        #print "\n",path
        current='Root'
        for x in range(len(path)): 
            successors=G.successors(current)
            for s in successors:
                nodename=s
                cc=nodename.split("_")[0]
                if path[x]==cc:
                    found=True
                    break
            else:
                found=False
            if found:
                current=nodename
                continue                
            elif path[x] not in cclevel: # never seen this cc before
                cclevel[path[x]]=0
                level=0
            else: # need to add node but we've seen this cc before
                level=cclevel[path[x]]+1
                cclevel[path[x]]=level
            newnode=path[x]+"_"+str(level)
            G.add_edge(current,newnode)
            G.node[newnode]['cc']=path[x] # label each node with its cc
            if current=='Root':
                relabelmap[newnode]=path[x]
            #print "add edge",current,newnode
            current=newnode
        
        count=count+1
        if count % 10000==0:
            print(".")
        if count % 100000==0:
            print(" ",count)
    
    nx.relabel_nodes(G,relabelmap,False) # nodes off of root use cc as name
    #print "ccmap\n",ccmap
    return G
    

years=[2016]
for year in years:
    print(year)
    dirpath='../../../resultfiles/Results-Geolocation/ptree/'
    fname=dirpath+str(year)+'.ccpaths.pkl'
    fileobject1=open(fname,'rb')
    ccpaths=pickle.load(fileobject1)
    ccodes=pickle.load(fileobject1)
    ccpaths.sort() # the algorithm relies on the data being sorted
    fileobject1.close()

    G=gen_ptrees(ccpaths,ccodes)
    
    filename=str(year)+'.ccprivtrees.json'
    g_json = json_graph.node_link_data(G)
    json.dump(g_json,open(filename,'w'),indent=2)
        
    fname=dirpath+str(year)+".ccodes.pkl"
    fileobject2=open(fname,'wb')
    pickle.dump(ccodes,fileobject2)
    fileobject2.close()

    del G
    del ccpaths
    del ccodes
    
