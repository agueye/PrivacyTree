import csv

years=[2015,2016]

for year in years:
    fileobject=open(str(year)+".involved_data.pkl",'rb')
    data = pickle.load(fileobject)
    fileobject.close()

    #print(data)

    all_dest = []
    for item in data:
        ###print(data[item])
        dests= data[item].keys()
        all_dest+=dests

    all_dest = list(set(all_dest))
    all_dest.sort()

    dest_mat=[]
    first_row=[' ']+all_dest
    dest_mat.append(first_row)

    for item in data:
        tmp=[item]
        dests= data[item].keys()
        for dest in all_dest:
            if dest not in dests:
                tmp.append(-1)
            else:
                tmp.append(data[item][dest])

        dest_mat.append(tmp)

    #print(dest_mat)
    res_file = str(year)+".involved_data.csv"
    with open(res_file,'w') as f:
        writer=csv.writer(f)
        writer.writerows(dest_mat)
    
