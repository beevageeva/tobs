from math import tan, sin, asin, pi, atan,cos


def galCoord(alphaHourFormat, deltaDeg):
	a1 = pi * (192.0 / 180 + 25.0 / 60) - alphaHourFormat[0] / 24 - alphaHourFormat[1] / (24 * 60) - alphaHourFormat[2] / (24 * 3600)
	a2 = (27.0 / 180.0  + 4.0 / 60.0)* pi 
	l = 303.0/180.0 * pi - atan(sin(a1) / (cos(a1) * sin(a2) - tan(deltaDeg * pi / 180.0) * cos(a2)))
	return l

print(galCoord([13,42,11],28)) #M33
#print(galCoord([13,42,11],28)) #NGC7006
