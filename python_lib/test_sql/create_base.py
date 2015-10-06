#!/usr/bin/python

import json
import sqlite3

debug = 0

conn = sqlite3.connect('scan.sql')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS aps')
c.execute('DROP TABLE IF EXISTS sky')
c.execute('DROP TABLE IF EXISTS points')
c.execute('DROP VIEW IF EXISTS maximum')

c.execute('CREATE TABLE aps (ap_id INTEGER PRIMARY KEY, bssid TEXT(17), essid TEXT(32))')
c.execute('CREATE TABLE sky (point_id INTEGER, ap_id INTEGER, sig INTEGER, PRIMARY KEY (point_id, ap_id))')
c.execute('CREATE TABLE points (point_id INTEGER PRIMARY KEY, az INTEGER, el INTEGER)')
c.execute('''CREATE VIEW maximum AS SELECT aps.essid AS essid, aps.bssid AS bssid, 
		CAST(ROUND(AVG(points.az)) AS INTEGER) AS az, 
		CAST(ROUND(AVG(points.el)) AS INTEGER) AS el, 
		CAST(ROUND(AVG(sky.sig)) AS INTEGER) AS sig 
		FROM sky, aps, points WHERE sky.ap_id = aps.ap_id AND 
		sky.point_id=points.point_id AND 
		sky.sig = (SELECT MAX(sub_sky.sig) FROM sky AS sub_sky 
		WHERE sub_sky.ap_id = sky.ap_id) GROUP BY sky.ap_id''')

conn.commit()

with open('sky_censored.json', 'rt') as fp:
	j = json.load(fp)

# Populating tables sky, points and aps
sky = j['sky']
for az in sky.keys():
	sky_az = sky[az]
	az = int(az)
	for el in sky_az.keys():
		sky_az_el = sky_az[el]
		el = int(el)
		for ap in sky_az_el.keys():
			val = int(round(sky_az_el[ap]))
			# Convert recieved power from "parrots" to dBm
			if (val > 64):
				val -= 256
			# Are we know this AP?
			c.execute('SELECT ap_id FROM aps WHERE bssid=?', (ap,))
			dumb = c.fetchone()
			if ((dumb is not None) and (len(dumb) > 0)):
				# Yes!
				ap_id = dumb[0]
			else:
				# No!
				c.execute('INSERT INTO aps (bssid) VALUES (?)', (ap,))
				# But now, we know it
				ap_id = c.lastrowid
			if (debug > 0):
				print("AP={:17s} ap_id={:2d}".format(ap, ap_id))
			# Are we know this point?
			c.execute('SELECT point_id FROM points WHERE az=? AND el=?', (az, el))
			dumb = c.fetchone()
			if ((dumb is not None) and (len(dumb) > 0)):
				# Yes!
				point_id = dumb[0]
			else:
				# No!
				c.execute('INSERT INTO points (az, el) VALUES (?, ?)', (az, el))
				# But now, we know it
				point_id = c.lastrowid
			if (debug > 0):
				print("AZ={:3d} EL={:3d}, point_id={:3d}".format(az, el, point_id))
			# Key operation: adding point to main table
			c.execute('INSERT INTO sky (point_id, ap_id, sig) VALUES (?, ?, ?)', \
					(point_id, ap_id, val))
			if (debug > 0):
				print("AZ = {:3d} EL = {:3d} AP = {:17s} VAL = {:4d}".\
						format(az, el, ap, val))

conn.commit()

# Updating table aps.
# We don't populate is before than sky, because this scenario excludes from testing
# our pretty 'INSERT INTO aps' statement
ap_names = j['ap_names']
for bssid in ap_names.keys():
	c.execute('UPDATE aps SET essid=? WHERE bssid=?', (ap_names[bssid], bssid))

conn.commit()

# Getting the results.
# Yes, we use conn.execute instead of c.execute, because the first one is iterable
for it in conn.execute('SELECT * FROM maximum'):
	print(it)

conn.close()
