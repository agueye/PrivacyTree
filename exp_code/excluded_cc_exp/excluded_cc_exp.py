# This code is for importing list(s) of AS paths and converting them into
# country code (cc) paths.

import pickle
from random import sample
from random import choice

def import_ccmap(dataset,year):
    filename='../datafiles/'+dataset+'pre-processed/'+str(year)+'.ccmap-paths.txt'
    fileobject=open(filename,'r')
    count=0  
    paths=0
    thrownout=0
    ccmap={}
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            line=line.strip('\n')
            count=count+1
            if count % 1000000==0:
                print(".")
                if count % 20000000==0:
                    print(" ",count)          
            linedata=line.split('|')
            #print linedata                      
            cclist=[]
            prior=None
            for x in range(len(linedata)-1):
                cc=linedata[x]  
                if cc!=prior:
                    cclist.append(cc) 
                prior=cc        
            if 'U' in cclist:
                thrownout=thrownout+1
                continue
            for x in range(len(cclist)):
                sublist=cclist[x:]
                src=sublist[0]
                dst=sublist[-1]
                sublist=sublist[1:-1]
                ccset=set(sublist)
                if src in ccset:
                    ccset.remove(src)
                if dst in ccset:
                    ccset.remove(dst)
                sublist=list(ccset)
                sublist.sort()
                if src not in ccmap:
                    ccmap[src]={}
                if dst not in ccmap[src]:
                    ccmap[src][dst]=set()                
                cctuple=tuple(sublist)
                ccmap[src][dst].add(cctuple)
            #print
            paths=paths+1                            
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines    
    fileobject.close()    
    return ccmap   

def excluded_cc_exp(src_cc_set,ccmap,resfile,year,only_src_set=False,both_ways=False,trials=500,verbose=True,todisk=True):
    if both_ways:
        assert only_src_set
        filename="../resultfiles/"+resfile+str(year)+".excludedcc_bothways.csv"        
    elif only_src_set:
        filename="../resultfiles/"+resfile+str(year)+".excludedcc_onlysrc.csv"
    else:
        filename="../resultfiles/"+resfile+str(year)+".excludedcc.csv"
    print("output file:",filename)
    fileobject=open(filename,'w')
    output="sourcecc,nexcluded,ngood,nbad,nmixed,goodratio,badratio,definedratio,mixedratio\r\n"
    fileobject.write(output)
    
    auclist=[]
    for sourcecc in src_cc_set: # perform experiment individually on each country
        if verbose:
            print("Evaluating",sourcecc)
        exclusionset=set(ccmap.keys())
        exclusionset.remove(sourcecc) # set of all countries other than sourcecc
        start=0
        auc=0
        for nexcluded in range(start,len(exclusionset)+1,10):
            g=b=m=0
            mixratiolist=[]
            for trial in range(trials):
                excluded=list(sample(exclusionset,nexcluded))
                if verbose:
                    excluded.sort()
                    #print excluded
                if only_src_set:
                    dstcc=choice(src_cc_set)
                else:
                    dstcc=choice(list(ccmap[sourcecc].keys()))
                
                # Check forward paths                
                badp=0
                goodp=0
                for path in ccmap[sourcecc][dstcc]:
                    for excludedcc in excluded:
                        if excludedcc in path:
                            badp=badp+1
                            break
                    else:
                        goodp=goodp+1
                
                # Check backwards paths  
                if both_ways:
                    for path in ccmap[dstcc][sourcecc]:
                        for excludedcc in excluded:
                            if excludedcc in path or excludedcc==dstcc:
                                badp=badp+1
                                break
                        else:
                            goodp=goodp+1

                assert goodp>0 or badp>0                 
                if badp==0:
                    g=g+1
                    result=1
                elif goodp==0:
                    b=b+1
                    result=-1
                else:
                    m=m+1
                    result=0
                    mratio=goodp*1.0/(goodp+badp)
                    mixratiolist.append(mratio)
#                if verbose:
#                    print("  ",sourcecc,dstcc,goodp,badp)
            if len(mixratiolist)>0:
                mixratio=sum(mixratiolist)*1.0/len(mixratiolist)   
                mixratio=int(mixratio*100)*1.0/100
            else: 
                mixratio=0
            goodratio=g*1.0/(g+b+m)
            badratio=b*1.0/(g+b+m)
            defratio=(g+b)*1.0/(g+b+m)
            defratio=int(defratio*100)*1.0/100
            if verbose:
                print("%d %s %d: (%d,%d,%d) def=%.2f mix=%.2f" % (year,sourcecc,nexcluded,g,b,m,defratio,mixratio))       

            output=sourcecc+","+str(nexcluded)+","+str(g)+","+str(b)+","+str(m)+","+str(goodratio)+","+str(badratio)+","+str(defratio)+","+str(mixratio)+"\r\n"
            fileobject.write(output)
            
            auc=auc+defratio
        auc=auc/24
        auc=int(auc*100)*1.0/100
        auclist.append([sourcecc,auc])
        fileobject.write("\n")
    output=""
    for pair in auclist:
        output=output+pair[0]+" "+str(pair[1])+"\n"
        if verbose:
            print(pair[0],pair[1])
    fileobject.write(output)
    fileobject.close()
    
# BEGIN MAIN PROCEDURE ************************************************

resfile = "Results-Geolocation/"
dataset="data-Geolocation/"


# These are the country codes that had at least 1 router reporting BGP data and that had
# over 100,000 destination prefixes (generally countries had less than 8000 or more than 400,000)
# We only test paths between these countries so that we can model both forward and backwards routes
targetcc=['AU','BR','CA','CH','EU','RU','US']
#targetcc=['FR','RU']
print("Target cc codes=",targetcc)

years=[2015, 2016]

for year in years:

    ccmap=import_ccmap(dataset,year)
    # This generate the data for the figures (x-axis number of excluded countries, y-axis
    # represents ratios: % good, % bad, % we can give a definitive answer)
    # It also calculates the AUC for the definitive answer for each country
    only_src_set=False
    both_ways=False
    excluded_cc_exp(targetcc,ccmap,resfile,year,only_src_set,both_ways)

    only_src_set=True
    both_ways=False
    excluded_cc_exp(targetcc,ccmap,resfile,year,only_src_set,both_ways)

    only_src_set=True
    both_ways=True
    excluded_cc_exp(targetcc,ccmap,resfile,year,only_src_set,both_ways)
