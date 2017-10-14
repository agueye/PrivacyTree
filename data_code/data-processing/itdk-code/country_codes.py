
AFR_Codes = ['AO','BJ','CV','KM','ER','LY','DZ','BW','BF','BI','CM','CF','TD','CG','CD','CI','DJ','EG','GQ','ET','GA','GM','GH','GN','GW','KE','LS','LR','MG','MW','ML','MR','MU','MA','MZ','NA','NE','NG','RW','SN','SL','SO','SS','SD','SZ','TG','TN','UG','EH','ZA','ZM','ZW','YT','ST','RE','SC','SH','TZ','EH']

EUR_Codes = ['GG','JE', 'AL','AD','AT','BY','BE','BA','BG','HR','CY','CZ','DK','EE','FO','FI','FR','DE','GI','GR','HU','IS','IE','IT','LV','LI','LT','LU','MK','MT','MD','MC','NL','NO','PL','PT','RO','RU','SM','RS','SK','SI','ES','SE','CH','UA','GB','VA','RS','IM','RS','ME', 'AX','EU']

EU_Codes = ['GG','JE','EU','BE','BG','CZ','DK','DE','EE','IE','EL','ES','FR','HR','IT','CY','LV','LT','LU','HU','MT','NL','AT','PL','PT','RO','SI','SK','FI','SE','UK','AX']

NAM_Codes = ['AI','AG','AW','BS','BB','BZ','BM','VG','CA','KY','CR','CU','CW','DM','DO','SV','GL','GD','GP','GT','HT','HN','JM','MQ','MX','PM','MS','CW','KN','NI','PA','PR','KN','LC','PM','VC','TT','TC','VI','US','SX','BQ','SA','SE','MF']

SAM_Codes = ['AR','BO','BR','CL','CO','EC','FK','GF','GY','GY','PY','PE','SR','UY','VE']

ASI_Codes = ['AF','AM','AZ','BH','BD','BT','BN','KH','CN','CX','CC','IO','GE','HK','IN','ID','IR','IQ','IL','JP','JO','KZ','KP','KR','KW','KG','LA','LB','MO','MY','MV','MN','MM','NP','OM','PK','PH','QA','SA','SG','LK','SY','TW','TJ','TH','TR','TM','AE','UZ','VN','YE','PS','AP']

AUS_Codes = ['AS','AU','NZ','CK','FJ','PF','GU','KI','MP','MH','FM','UM','NR','NC','NZ','NU','NF','PW','PG','MP','SB','TK','TO','TV','VU','UM','WF','WS','TL']

ANT_Codes = ['AQ']

AIR_Codes = ['A1', 'A2']

conts = ['AFR','EUR','NAM','SAM','ASI','AUS','ANT','AIR']

#base_dir = '../Data/'

import os

#def write_data(dic,file):
def writeDict(filename,d):
	try:
		if os.path.isfile(filename):
			os.unlink(filename)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
	except Exception as e:
		print(e)


	with open(filename, "a") as f:
		for i in d.keys():   
			f.write(i + "\t" + d[i] + "\n")	
			#f.write(i + "\t" + '\t'.join(d[i]) + "\n")	

def get_cont_codes(base):
    if base == 'AFR':  return AFR_Codes
    elif base == 'EUR':  return EUR_Codes
    elif base == 'EU':  return EU_Codes
    elif base == 'ASI':  return ASI_Codes
    elif base == 'AUS':  return AUS_Codes
    elif base == 'ANT':  return ANT_Codes
    elif base == 'NAM':  return NAM_Codes
    elif base == 'SAM':  return SAM_Codes
    elif base == 'AIR':  return AIR_Codes
    else:
	    return []
    ###sys.exit('Error!  Unknown country code')


def get_cont_code(country):

    if country in  AFR_Codes:
        return 'AFR'
    elif country in  EUR_Codes:
        return 'EUR'
    elif country in  EU_Codes:
        return 'EU'
    elif country in  NAM_Codes:
        return 'NAM'
    elif country in  SAM_Codes:
        return 'SAM'
    elif country in  ASI_Codes:
        return 'ASI'
    elif country in  AUS_Codes:
        return 'AUS'
    elif country in  ANT_Codes:
        return 'ANT'
    elif country in  AIR_Codes:
        return 'AIR'
    else:
        return []
        #sys.exit('Error!  Unknown country code')


def country_latlon_2():
    EUR_nodes = {}
    with open("../Data/Old_data/country_latlon.csv", "r") as f:
        for line in f:
            line =line.rstrip('\n')
            code = line.split(",")[0]
            lat = line.split(",")[1]
            lon = line.split(",")[2]
            cont = get_cont_code(code)
            if cont == 'EUR': EUR_nodes[code] = [lat,lon]
    print(EUR_nodes)
    # Write stats into files by continent
    writeDict('EUR_latlon.txt',EUR_nodes)
    #writeDict('EUR_latlon.txt',EUR_nodes)

