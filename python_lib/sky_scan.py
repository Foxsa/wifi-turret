#!/usr/bin/python
#v0.1

from optparse import OptionParser
import time
import json

import turret
from pythonwifi import iwlibs

def median(lst):
	lst = sorted([x for x in lst if x is not None])
	if (len(lst) < 1):
		return None
	if ((len(lst) % 2) == 1):
		return lst[((len(lst)+1)/2)-1]
	else:
		return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

def uniq(seq):
	return list(set(seq))

##### Options #####
parser = OptionParser(description="Program for scanning sky segment with turret device)")
parser.add_option("-p", "--port",dest="tty",default="/dev/ttyUSB0",
		help="Serial port of connected Arduino servo controller (default: /dev/ttyUSB0)", metavar='tty')
parser.add_option("-i", "--iface",dest="iface",default="wlan0",
		help="Interface that will be used for scanning (default: wlan0)", metavar='iface')
parser.add_option("-v", "--verbose",action="store_true",
		help="Increse verbosity")
parser.add_option("-o", "--output",dest="output",
		help="Write result in json file",metavar="FILE")


##mode: scan find
##starty, finy
##startx, finx
##delta

##### options #####
output="sky_scan.out"
startx=0
finx=180
starty=0
finy=180
delta=60
num_measures=3
measures_sleep=1

### initialization ###
(options, args) = parser.parse_args()
turret=turret.MyTurret(options.tty)
wifi=iwlibs.Wireless(options.iface)

sky={}
all_aps=[]

### X azimut
for curx in range(startx,finx,delta)+[finx]:
	sky[curx]={}
	turret.setx(curx)
	if options.verbose: print 'Set X: '+str(curx)

### Y Elevation
	for cury in range(starty,finy,delta)+[finy]:
		turret.sety(cury)
		if options.verbose: print 'Set Y: '+str(cury)
		sky[curx][cury]={}
		## scan
		scan_results={}
		aps_bssid=[]
		for m in range(0, num_measures):
			scan_results[m]={}
			results=wifi.scan()
			for i in results:
				scan_results[m][i.bssid]=i.quality.siglevel
				aps_bssid.append(i.bssid)
				all_aps.append(i.bssid)
			time.sleep(measures_sleep)
		aps_bssid=uniq(aps_bssid)
	
		### sort and calculate ###
	
		for ap in aps_bssid:
			power=[]
			for m in range(0, num_measures):
				if ap in scan_results[m]:
					power.append(scan_results[m][ap])
			sky[curx][cury][ap]=median(power)
		
all_aps=uniq(all_aps)

maximum={}
for ap in all_aps:
	maximum[ap]={}
	appower=0
	for cx in sky:
		for cy in sky[cx]:
			if ap in sky[cx][cy]: 
				if sky[cx][cy][ap] > appower:
					appower=sky[cx][cy][ap]
					maximum[ap]['x']=cx
					maximum[ap]['y']=cy
					maximum[ap]['level']=sky[cx][cy][ap]
					maximum[ap]['dbm']=sky[cx][cy][ap]-256
if options.verbose or not options.output: print maximum

if options.output:
	data={}
	data['all_aps']=all_aps
	data['sky']=sky
	data['maximum']=maximum
	
	with open(options.output, 'w') as outfile:
		json.dump(data, outfile,sort_keys=True)
