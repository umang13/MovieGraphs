#!/usr/bin/env python3
import subprocess
import json
import numpy as np 
import cv2
import os

scenes = os.listdir('/Users/umangsharma/Downloads/MovieGraphs/Video_frames_1')
for scene in scenes :
	print(scene)
	os.mkdir("./Video_frames_pose/{}".format(scene))
	cmd = " build/examples/openpose/openpose.bin --num_gpu 1 --num_gpu_start 2" \
	+ " --image_dir /Users/umangsharma/Downloads/MovieGraphs/Video_frames_1/{}".format(scene) \
	+ " --face --hand --write_images /Users/umangsharma/Downloads/MovieGraphs/Video_frames_pose/{}".format(scene) \
	+ "--display 0"
	subprocess.call(cmd, shell=True)