def country_latlon():
    AFR_nodes = {}
    ASI_nodes = {}
    NAM_nodes = {}
    SAM_nodes = {}
    EUR_nodes = {}
    EU_nodes = {}
    AUS_nodes = {}
    ANT_nodes = {}
    UNK_nodes = {}

    with open("../Data/Old_data/country_latlon.csv", "r") as f:
        for line in f:
            line =line.rstrip('\n')
            code = line.split(",")[0]
            lat = line.split(",")[1]
            lon = line.split(",")[2]
            cont = get_cont_code(code)
            if cont == 'AFR': AFR_nodes[code] = [lat,lon]
            elif cont == 'EUR': EUR_nodes[code] = [lat,lon]
            elif cont == 'EU':  EU_nodes[code] = [lat,lon]
            elif cont == 'ASI': ASI_nodes[code] = [lat,lon]
            elif cont == 'AUS': AUS_nodes[code] = [lat,lon]
            elif cont == 'ANT': ANT_nodes[code] = [lat,lon]
            elif cont == 'NAM': NAM_nodes[code] = [lat,lon]
            elif cont == 'SAM': SAM_nodes[code] = [lat,lon]
            elif cont == 'AIR': AIR_nodes[code] = [lat,lon]
            

    print(AFR_nodes)
    # Write stats into files by continent
    writeDict('AFR_latlon.txt',AFR_nodes)
    #writeDict('EUR_latlon.txt',EUR_nodes)
    writeDict('EU_latlon.txt',EU_nodes)
    writeDict('ASI_latlon.txt',ASI_nodes)
    writeDict('AUS_latlon.txt',AUS_nodes)
    writeDict('ANT_latlon.txt',ANT_nodes)
    writeDict('SAM_latlon.txt',SAM_nodes)
    writeDict('NAM_latlon.txt',NAM_nodes)
    writeDict('AIR_latlon.txt',UNK_nodes)


def country_stats(filename):
 
    c_stats = {}

    with open(filename, "r") as f:
	    for line in f:
		    tmp = line.split()[1]
		    if c_stats.has_key(tmp):
			    c_stats[tmp] +=1
		    else:
			    c_stats[tmp] =1

    return c_stats   # number of nodes in each country


def cont_nodes(filename):
	
	c_nodes = {}
	
	with open(filename, "r") as f:
		for line in f:
			node = line.split()[0]
			cc = line.split()[1]
			c_nodes[node]=cc
				
	return c_nodes


def generate_ordered_key(ct1,ct2,cc1='',cc2=''):
	
	# Make sure that everything is in the right order....
	c_codes = get_cont_codes(ct1)
	
	if ct1 == ct2:
		if c_codes.index(cc1)<c_codes.index(cc2):
			key = cc1+"_"+cc2
		else:
			key = cc2+"_"+cc1
	else:
		if conts.index(ct1)<conts.index(ct2):
			#print "Different Continent ", "cc1=",cc1," cc2=",cc2
			if is_in_list(cc1,c_codes):
				key = cc1+"_"+cc2
				#print "Different Continent", cc1," in ",ct1
			else:
				key = cc2+"_"+cc1
				#print "Different Continent", cc1," not in ",ct1

		else:
			if is_in_list(cc1,c_codes):
				key = cc2+"_"+cc1
			else:
				key = cc1+"_"+cc2

	return key


def is_in_list(el,lst):
	for e in lst:
		#print "ttesting", e ," and ", el
		if e==el: return True
	return False

# 
def get_links_stats(src,filename):
	
	
	ln = filename.split('_')
	ct1 = ln[0]
	ct2 = ln[1]

	stats = {}
	num_links = 0
	cc_stats = {}
	cc_num_links = 0
	with open(src+filename,"r") as f:
		for line in f:
			line =line.strip('\n')
			line =line.strip()
			line= line.replace(" ", "")
			line = line.split(',')
			cc1 = line[0]
			cc2 = line[1]
			#print "cc1=",cc1," cc2=",cc2
			
			key = generate_ordered_key(ct1,ct2,cc1,cc2)
			if stats.has_key(key):
				stats[key] +=1
			else:
				stats[key] =1
			num_links +=1
			if cc1!=cc2:
				if cc_stats.has_key(key):
					cc_stats[key] +=1
				else:
					cc_stats[key] =1
				cc_num_links +=1

	return stats, num_links #,cc_stats, cc_num_links




def get_marker_sz(c_stats):
    
    tot = sum(c_stats.values())
    step = tot/8
    vals = range(min(c_stats.values()),max(c_stats.values()),step)

    mk_sz ={}

    for k in c_stats.keys():
        inds = [v for v in vals if v<=c_stats[k]]
        mk_sz[k]=5*len(inds)
        
    return mk_sz

############################
#conts = ['AUS','AFR']


#stats = get_links_stats("AFR_AUS_links.txt")
#print stats
#print "Num Afr count", len(AFR_Codes)
#country_stats("AFR.txt")
#country_latlon_2()            
     

