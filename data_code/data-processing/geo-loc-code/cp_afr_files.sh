#!/bin/bash

d=africa-files
[ ! -d $d ] && mkdir -v $d

# list from Assane email 2017-09-25
x='acc-gh cmn-ma cmn2-ma coo-bj dar-tz dar2-tz dkr-sn dur-za jnb-za kgl-rw kgl2-rw kgl3-rw krt-sd los-ng mru-mu nbo-ke oua-bf oua2-bf pry-za tnr-mg bjl-gm'
# auto-generate inames arguments:

unset inames; for i in $x; do inames+="-iname '*$i*' -o "; done

#echo "$inames"  # note we have a trailing extra " -o "
#-iname '*acc-gh*' -o -iname '*cmn-ma*' -o -iname '*cmn2-ma*' -o -iname '*coo-bj*' -o -iname '*dar-tz*' -o -iname '*dar2-tz*' -o -iname '*dkr-sn*' -o -iname '*dur-za*' -o -iname '*jnb-za*' -o -iname '*kgl-rw*' -o -iname '*kgl2-rw*' -o -iname '*kgl3-rw*' -o -iname '*krt-sd*' -o -iname '*los-ng*' -o -iname '*mru-mu*' -o -iname '*nbo-ke*' -o -iname '*oua-bf*' -o -iname '*oua2-bf*' -o -iname '*pry-za*' -o -iname '*tnr-mg*' -o -iname '*bjl-gm*' -o

# verify this removes trailer

#echo ${inames% -o }

# remove the extra trailer string from inames to clean it up:

inames=${inames% -o }


eval find dailyGeoFiles -type f "\(" $inames "\)" -exec cp -t $d {} + 
