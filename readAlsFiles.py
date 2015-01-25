from configLocal import OUTPUTDIR, FILTERS
import os.path 

prefFile = "RESOBJ"
prefMark = "RESMARK"


R = 1.0  #For M37
#R = 6.0 #FOR standard
import getopt,sys, re
try:
				opts, args = getopt.getopt(sys.argv[1:], "", ["listFiles=", "markNumber=", "standard"])
except getopt.GetoptError as err:
				# print help information and exit:
				print("Error in parsing args")
				print(str(err)) # will print something like "option -a not recognized"
				sys.exit(2)
#print("OPTIONS")
#print(opts)
#print("OPTIONS END")
listFiles = None
for o, a in opts:
				#print("o is now >%s<" % o)
				if o == "--listFiles":
								listFiles = a
				if o == "--standard":
								print("STANDARD FLAG Using R = 6")
								R = 6
				else:
								print("option %s not recognized " % o)

sind = listFiles.rindex('-') 
if(sind!=-1):
	objName = "ALSREAD-" + listFiles[sind+1:]
else:
	objName = "ALSREAD-GENERIC"
if not os.path.exists(os.path.join(OUTPUTDIR,objName)):
	os.makedirs(os.path.join(OUTPUTDIR,objName))
else:
	os.system("rm -f %s/*" % os.path.join(OUTPUTDIR,objName))


stars = []
def addToStars(xcenter, ycenter, mag, filename):
	for s in stars:
		for coords in s:
			if (coords[0] - xcenter)**2 + (coords[1] - ycenter)**2 < R**2:
				print("FOUND x=%4.1f y=%4.1f, c[0]=%4.1f, c[1]=%4.1f, diff=%4.1f, " % (xcenter, ycenter, coords[0], coords[1], ( (coords[0] - xcenter)**2 + (coords[1] - ycenter)**2 )))
				s.append([xcenter, ycenter, mag, filename])
				return
	print("ADD x=%4.1f y=%4.1f" % (xcenter, ycenter))
	stars.append([])
	stars[-1].append([xcenter, ycenter, mag, filename])


with open(listFiles) as file1:
	for line in file1:
		fullFilename = line.strip() + ".als"
		print("ALS filename is %s" % fullFilename)	
		with open(fullFilename) as file2:
			prevLine = ""
			for line2 in file2:
				cl2 = line2.strip()
				if not cl2.startswith("#"):
					if cl2.endswith("\\"):
						prevLine = cl2[:-1]
					else:
						cl2 = prevLine + cl2
						values = re.split('\s+',cl2)	
						#print(values)
						xcenter = float(values[1])
						ycenter = float(values[2])
						mag = float(values[3])
						addToStars(xcenter, ycenter, mag, fullFilename[:-4])


stars = sorted(stars, key=lambda s: len(s) * 100 - s[0][2], reverse=True)
print("FIN")
n = 0
for s in stars:
	print("star[%d]" % n)
	for coords in s:
		print(coords)	
		fw = os.path.join(OUTPUTDIR,objName, "%s_%d" % (prefFile, n))	
		os.system("echo '%4.1f %4.1f %4.1f %s' >> %s" % (coords[0], coords[1], coords[2], coords[3],fw ))	
		mw = os.path.join(os.path.dirname(coords[3]), "%s_%s" % (prefMark,os.path.basename(coords[3]) ))
		os.system("echo '%4.1f %4.1f %d' >> %s" % (coords[0], coords[1], n , mw))
	n+=1





