# This code is for importing list(s) of AS paths and converting them into
# country code (cc) paths.

import pickle

#filename1='asn_to_cc.pkl'
#fileobject1=open(filename1,'r')
#asn_to_cc=pickle.load(fileobject1)

#filename='20151201.all-paths_reduced'
#filename='20151201_IPV4.all-paths_reduced'
#fileobject=open(filename,'r')
#data=fileobject.readlines()

filepath='../datafiles/data-Geolocation/yearlyGeoFiles/'


years=[2015, 2016]

for year in years:
    count=0
    paths={}
    ccdict={}
    filename=filepath+str(year)+'.geodata.txt'
    with open(filename,'r') as fileobject:
        data=fileobject.readlines()

        for line in data:
            count=count+1
            linedata=line.split('|')  
            if '??' in linedata:
                continue
            #linedata=linedata[:-1]
            #print linedata

            # Remove adjacent duplicate country labels in each list
            cclist=linedata[:-1]
            ccdict.update(dict(zip(cclist, [True]*len(cclist))))
            #for elem in linedata:
            #    if elem==prev:
            #        continue
            #    cclist.append(elem)
            #    ccdict[elem]=True # store a dict of cc observed
            #    prev=elem
            #print cclist

            # Create sublists and remove duplicate paths
            for x in range(len(cclist)):
                path=tuple(cclist[x:])
                #print path
                if path not in paths:
                    paths[path]=True

            #if count % 200==0:
            #    break

            if count % 100000==0:
                print(".")
                if count % 1000000==0:
                    print(" ",count)

    ccodes=list(ccdict.keys()) # List of all observed country codes
    ccpaths=list(paths.keys()) # List of all cc paths

    if 1==1:
        fname=str(year)+".ccpaths.pkl"
        fileobject2=open(fname,'wb')
        pickle.dump(ccpaths,fileobject2)  
        pickle.dump(ccodes,fileobject2)
        fileobject2.close()

    print(year)
    print("File lines",count)
    print("ccodes",len(ccodes))
    print("Distinct paths",len(ccpaths))
    print(sorted(ccodes))

    #ccpaths.sort()
    #for line in ccpaths:
    #    print line
