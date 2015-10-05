# wifi-turret


TODO:
- README
- Add security to ap_names (WEP WPA WPA2 WPS)
- Add Pineapple Infusion
- Add controller check to turret lib

BUG:

In [4]: tur.getx()

ValueError                                Traceback (most recent call last)
<ipython-input-4-44318197f59d> in <module>()
tur.getx()

     54                 self.port.write('gx\n')
     55                 out=self.port.readline()
     56                 return int(out)
     57 

ValueError: invalid literal for int() with base 10: 'Controller initialized\r\n'
