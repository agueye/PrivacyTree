import pickle

def active_monitors(src_cc,threshold):  #Monitors that appear a number of times above the threshold.
    filename='../datafiles/ccmap-sets.txt'
    fileobject=open(filename,'r')
    count=0  
    monmap={}
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
            src=linedata[0]
            if src != src_cc:
                continue
            mon=linedata[-1]
            mon=mon.strip()
            if mon not in monmap:
                monmap[mon]=0
            monmap[mon]=monmap[mon]+1                     
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines    
    fileobject.close()    
    active=[]
    for mon in monmap.keys():
        if monmap[mon]>threshold:
            active.append(mon)
            #print "ACTIVE:",mon,monmap[mon]
    return active   

def generalization_result(src_cc,monitors):
    filename='../datafiles/ccmap-sets.txt'
    fileobject=open(filename,'r')
    count=0  
    paths=0
    thrownout=0
    set1=set()
    set2=set()
    monmap={}
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
            src=linedata[0]
            if src != src_cc:
                continue
            mon=linedata[-1]
            mon=mon.strip()
            if mon not in monitors:
                continue
            if mon not in monmap:
                monmap[mon]=0
            monmap[mon]=monmap[mon]+1
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
            dst=cclist[-1]
            ccset=set(cclist)
            ccset.remove(src)
            if dst in ccset:
                ccset.remove(dst)
            cclist=list(ccset)
            cclist.sort()
            cclist.append(dst)
            #print
            cctuple=tuple(cclist)
            if cctuple not in set1:
                set1.add(cctuple)
            elif cctuple not in set2:
                set2.add(cctuple)
            paths=paths+1                            
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines    
    fileobject.close()    
    failures=len(set1)-len(set2)
    return paths,failures

def generalization_result2(src_cc,monitors):
    filename='../datafiles/ccmap-sets.txt'
    fileobject=open(filename,'r')
    count=0  
    paths=0
    thrownout=0
    set1=set()
    set2=set()
    monmap={}
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
            src=linedata[0]
            if src != src_cc:
                continue
            mon=linedata[-1]
            mon=mon.strip()
            if mon not in monitors:
                continue
            if mon not in monmap:
                monmap[mon]=set()
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
            dst=cclist[-1]
            ccset=set(cclist)
            ccset.remove(src)
            if dst in ccset:
                ccset.remove(dst)
            cclist=list(ccset)
            cclist.sort()
            cclist.append(dst)
            #print
            cctuple=tuple(cclist)
            if cctuple not in set1:
                set1.add(cctuple)
            elif cctuple not in set2:
                set2.add(cctuple)
            monmap[mon].add(cctuple)
            paths=paths+1                            
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines    
    fileobject.close()    
    failures=len(set1)-len(set2)
    
    for mon in monitors:
        fail=0
        for cctuple in monmap[mon]:
            if cctuple not in set2:
                fail=fail+1
        total=len(monmap[mon])
        ratio=(total-fail)*1.0/total
        print "%s %d %.02f" % (mon,len(monmap[mon]),ratio)
    return paths,failures

# BEGIN MAIN PROCEDURE ************************************************

filename='../datafiles/cc_to_mon.pkl'
fileobject=open(filename,'r')
cc2mon=pickle.load(fileobject)  #All monitors in a country
fileobject.close()

filename='../datafiles/cc_to_name.pkl'
fileobject=open(filename,'r')
cc2name=pickle.load(fileobject)   #Country name
fileobject.close()

fileobject=open("../resultfiles/generalization-results",'w')
ccodes=cc2mon.keys()
ccodes.sort() #All country codes
for cc in ccodes:
    monitors=active_monitors(cc,100)
    if len(monitors)<2:
        continue
    paths,failures=generalization_result(cc,monitors) 
    if paths==0:
        continue
    print cc2name[cc],cc,len(monitors),(paths-failures)*1.0/paths
    outputstring=cc+" "+str(len(monitors))+" "+str((paths-failures)*1.0/paths)+"\r\n"
    fileobject.write(outputstring)
fileobject.close()
