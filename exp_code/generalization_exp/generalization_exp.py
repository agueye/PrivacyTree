import pickle

def active_monitors(src_cc,threshold,dataset,year):
    filename='../../../datafiles/'+dataset+'pre-processed/'+str(year)+'.ccmap-sets.txt'
    fileobject=open(filename,'r')
    count=0  
    monmap={}
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            count=count+1
            if count % 1000000==0:
                print(".")
                if count % 20000000==0:
                    print(" ",count)          
            linedata=line.split('|')
            src=linedata[0]
            #print(src,src_cc)
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

def generalization_result(src_cc,monitors,dataset,year):
    filename='../../../datafiles/'+dataset+'pre-processed/'+str(year)+'.ccmap-sets.txt'
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
                print(".")
                if count % 20000000==0:
                    print(" ",count)          
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
    filename='../datafiles/pre-processed/ccmap-sets.txt'
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
                print(".")
                if count % 20000000==0:
                    print(" ",count)          
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
        print("%d %s %d %.02f" % (year, mon,len(monmap[mon]),ratio))
    return paths,failures

# BEGIN MAIN PROCEDURE ************************************************

filename='../../../datafiles/cc_to_name.pkl'  #Common
fileobject=open(filename,'rb')
cc2name=pickle.load(fileobject, encoding='latin1')
fileobject.close()

dataset="data-Geolocation/"
dataset="data-ASN/"

if dataset=="data-Geolocation/":
    years=[2015, 2016]
    resfile = "Results-Geolocation/generalization/"
elif dataset=="data-ASN/":
    years=[2015]
    resfile = "Results-ASN/generalization/"
else:
    print("Unknown Dataset....exiting")
    exit(1)


for year in years:
    #filename='../datafiles/'+dataset+str(year)+'.cc_to_mon.pkl'   #add year
    filename='../../../datafiles/'+dataset+'pre-processed/'+str(year)+'.mon_to_cc.pkl'  
    fileobject=open(filename,'rb')
    cc2mon=pickle.load(fileobject)
    fileobject.close()
    fname = "../../../resultfiles/"+resfile+str(year)+".generalization-results"
    fileobject=open(fname,'w')  #add year and dataset
    ccodes=list(cc2mon.keys())
    ccodes.sort()
    #print(ccodes)
    for cc in ccodes:
        cc=cc.strip('\n')
        cc=cc.upper()
        monitors=active_monitors(cc,10,dataset,year)
        #print(monitors)
        if len(monitors)<2:
            continue
        paths,failures=generalization_result(cc,monitors,dataset,year) 
        if paths==0:
            continue
        print("Year: ",year,cc2name[cc],cc,len(monitors),(paths-failures)*1.0/paths)
        outputstring=cc+" "+str(len(monitors))+" "+str((paths-failures)*1.0/paths)+"\r\n"
        fileobject.write(outputstring)
    fileobject.close()
