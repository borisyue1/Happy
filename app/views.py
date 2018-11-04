from app import app
from flask import render_template, flash, redirect, request
import json
import glob2
from .scripts.faces import get_emotions, get_frames
from .scripts.speech_text import wav_to_sentiment
import pandas as pd

WEBM_PATH = "uploads/*.webm"
JPEG_PATH = "temp/*.jpg"
HISTORICALS_PATH = "historicals.csv"
historicals_df = pd.read_csv(HISTORICALS_PATH)


@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/new_entry', methods=["GET", "POST"])
def new_entry():
	# try:
	print("Converting video to jpegs")
	webm_video_paths = glob2.glob(WEBM_PATH)
	webm_video_paths = sorted(webm_video_paths)
	latest_video_path = webm_video_paths[-1]
	get_frames(latest_video_path, "temp/") 

	print("Getting video sentiment")
	video_sentiments = [get_emotions(frame_path) for frame_path in glob2.glob(JPEG_PATH)]
	filtered_video_sentiments = {}
	for d in video_sentiments:
	    for k in d:
	    	if k not in filtered_video_sentiments:
	    		filtered_video_sentiments[k] = [d[k]]
	    	else:
	    		filtered_video_sentiments[k].append(d[k])
	mean = lambda numbers: float(sum(numbers)) / max(len(numbers), 1)
	for category in filtered_video_sentiments:
		filtered_video_sentiments[category] = mean(filtered_video_sentiments[category])

	print("Getting audio sentiment")
	audio_sentiment = wav_to_sentiment(WEBM_PATH)
	print("Video:", filtered_video_sentiments)
	print("Audio:", audio_sentiment)

	if latest_video_path not in historicals_df.path:
		new_row = [latest_video_path, 
		filtered_video_sentiments["contempt"],
		filtered_video_sentiments["happiness"],
		filtered_video_sentiments["neutral"],
		filtered_video_sentiments["fear"],
		filtered_video_sentiments["sadness"],
		filtered_video_sentiments["disgust"],
		filtered_video_sentiments["surprise"],
		filtered_video_sentiments["anger"],
		audio_sentiment]
		historicals_df.loc[-1] = new_row
		historicals_df.to_csv(HISTORICALS_PATH, index=False)

	return render_template("index.html", video_sentiments=filtered_video_sentiments, audio_sentiment=audio_sentiment)

	# except:
	# 	return render_template("index.html")
@app.route('/chart', methods=["GET"])
def chart():
    labels = ["Contempt","Happiness","Neutral","Fear","Sadness","Disgust","Surprise","Anger"]
    values = [1, 10, 2, 5, 7, 5, 5, 5]
    return render_template('chart.html', values=values, labels=labels)







    
