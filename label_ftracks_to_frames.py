#!/usr/bin/env python3
import subprocess
import json
import numpy as np 
import cv2
import os		

clips = os.listdir('./Video_Splits')
for clip in clips :
	if(clip.startswith('.')) :
		continue
	filename = clip.split('.mp4')[0]
	if not os.path.isfile("./Keypoints_bboxes/{}.json".format(filename)) :
			continue
	with open("./Keypoints_bboxes_labels/{}.json".format(filename)) as f :
		ftracks = json.load(f)
		for frame in ftracks :
			detections = ftracks.get(frame)
			img_file = frame + '.jpg'
			image = cv2.imread("./Video_frames_3/{}/{}".format(filename, img_file))
			for detection in detections :
				x, y, w, h, character = detection["x"], detection["y"], detection["w"], detection["h"], detection["character"]
				cv2.rectangle(image, (int(x),int(y)), (int(x+w), int(y+h)), (255,0,0), 3)
				cv2.putText(image, character, (int(x) , int(y-10)),  cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
			cv2.imwrite("./Video_frames_full/{}/{}".format(filename, img_file), image)