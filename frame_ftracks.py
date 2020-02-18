#!/usr/bin/env python3
import subprocess
import json
import numpy as np 
import cv2
import os
from shapely.geometry import Polygon

def iou(box_1, box_2) :
	x, y, w, h = box_1["x"], box_1["y"], box_1["w"], box_1["h"]
	box_1 = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]
	x, y,w,h = box_2["x"], box_2["y"], box_2["w"], box_2["h"]
	box_2 = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]
	# print(box_1, box_2)
	poly_1 = Polygon(box_1)
	poly_2 = Polygon(box_2)
	iou = poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
	return iou

res_factor_w = 1920/960
res_factor_h = 796/512
iou_threshold = .32
shot_dict = {}
frame_dict = {}
with open("./mg_videoinfo/scene_boundaries/tt1285016.scenes.gt") as f, open("./mg_videoinfo/video_boundaries/tt1285016.videvents") as g, open("./mg_videoinfo/video_boundaries/tt1285016.matidx") as h:
	for line in h.readlines():
		frame_no, timestamp = line.strip().split(' ')
		frame_dict[int(frame_no)] = float(timestamp)
	next(g)
	shot_count = 0
	# shot_dict[shot_count] = str(0)
	start_frame = 0
	for line in g.readlines():
		frame_no, _, imp = line.strip().split(' ')
		last_frame = int(frame_no) - 1
		shot_count = shot_count + 1
		shot_dict[shot_count] = {"start_time" : float(frame_dict[start_frame]) , "end_time" : float(frame_dict[last_frame]), "start_frame" : start_frame, "end_frame" : last_frame}
		start_frame = int(frame_no)
empty_scenes = []
clips = os.listdir('./Video_Splits')
for clip in clips :
	if(clip.startswith('.')) :
		continue
	filename = clip.split('.mp4')[0]
	scene_num = int((filename.split('.')[0]).split('-')[1])
	start_shot = int((filename.split('.')[1]).split('-')[1])
	end_shot = int((filename.split('.')[2]).split('-')[1])
	# os.mkdir("./Video_frames_3/{}".format(filename))
	print("Working on scene num : {}, with start shot : {} and end shot : {}".format(scene_num, start_shot, end_shot))
	with open("./mg_ftracks/ftrack_ids/tt1285016.json") as f, open("./mg_ftracks/ftracks/tt1285016/{}.json".format(filename)) as g, open("./mg_videoinfo/video_boundaries/tt1285016.videvents") as h:
		id_data = json.load(f)
		ftrack_data = json.load(g)
		if filename not in id_data :
			empty_scenes.append(filename)
			continue

		ids_list = id_data[filename]
		per_frame_list = [[] for frame in ftrack_data['frame2ftracks']]
		global_frame_count = shot_dict.get(start_shot)["start_frame"]
		is_first_frame = [False for frame in ftrack_data['frame2ftracks']]
		while(start_shot <= end_shot) :
			is_first_frame[shot_dict.get(start_shot)["start_frame"] - global_frame_count] = True
			start_shot += 1


		for idx, ftrack in enumerate(ftrack_data['ftracks']) :
			for detection in ftrack :
				x, y, w, h, timestamp, frame = detection["x"], detection["y"], detection["w"], detection["h"], detection["timestamp"], detection["frame"]
				per_frame_list[frame].append({"x":x*res_factor_w, "y":y*res_factor_h,"w":w*res_factor_w,"h":h*res_factor_h, "timestamp":timestamp, "character" : ids_list[idx]})

		# file_list = os.listdir('./Keypoints_bboxes')
		# for filename in file_list :
		# 	if filename.startswith(".") : continue
		# 	filename = filename.split(".json")[0]
		# 	print(filename)

		# frame_list = os.listdir("./Video_frames/{}".format(filename))
		# # os.mkdir("./Video_frames_full/{}".format(filename))
		# for frame_file in frame_list :
		if not os.path.isfile("./Keypoints_bboxes/{}.json".format(filename)) :
			continue
		with open("./Keypoints_bboxes/{}.json".format(filename)) as f :
			ftracks = json.load(f)
			ftracks_labels = {}
			for frame in ftracks :
				frame_no = int(frame.split('frame_')[1])
				img_file = frame + '.jpg'
				detections = ftracks.get(frame)
				orig_detections = [{"x" : per_frame_list[frame_no][i]["x"], "y" : per_frame_list[frame_no][i]["y"], "w" : per_frame_list[frame_no][i]["w"], "h" : per_frame_list[frame_no][i]["h"], "character" : per_frame_list[frame_no][i]["character"]} for i in range(len(per_frame_list[frame_no]))]
				# print(orig_detections)
				new_detection = [{"x" : detections[i]["x"],"y" : detections[i]["y"], "w" : detections[i]["w"], "h" : detections[i]["h"]} for i in range(len(detections))]
				# print(new_detection)
				# break
				for unk_detect in new_detection :
					max_overlap = 0.
					final_label = "other"
					for kn_detect in orig_detections :
						overlap = iou(kn_detect, unk_detect)
						if overlap > max_overlap :
							max_overlap = overlap
							label = kn_detect["character"]
					if(max_overlap > iou_threshold) :
						final_label = label
					print(frame, max_overlap, final_label)
					unk_detect["character"] = final_label
				ftracks_labels[frame] = new_detection
			#print(ftracks_labels)

		with open("./Keypoints_bboxes_labels/{}.json".format(filename), 'w') as outfile :
			json.dump(ftracks_labels, outfile)	



