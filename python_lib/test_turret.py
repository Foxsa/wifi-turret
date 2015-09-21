from turret import MyTurret

opts={'y': 135, 'x': 60, 'power': 172}

turret=MyTurret()
#turret.sety(160)
turret.aim(opts)
y=turret.gety()
print y
