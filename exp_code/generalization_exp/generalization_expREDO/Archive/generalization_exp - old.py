import pickle

def generalization_exp(mode,targetcc,cc_to_asn_only=False,source_cc='',excluded_asn='',verbose=True):
    assert mode=="paths" or mode=="sets"
    filename='20151201_IPV4_with_prefix.all-paths_reduced'
    fileobject=open(filename,'r')
    
    count=0  
    excluded={}
    crossed={} # key is (prefix), value is observed intermediary countries  
    cc_to_asn={}
    batchsize=40*5000000*2 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            count=count+1
            if count % 10000000==0 and verbose:
                print ".",
                #if count % 20000000==0 and verbose:
                #    print " ",count
            
            linedata=line.split('|') 
        
            cclist=[]
            stop=False
            for x in range(len(linedata)-1):
                asn=linedata[x]
                if asn in asn_to_cc:
                    cc=asn_to_cc[asn]
                    if x==0 and cc!=source_cc and cc_to_asn_only==False:
                        stop=True
                        break
                    cclist.append(cc) 
                else:
                    if x==0: # the first ASN is an unknown country
                        stop=True
                        break
            if stop==True:
                continue
            
            dst=cclist[-1]
           
            if cclist[0] in targetcc:
                asn=linedata[0] # AS that reported this path
                if cclist[0] not in cc_to_asn:
                    cc_to_asn[cclist[0]]=set()
                cc_to_asn[cclist[0]].add(asn) # Record each reporting AS for each cc  
            
            if cc_to_asn_only==True:
                continue

            if dst not in targetcc and len(targetcc)>0:
                continue
            
            if cclist[0]!=source_cc: 
                continue
            
            #assert len(set(cclist))==len(cclist)

            prefix=linedata[-1].split()[0] # add prefix but remove ' \r\n' 
            #assert "." in prefix
    
            # Create sublists and remove duplicate paths
            for x in range(len(cclist)-1):
                if cclist[x] in targetcc or len(targetcc)==0:
                    src=cclist[x]
                    #ccodes.add(cclist[x])
                    ccdata=cclist[x+1:] 
                    if prefix not in crossed:
                        crossed[prefix]=set()
                    if prefix not in excluded:
                        excluded[prefix]=set()
                    ccdata=set(ccdata) # remove duplicates
                    if mode=="sets":                           
                        if asn==excluded_asn:
                            excluded[prefix].update(ccdata)                    
                        else:
                            crossed[prefix].update(ccdata)
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
        #data=[]
        
    fileobject.close()  
    if verbose:
        print
    if cc_to_asn_only==True:
        return cc_to_asn
    else:
        return crossed,excluded

# BEGIN MAIN PROCEDURE ************************************************

filename='asn_to_cc.pkl'
fileobject=open(filename,'r')
asn_to_cc=pickle.load(fileobject)
fileobject.close()

# These are the country codes that had at least 1 router reporting BGP data and that had
# over 100,000 destination prefixes (generally countries had less than 8000 or more than 400,000)
# We only test paths between these countries so that we can model both forward and backwards routes
targetcc=['AT', 'AU', 'BR', 'CA', 'CH', 'CZ', 'DE', 'ES', 'FR', 'GB', 'HK', 'IE', 'IT', 'JP', 'KH', 'MU', 'NL', 'NO', 'RU', 'SE', 'SG', 'UA', 'US', 'ZA']
#targetcc=['FR','RU']
print "Target cc codes=",targetcc

fileobject2=open("generalization-results",'w')

#mode="paths"
mode="sets" # only need sets to compare coverage

print "Getting cc to asn map"
# this is a special mode for generalization_exp() that returns a cc to asn mapping
cc_to_asn=generalization_exp('sets',targetcc,True)

ratios={}
ccodes=cc_to_asn.keys()
ccodes.sort()
for cc in ccodes:
    print "Evaluating",cc
    ratios[cc]=0
    if len(cc_to_asn[cc])==1: 
        print "Can't evaluate, only 1 AS available"
        continue
    for asn in cc_to_asn[cc]:
        majority,excluded=generalization_exp('sets',targetcc,False,cc,asn)        
        success=0
        failure=0
        for prefix in excluded.keys():
            if excluded[prefix].issubset(majority[prefix]):
                success=success+1
            else:
                failure=failure+1
        ratio=success*1.0/(success+failure)
        ratios[cc]=ratios[cc]+ratio     
        print "  ",cc,"asn:",asn,
        print "ratio: %.4f" % ratio,
        print "success:",success,"failure:",failure
        
    ratios[cc]=ratios[cc]/len(cc_to_asn[cc]) # divide by number of ASNs evaluated
    ratios[cc]=int(ratios[cc]*10000)*1.0/10000
    print "Mean ratio:",ratios[cc],"Number of ASNs:",len(cc_to_asn[cc]) 
    outputstring=cc+" "+str(ratios[cc])+" "+str(len(cc_to_asn[cc]))+"\n"
    print outputstring
    fileobject2.write(outputstring)
fileobject2.close()