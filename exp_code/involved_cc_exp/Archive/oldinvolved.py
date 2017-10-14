# This code is for importing list(s) of AS paths and converting them into
# country code (cc) paths.

import pickle
import numpy as np
import matplotlib.pyplot as plt

EU_cc= ['BE','BG','CZ','DK','DE','EE','IE','EL','ES','FR','HR','IT','CY','LV','LT','LU','HU','MT','NL','AT','PL','PT','RO','SI','SK','FI','SE','GB','UK']

def import_monitors(filename,thresh=1000):
    fileobject=open(filename,'r')
    linecount=0  
    count={}
    monitors=[]
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            linecount+=1
            if linecount % 1000000==0:
                print ".",
                if linecount % 20000000==0:
                    print " ",linecount          
            linedata=line.split('|')
            cclist=cleanline(linedata)
            if len(cclist)<1:
                continue
            src=cclist[0]
            if src not in monitors:
                monitors.append(src)
            if src not in count:
                count[src]=0
            count[src]+=1
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines    
    fileobject.close()    
    tmp=monitors[:]
    for mon in tmp:
        if count[mon]<thresh:
            monitors.remove(mon)
    monitors.sort()
    return monitors

def cleanline(linedata):
    linedata=linedata[0:-1] # strip off monitor name 
    cleaned=[]
    prior=0
    for cc in linedata:
        if cc=='U' or cc=='??' or cc=='A1': # A1 is anonymous proxy
            cleaned=[]
            break
        if cc not in cc2name and cc!='AP' and cc!='A2': # approved ISO codes, AP: Asia/Pacific, A2: space
            print cc, 
            cleaned=[]
            break
        if cc in EU_cc:
            cc='EU'
        if cc!=prior:
            cleaned.append(cc)
        prior=cc
    return cleaned
    
def import_involved(filename,src):
    fileobject=open(filename,'r')
    linecount=0  
    involved={}
    dmin={}
    dmean={}
    history={}
    count={}
    batchsize=40*5000000 # 40 chars per line, 5 million lines
    data=fileobject.readlines(batchsize)
    while data!=[]: # and count<10000:
        for line in data:
            linecount+=1
            if linecount % 1000000==0:
                print ".",
                if linecount % 20000000==0:
                    print " ",linecount          
            linedata=line.split('|')
            cclist=cleanline(linedata)
            if len(cclist)<1 or cclist[0]!=src:
                continue
            dst=cclist[-1]
            ccset=set(cclist)
            ccset.remove(src)
                
            if dst not in involved:
                involved[dst]=set()
                history[dst]=[]
                dmin[dst]=len(ccset)
                dmean[dst]=0
                count[dst]=0
            if ccset not in history[dst]: 
                history[dst].append(ccset)
            else: # don't process if we've already seen it
                continue

            #if src==dst: print ccset

            involved[dst].update(ccset)
            if dmin[dst]>len(ccset):
                dmin[dst]=len(ccset)
            dmean[dst]+=len(ccset) # subtract out src and monitor
            count[dst]+=1 # counts number of data items
        #if count>500000:
        #    data=[]
        #else: 
        #    data=fileobject.readlines(batchsize) # get next batch of lines
        data=fileobject.readlines(batchsize) # get next batch of lines    
    fileobject.close()    
    for cc in dmean.keys():
        dmean[cc]=dmean[cc]*1.0/count[cc]
        dmean[cc]=round(dmean[cc],1) # round to tenths digit
    return involved,dmin,dmean

# BEGIN MAIN PROCEDURE ************************************************

def plot_involved(src,involved,xvalues,xlabel):
    ymean={}
    count={}
    ymax=0
    for cc in involved.keys():
        xvalue=xvalues[cc]
        yvalue=len(involved[cc])
        #if yvalue==1 and xvalue==1:
        #    print 1,1,cc,cc2name[cc]
        if ymax<yvalue:
            ymax=yvalue
        #print xvalue,yvalue
        plt.scatter(xvalue,yvalue)
        xvalue=round(xvalue)
        if xvalue not in ymean:
            ymean[xvalue]=0
            count[xvalue]=0
        ymean[xvalue]+=yvalue
        count[xvalue]+=1

    xvalues=ymean.keys()
    xvalues=sorted(xvalues)
    yvalues=[]
    for xvalue in xvalues:
        ymean[xvalue]=ymean[xvalue]*1.0/count[xvalue]
        yvalues.append(round(ymean[xvalue]))
    plt.plot(xvalues,yvalues)
    print "xvalues",[int(x) for x in xvalues]
    print "meanvalues",[int(y) for y in yvalues]
    
    # Plot number of countries at each x-value
    yvalues=[]
    for xvalue in xvalues:
        yvalues.append(count[xvalue])
    plt.plot(xvalues,yvalues)
    print "ncountries at each x",yvalues,"sum=",len(involved.keys()),"/",len(cc2name.keys())-len(EU_cc)+1
        
    plt.ylabel('Involved Countries')
    plt.xlabel(xlabel)
    plt.title(cc2name[src]+" ("+src+")")
    plt.axis([0,max(count.keys()),0,ymax+10])    
    plt.show()  
    
#*********************************************************************
    
filename='../datafiles/cc_to_name.pkl'
fileobject=open(filename,'r')
cc2name=pickle.load(fileobject)
fileobject.close()

filename="../datafiles/data-Geolocation/yearlyGeoFilesNoMon/2016.geodata.nomon.txt"
#filename="../datafiles/data-Geolocation/yearlyGeoFiles/2015.geodata.txt"
#filename="../datafiles/data-Geolocation/monthlyGeoFilesNoMon/2015.01.geodata.nomon.txt"

monitors=import_monitors(filename)
print "monitors=",monitors, len(monitors)
print

monitors=['US']
for target in monitors:
    assert target in monitors
    involved,dmin,dmean=import_involved(filename,target)
    #print len(involved.keys())
    #print dmin
    
    plot_involved(target,involved,dmin,'Min Country Distance')
    plot_involved(target,involved,dmean,'Mean Country Distance')