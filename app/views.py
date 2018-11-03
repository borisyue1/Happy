from app import app
from flask import render_template, flash, redirect, request
import json
import glob2
from .scripts.faces import get_emotions, get_frames
from .scripts.speech_text import wav_to_sentiment

WEBM_PATH = "app/recordings/11_3.webm"
JPEG_PATH = "app/recordings/*.jpg"

@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/new_entry', methods=["GET", "POST"])
def new_entry():
	get_frames(WEBM_PATH) #clean up tomorrow
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
	
	audio_sentiment = wav_to_sentiment(WEBM_PATH)

	print(video_sentiments)
	print("Video:", filtered_video_sentiments)
	print("Audio:", audio_sentiment)
	return render_template("index.html")