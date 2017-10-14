# This code is for importing list(s) of AS paths and converting them into
# country code (cc) paths.

import pickle
from random import sample
from random import choice

def getccpaths(mode,targetcc,prefix_thresh=100000):
    assert mode=="paths" or mode=="sets"
    filename='20151201_IPV4_with_prefix.all-paths_reduced'
    fileobject=open(filename,'r')
    
    count=0  
    crossed={} # key is (prefix), value is observed intermediary countries  
    cc_to_asn={}
    #ccodes=set()
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            count=count+1
            if count % 1000000==0:
                print ".",
                if count % 20000000==0:
                    print " ",count
            
            linedata=line.split('|') 
                  
            cclist=[]
            prior=None
            for x in range(len(linedata)-1):
                asn=linedata[x]
                if asn in asn_to_cc:
                    cc=asn_to_cc[asn]
                else:
                    cc="U"    
                if cc!=prior:
                    cclist.append(cc) 
                prior=cc
            dst=cclist[-1]
            if dst not in targetcc and len(targetcc)>0:
                continue
            
            if cclist[0] in targetcc:
                asn=linedata[0] # AS that reported this path
                if cclist[0] not in cc_to_asn:
                    cc_to_asn[cclist[0]]=set()
                cc_to_asn[cclist[0]].add(asn) # Record each reporting AS for each cc            
            #assert len(set(cclist))==len(cclist)

            prefix=linedata[-1].split()[0] # add prefix but remove ' \r\n' 
            #assert "." in prefix
    
            # Create sublists and remove duplicate paths
            for x in range(len(cclist)-1):
                if cclist[x] in targetcc or len(targetcc)==0:
                    src=cclist[x]
                    #ccodes.add(cclist[x])
                    ccdata=cclist[x+1:] 
                    #ccodes.update(ccdata)
                    if src not in crossed:
                        crossed[src]={}
                    if dst not in crossed[src]:
                        crossed[src][dst]={}
                    if prefix not in crossed[src][dst]:
                        crossed[src][dst][prefix]=set()
                    ccdata=set(ccdata) # remove duplicates
                    if mode=="sets":                           
                        crossed[src][dst][prefix].update(ccdata)                    
                        #print crossed[prefix]
                        continue
                    else: # mode == "path"
                        ccdata=list(ccdata)                  
                        ccdata.sort()
                        crossed[src][dst][prefix].update([tuple(ccdata)])
                        #print "added",src,dst,prefix,ccdata
                        #print crossed[prefix]          
    
#        if count>1000000:
#            data=[]
#        else: 
#            data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines
    fileobject.close()    
    return crossed,cc_to_asn

def write_crossed_to_disk(crossed,mode):
    filename="crossed-"+mode+".pkl"
    print "\nWriting crossed dictionary representation to file:",filename 
    fileobject=open(filename,'w')
    keys=crossed.keys()
    keys.sort()
    for key in keys:
        print key,
        pickle.dump(key,fileobject,2)
        pickle.dump(crossed[key],fileobject,2)  
    fileobject.close()

def experiment1(targetcc,ccset,crossed,trials=500,mode="path",verbose=True,todisk=True):
    filename="figure-results"
    fileobject=open(filename,'w')
    output="sourcecc nexcluded ngood nbad nmixed goodratio badratio definedratio mixedratio \n"
    fileobject.write(output)
    
    assert mode=="path"
    auclist=[]
    for sourcecc in targetcc: # perform experiment individually on each country
        if verbose:
            print "Evaluating",sourcecc
        exclusionset=set(list(ccset)[:])
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
                dstcc=choice(crossed[sourcecc].keys())
                dstprefix=choice(crossed[sourcecc][dstcc].keys())
                revprefix=choice(crossed[dstcc][sourcecc].keys())
                
                # Check forward paths                
                badp=0
                goodp=0
                for path in crossed[sourcecc][dstcc][dstprefix]:
                    for excludedcc in excluded:
                        if excludedcc in path:
                            badp=badp+1
                            break
                    else:
                        goodp=goodp+1
                
                # Check backwards paths                
                for path in crossed[dstcc][sourcecc][revprefix]:
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
#                    print "  ",sourcecc,dstcc,goodp,badp
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
                print "%s %d: (%d,%d,%d) def=%.2f mix=%.2f" % (sourcecc,nexcluded,g,b,m,defratio,mixratio)       

            output=sourcecc+" "+str(nexcluded)+" "+str(g)+" "+str(b)+" "+str(m)+" "+str(goodratio)+" "+str(badratio)+" "+str(defratio)+" "+str(mixratio)+"\n"
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
            print pair[0],pair[1]
    fileobject.write(output)
    fileobject.close()
    
# BEGIN MAIN PROCEDURE ************************************************

filename='asn_to_cc.pkl'
fileobject=open(filename,'r')
asn_to_cc=pickle.load(fileobject)
fileobject.close()
ccset=set(asn_to_cc.values()) # Set of all observed country codes

mode="paths"

# These are the country codes that had at least 1 router reporting BGP data and that had
# over 100,000 destination prefixes (generally countries had less than 8000 or more than 400,000)
# We only test paths between these countries so that we can model both forward and backwards routes
targetcc=['AT', 'AU', 'BR', 'CA', 'CH', 'CZ', 'DE', 'ES', 'FR', 'GB', 'HK', 'IE', 'IT', 'JP', 'KH', 'MU', 'NL', 'NO', 'RU', 'SE', 'SG', 'UA', 'US', 'ZA']
#targetcc=['FR','RU']
print "Target cc codes=",targetcc

print "Generating Crossed"
crossed=None # Clear memory from past run
cc_to_asn=None
crossed,cc_to_asn=getccpaths(mode,targetcc)
#write_crossed_to_disk(crossed,mode) # Write out results to a file

# This generate the data for the figures (x-axis number of excluded countries, y-axis
# represents ratios: % good, % bad, % we can give a definitive answer)
# It also calculates the AUC for the definitive answer for each country
experiment1(targetcc,ccset,crossed)