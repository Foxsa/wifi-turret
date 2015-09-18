from pythonwifi import iwlibs


iface=iwlibs.Wireless('wlan0')

#print dir (iface)
scanresults=iface.scan()
a={}

for i in scanresults:
	print i.bssid+"   "+str(i.quality.siglevel-256)
	a[i.bssid] = i.quality.siglevel
#	print dir(i.range)

for bssid,level in a.items():
	print bssid+": "+str(level)
