import os
import pickle
record_monitors=False

inputfiles=os.listdir('dailyGeoFiles')
for record_monitors in [False,True]:
    for year in [2015,2016]:
        # Get list of .warts input files
        yearfiles=[]
        for filename in inputfiles:
            if '.warts' in filename and '.'+str(year) in filename:
                yearfiles.append(filename)
        print("\nProcessing",len(yearfiles),"input files from",year)
        
        ccpaths={}
        count=0
        mismatch=0
        linecount=0
        for filename in yearfiles:
            count=count+1
            if count % 1000==0: 
                print(".") 
                if count % 10000==0:
                    print(" ",count)       
            filepath='dailyGeoFiles/'
            fileobject=open(filepath+filename,'r')
            namefields=filename.split('.')
            monitor=namefields[5]
            monitorcc=monitor.split('-')[1].upper()        
            lines=fileobject.readlines()
            for line in lines:


                line=line.strip('\n')
                linedata=line.split('|')
                if len(linedata)==2:
                    linedata.insert(1,linedata[0])

                #linedata=line.split('|')
                #linedata=linedata[:-1] # remove newline

                if len(linedata)==2: #This is the case where the src=dst
                    linedata.insert(1,linedata[0])  
                    
                if len(linedata)<2:
                    mismatch+=1
                    continue                  
                
                if linedata[0]=='??':
                    #status=False
                    #if linedata[1]!=monitorcc:
                    #    print monitorcc,linedata," ",
                    #    status=True
                    
                    #print linedata
                    linedata[0]=monitorcc # replace ?? with monitor cc
                    marker=0            
                    for x in range(1,len(linedata)-1):            
                        if linedata[x]==monitorcc:
                            marker=x
                        else:
                            break
                    if marker>0:
                        linedata=linedata[marker:]
                    #if status==True:
                    #    print linedata
                    #print linedata,"\n"
    
                if linedata[0]!=monitorcc:
                    mismatch+=1
                    linedata[0]=monitorcc
                    #print linedata,monitorcc
                    continue
                
                linecount+=1
                if record_monitors==True:
                    linedata.append(monitor)
                else:
                    linedata.append('0')
                if tuple(linedata) not in ccpaths:
                    ccpaths[tuple(linedata)]=1
                else:
                    ccpaths[tuple(linedata)]+=1
                #print linedata
                #print(linecount,mismatch)
            fileobject.close()
            #if count>100: break
            
        print("\nWriting processed data for year",year)
        print("Number of distinct paths=",len(ccpaths.keys()))
        print("Number of path instances=",linecount)
        if record_monitors==True:
            monstatus=''
            filepath='yearlyGeoFiles/'
        else:
            monstatus='.nomon'
            filepath='yearlyGeoFilesNoMon/'        
#        filename=filepath+str(year)+'.Geodata'+monstatus+'.pkl'
#        print filename
#        output=open(filename,'wb')
#        pickle.dump(ccpaths,output)
#        output.close()
    
        filename=filepath+str(year)+'.Geodata'+monstatus+'.txt'
        print(filename)
        output=open(filename,'w')
        for path in ccpaths:
            line=""
            for elem in path:
                line=line+elem+'|'
            line=line+str(ccpaths[path])
            output.write(line+'\r\n')
        output.close()
