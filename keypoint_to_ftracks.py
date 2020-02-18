#!/usr/bin/env python3
import subprocess
import json
import numpy as np 
import cv2
import os


confidence_threshold = 0.1
folder_list = os.listdir("./Frame_keypoints_3/")
# os.mkdir("./Keypoints_bboxes/")
for scene_folder in folder_list :
	ftrack = {}
	frame_list = os.listdir("./Frame_keypoints_3/{}".format(scene_folder))
	for frame_file in frame_list :
		with open("./Frame_keypoints_3/{}/{}".format(scene_folder, frame_file)) as f :
			keypoints = json.load(f)
			detections = keypoints.get("people")
			frame_key = (frame_file.split('.json')[0]).split('_keypoints')[0]
			ftrack[frame_key] = []

			for detection in detections :
				face_keypoints = detection.get("face_keypoints_2d")
				max_x = max_y = -1
				min_x = min_y = 10000
				face_keypoints_fmt = [face_keypoints[k:k+3] for k in range(0,len(face_keypoints), 3)]
				min_confidence_flag = False
				for keypoint in face_keypoints_fmt :
					if keypoint[2] < confidence_threshold :
						continue
					min_confidence_flag = True
					if keypoint[0] > max_x :
						max_x = keypoint[0]
					if keypoint[0] < min_x :
						min_x = keypoint[0]
					if keypoint[1] > max_y :
						max_y = keypoint[1]
					if keypoint[1] < min_y :
						min_y = keypoint[1]
				if min_confidence_flag :
					ftrack[frame_key].append({"x":min_x, "y":min_y, "w" : max_x-min_x, "h" : max_y - min_y})
	with open("./Keypoints_bboxes/{}.json".format(scene_folder), 'w') as outfile :
		json.dump(ftrack, outfile)




