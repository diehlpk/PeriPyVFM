from itertools import izip
import sys

print "#x,y,z,u,v,w,a,b,c,d,e,f"
with open(sys.argv[1]) as textfile1, open(sys.argv[2]) as textfile2: 
    for x, y in izip(textfile1, textfile2):
        x = x.strip()
        y = y.strip()
        print x  + y + ",0.000,0.000,0.000,0.000,0.000,0.000"