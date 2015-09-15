from pythonwifi import iwlibs


iface=iwlibs.Wireless('wlan0')

#print dir (iface)
scanresults=iface.scan()

for i in scanresults:
	print i.bssid+"   "+str(i.quality.siglevel-256)
#	print dir(i.range)
