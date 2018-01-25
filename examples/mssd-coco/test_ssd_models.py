#!/usr/bin/python
from __future__ import print_function
'''
./build/tools/caffe train \
--solver="examples/mssd-coco/test_solver.prototxt" \
--weights="examples/mssd-coco/models/MobileNet_SSD_320x320_COCOVOC_msra_iter_190000.caffemodel" \
-gpu 0 
'''
import shlex
import os.path
import sys

log_file = 'examples/mssd-coco/test_ssd_models.log'
use_coco_scale = False

cmd_str = "./build/tools/caffe train \
--solver=\"examples/{}/test_solver.prototxt\" \
-gpu 0 \
--weights=\"<place_holder>\" \
".format('mssd-coco' if use_coco_scale else 'mssd')

cmd = shlex.split(cmd_str)
import subprocess
try:
	import re2 as re
except ImportError:
	import re

def GetTestCaffeModels():
	return ['examples/mssd/MobileNet_SSD_320x320_VOC_iter_160000.caffemodel']
	#import glob
	#model_file_list = sorted(glob.glob("examples/mssd-coco/models/*COCOVOC*caffemodel"))
	test_model_list = re.split(
						r'\n|\r\n',
						subprocess.check_output(
							'ls examples/mssd-coco/models/*_COCO_iter_*caffemodel | sort -V',  # stage 1: trained on COCO
							#'ls examples/mssd-coco/models/*COCOVOC*caffemodel | sort -V',  # mixed COCOVOC data
							shell=True
						)
					  )
	test_model_list += re.split(
						r'\n|\r\n',
						subprocess.check_output(
							'ls examples/mssd-coco/models/*_COCOSCALE_iter*caffemodel | sort -V',  # fine-tuned on VOC 
							#'ls examples/mssd-coco/models/*COCOVOC*caffemodel | sort -V',  # mixed COCOVOC data
							shell=True
						)
					  )	

	# for mf in model_file_list:
		# m = re.search(r'_iter_(\d+)', mf)
		# if not m:	continue
		# iter = int(m.group(1))
		# if iter < 190000:	continue
	return test_model_list

def ExtractSsdDetectionResult(test_out):
	re_person = re.compile(r'\s+class15:\s+([\d\.]+)')
	re_mAP = re.compile(r'\s+detection_eval\s+=\s+([\d\.]+)')
	cnt = 0
	for line in test_out:
		m = re_person.search(line)
		if m:
			person_ap = float(m.group(1))
			cnt += 1
			if cnt >= 2:	break
		else:
			m = re_mAP.search(line)
			if m:
				mAP = float(m.group(1))
				cnt += 1
				if cnt >= 2:	break
	if cnt >= 2:
		return (person_ap, mAP)
	else:
		return (None, None)

try:
	with open(log_file, 'w') as logout:
		for mf in GetTestCaffeModels():
			if not os.path.isfile(mf): continue

			print(mf+': ', end=''); sys.stdout.flush()

			#  do not use '--weights=\"{}\"'
			cmd[-1] = '--weights={}'.format(mf) # os.path.abspath(mf)
			try:
				# PROBLEM: will be printed to STDOUT
				#test_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
				#
				proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				out, err = proc.communicate() # proc.returncode
				# proc.wait()  # stuck here, due to stdout and stdin point to th same thing??
				# out = proc.stdout.read()
				# err = proc.stderr.read()

				person_ap, mAP = ExtractSsdDetectionResult( re.split(r'\n|\r\n',out + err) )
				if person_ap is None or mAP is None:
					print('No detection results found')
				else:
					print('{:.3f} {:.3f}'.format(person_ap, mAP))

				print(out, file=logout)
				print(err, file=logout)

			except subprocess.CalledProcessError as e:
				print('ERROR: returns error code {}'.format(e.returncode))
except IOError:
	print('FAILED to open ' + log_file)


