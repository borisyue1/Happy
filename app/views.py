from app import app
from flask import render_template, flash, redirect, request
import json
import glob2
from .scripts.faces import get_emotions
from .scripts.webm_to_jpg import get_frames
from .scripts.speech_text import wav_to_sentiment
import math

WEBM_PATH = "TEMP.webm"
JPEG_PATH = ".jpg"

@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/new_entry', methods=["POST"])
def new_entry():
	get_frames(WEBM_PATH) #clean up tomorrow
	video_sentiments = [get_emotions(frame_path) for frame_path in glob2.glob(JPEG_PATH)]
	filtered_video_sentiments = {}
	for d in filtered_video_sentiments:
	    for k, v in d.iteritems(): 
	        filtered_video_sentiments.setdefault(k, []).append(v)

	for category in filtered_video_sentiments:
		filtered_video_sentiments[category] = math.mean(filtered_video_sentiments[category])
	audio_sentiment = wav_to_sentiment(WEBM_PATH)
	return render_template("index.html")

@app.route('/chart', methods=["GET"])
def chart():
    labels = ["Contempt","Happiness","Neutral","Fear","Sadness","Disgust","Surprise","Anger"]
    values = [10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=labels)