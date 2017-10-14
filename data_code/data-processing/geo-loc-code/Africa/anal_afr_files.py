from os import listdir


AFR_Codes = ['AO','BJ','CV','KM','ER','LY','DZ','BW','BF','BI','CM','CF','TD','CG','CD','CI','DJ','EG','GQ','ET','GA','GM','GH','GN','GW','KE','LS','LR','MG','MW','ML','MR','MU','MA','MZ','NA','NE','NG','RW','SN','SL','SO','SS','SD','SZ','TG','TN','UG','EH','ZA','ZM','ZW','YT','ST','RE','SC','SH','TZ','EH']

EUR_Codes = ['GG','JE', 'AL','AD','AT','BY','BE','BA','BG','HR','CY','CZ','DK','EE','FO','FI','FR','DE','GI','GR','HU','IS','IE','IT','LV','LI','LT','LU','MK','MT','MD','MC','NL','NO','PL','PT','RO','RU','SM','RS','SK','SI','ES','SE','CH','UA','GB','VA','RS','IM','RS','ME', 'AX','EU']

EU_Codes = ['GG','JE','EU','BE','BG','CZ','DK','DE','EE','IE','EL','ES','FR','HR','IT','CY','LV','LT','LU','HU','MT','NL','AT','PL','PT','RO','SI','SK','FI','SE','UK','AX']

NAM_Codes = ['AI','AG','AW','BS','BB','BZ','BM','VG','CA','KY','CR','CU','CW','DM','DO','SV','GL','GD','GP','GT','HT','HN','JM','MQ','MX','PM','MS','CW','KN','NI','PA','PR','KN','LC','PM','VC','TT','TC','VI','US','SX','BQ','SA','SE','MF']

SAM_Codes = ['AR','BO','BR','CL','CO','EC','FK','GF','GY','GY','PY','PE','SR','UY','VE']

ASI_Codes = ['AF','AM','AZ','BH','BD','BT','BN','KH','CN','CX','CC','IO','GE','HK','IN','ID','IR','IQ','IL','JP','JO','KZ','KP','KR','KW','KG','LA','LB','MO','MY','MV','MN','MM','NP','OM','PK','PH','QA','SA','SG','LK','SY','TW','TJ','TH','TR','TM','AE','UZ','VN','YE','PS','AP']

AUS_Codes = ['AS','AU','NZ','CK','FJ','PF','GU','KI','MP','MH','FM','UM','NR','NC','NZ','NU','NF','PW','PG','MP','SB','TK','TO','TV','VU','UM','WF','WS','TL']

ANT_Codes = ['AQ']

AIR_Codes = ['A1', 'A2']


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
        return '???'
        #sys.exit('Error!  Unknown country code')


path='africa-files/'

years=[2015,2016]

for year in years:
    fcode='.'+str(year)
    outfilename='all'+fcode+'.traces.txt'
    outfile=open(outfilename,'w')
    files=[f for f in listdir(path) if fcode in f]
    for file in files:
        with open(path+file,'r') as fileobject:
            lines=fileobject.readlines()
            for line in lines:
                line=line.strip('\n')
                linedata=line.split('|')
                linedata=linedata[:-1] 
                if linedata[-1] not in AFR_Codes:
                    continue
                
                boomerang=[]
                for cc in linedata:
                   continent=get_cont_code(cc)
                   if continent!='AFR':
                       boomerang.append(continent)

                outline=line+'\t||\t'+str(len(boomerang))+'\t||\t'

                for cc in boomerang:
                    outline+=cc+'|'
                
                outline+='\n'
                outfile.write("%s" % outline)
    
    outfile.close()
                



