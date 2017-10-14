# Get all the monitors belonging to one country

import pickle

filepaths=[]
#filepaths.append('../Data-ASN')
#filepaths.append('../data-Geolocation')

filepath='../data-Geolocation'

years=[2015, 2016]

for year in years:

    with open(filepath+"/"+str(year)+".files.list.txt",'r') as  fileobject:
        data=fileobject.readlines()
        count=0
        cc2mon={}
        for line in data:
            count=count+1
            if count % 1000000==0:
                print("."),
                if count % 20000000==0:
                    print(" ",count)
            linedata=line.split('.')  
            mon=linedata[-2]
            mon=mon.strip()
            cc=mon.split('-')[1]
            if cc not in cc2mon:
                cc2mon[cc]=set()
            cc2mon[cc].add(mon) 
           
    fileobject2=open(filepath+"/"+str(year)+".cc_to_mon.pkl",'wb')
    pickle.dump(cc2mon,fileobject2)
    fileobject2.close()
