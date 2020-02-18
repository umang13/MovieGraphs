#!/bin/bash

exec 3<list
count=1

while read -u 3 line ; do

	read start endtime _ <<< "$line"

	echo ffmpeg -ss "$start" -to "$endtime" -i "$1" -vcodec copy -acodec copy "$HOME/Downloads/Video_Splits/SocialNetwork-$(( count )).mp4"
	ffmpeg -ss "$start" -to "$endtime" -i "$1" -vcodec copy -acodec copy "$HOME/Downloads/Video_Splits/SocialNetwork-$(( count++ )).mp4"

done
