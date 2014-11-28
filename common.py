from math import pi

def hourToRad(h,m,s):
	return  (h+m/60.0+s/3600.0)* pi/ 12.0

def degToRad(d,m,s):
	return  (d+m/60.0+s/3600.0)* pi/ 180.0

