#!/usr/bin/python
from __future__ import print_function

import re

def ExtractSsdStat( result_file ):
	try:		
		with open(result_file) as fh_in:
			list_iter, list_people_ap, list_mAP = [], [], []
			for line in fh_in:
				m = re.search(r'_iter_(\d+).*:\s+([\d\.]+)\s+([\d\.]+)$', line)
				if m:
					list_iter.append(int(m.group(1)))
					list_people_ap.append(float(m.group(2)))
					list_mAP.append(float(m.group(3)))
			return (list_iter, list_people_ap, list_mAP)
	except IOError:
		print('FAILED to open ' + result_file)
		return (None, None, None)

import sys
list_iter, list_people_ap, list_mAP = ExtractSsdStat(sys.argv[1])

list_iter_corrected = [list_iter[0]]
off = 0
for i in xrange(1, len(list_iter)):
	if list_iter[i] < list_iter[i-1]:
		off += list_iter[i-1]
	if list_iter[i] < list_iter_corrected[i-1]:
		list_iter_corrected.append(list_iter[i] + off)
	else:
		list_iter_corrected.append(list_iter[i])

import matplotlib.pyplot as plt
plt.plot(list_iter_corrected, list_people_ap, 'g', label='People AP')
plt.plot(list_iter_corrected, list_mAP, 'r', label='mAP')
plt.legend()
plt.grid(b=True, which='major')
plt.grid(b=True, which='minor', linestyle=':')
plt.minorticks_on()  # must be called to show minor
plt.show()


