import sys
from pyraf import iraf

def get_head(image):
    s=iraf.imhead(image,long='yes', Stdout=1)
    for i in s:
        print i

get_head(sys.argv[1])
