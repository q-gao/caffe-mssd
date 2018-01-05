from __future__ import print_function

import sys
import re
#import numpy as np

lt = []
prev_t = None
for line in sys.stdin:
	m = re.search(r'Iteration (\d+),\s*loss\s*=', line)
	if m:
		a = line.split()
		a = a[1].split(':')
		t = int(a[0])*3600 + int(a[1])*60 + float(a[2]) 
		if prev_t is not None:
			lt.append(t - prev_t)
		prev_t = t

import matplotlib.pyplot as plt
plt.plot(lt)
plt.show()
