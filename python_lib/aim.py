import json
from optparse import OptionParser
from turret import MyTurret

parser = OptionParser(description="Program for aiming wifi-turet at AP)")

parser.add_option("-p", "--port",dest="tty",default="/dev/ttyUSB0",
		help="Serial port of connected Arduino servo controller (default: /dev/ttyUSB0)", metavar='tty')
parser.add_option("-v", "--verbose",action="store_true",
		help="Increse verbosity")
parser.add_option("-f", "--file",dest="file", default="data.json",
		help="Read json file of results (default: data.json)")

(options, args) = parser.parse_args()

with open(options.file) as data_file:    
	data = json.load(data_file)
turret=MyTurret(options.tty)

maximum=data['maximum']
#print maximum
ap=args[0].upper()
if ap in maximum:
	if options.verbose: print "Aiming at point: X=" + str(maximum[ap]['x'])+" Y="+str(maximum[ap]['y'])
	turret.aim(maximum[ap])
else: 
	print "Unknown AP in file "+options.file

