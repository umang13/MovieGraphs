#!/usr/bin/env python3
import subprocess
with open("./mg_videoinfo/scene_boundaries/tt1285016.scenes.gt") as f, open("./mg_videoinfo/video_boundaries/tt1285016.videvents") as g, open("./mg_videoinfo/video_boundaries/tt1285016.matidx") as h:
	shot_dict = {}
	frame_dict = {}
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


	count = 1
	# print(shot_dict)
	for line in f.readlines():
		start_shot, end_shot, imp = line.strip().split(' ')
		if imp == '0' :
			count +=1
			continue
		start_time = shot_dict.get(int(start_shot))["start_time"]
		end_time = shot_dict.get(int(end_shot))["end_time"]
		start_frame = shot_dict.get(int(start_shot))["start_frame"]
		end_frame = shot_dict.get(int(end_shot))["end_frame"]


		cmd = "ffmpeg -ss {} -to {} -i ./TheSocialNetwork.mp4 -vcodec copy -acodec copy ./Video_Splits_1/scene-{:03}.ss-{:04}.es-{:04}.mp4".format(start_time, end_time, count, int(start_shot), int(end_shot))
		print(cmd)
		count += 1
		subprocess.call(cmd, shell=True)