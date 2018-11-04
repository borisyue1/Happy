from app import app
from flask import render_template, flash, redirect, request
import json
import glob2
import os
from .scripts.faces import get_emotions, get_frames
from .scripts.speech_text import wav_to_sentiment
import pandas as pd
import numpy as np

WEBM_PATH = "uploads/*.webm"
JPEG_PATH = "temp/*.jpg"
HISTORICALS_PATH = "historicals.csv"
historicals_df = pd.read_csv(HISTORICALS_PATH, index_col=0)
LABELS = ["Contempt","Happiness","Neutral","Fear","Sadness","Disgust","Surprise","Anger"]
result_lst = ["contemptuous",
			   "happy",
			   "neutral",
			   "scared" ,
			   "sad",
			   "disgusted",
			   "surprised",
			   "angry"]


@app.route('/')
@app.route('/index', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/result', methods=["GET", "POST"])
def result():
	app.logger.info("Converting video to jpegs")
	webm_video_paths = glob2.glob(WEBM_PATH)
	webm_video_paths = sorted(webm_video_paths)
	latest_video_path = webm_video_paths[-1]
	get_frames(latest_video_path, "temp/") 

	app.logger.info("Getting video sentiment %s", glob2.glob(JPEG_PATH))
	video_sentiments = [get_emotions(frame_path) for frame_path in glob2.glob(JPEG_PATH)]

	app.logger.debug(video_sentiments)

	filtered_video_sentiments = {}
	for d in video_sentiments:
	    for k in d:
	    	if k not in filtered_video_sentiments:
	    		filtered_video_sentiments[k] = [d[k]]
	    	else:
	    		filtered_video_sentiments[k].append(d[k])
	mean = lambda numbers: float(sum(numbers)) / max(len(numbers), 1)
	for category in filtered_video_sentiments:
		filtered_video_sentiments[category] = int(10 * mean(filtered_video_sentiments[category]))

	app.logger.info("Getting audio sentiment")
	audio_sentiment = wav_to_sentiment(latest_video_path)
	app.logger.info("Video:", filtered_video_sentiments)
	app.logger.info("Audio:", audio_sentiment)

	new_row = [filtered_video_sentiments.get("contempt", 0),
		filtered_video_sentiments.get("happiness", 0),
		filtered_video_sentiments.get("neutral", 0),
		filtered_video_sentiments.get("fear", 0),
		filtered_video_sentiments.get("sadness", 0),
		filtered_video_sentiments.get("disgust", 0),
		filtered_video_sentiments.get("surprise", 0),
		filtered_video_sentiments.get("anger", 0),
		audio_sentiment]
	if latest_video_path not in historicals_df.index:
		historicals_df.loc[latest_video_path] = new_row
		historicals_df.to_csv(HISTORICALS_PATH)

	max_feel = np.argmax(new_row)

	app.logger.debug(result_lst)

	# TODO: hacky
	if max_feel == 8:
		max_feel = 2

	return render_template("chart.html", values=new_row[:-1], labels=LABELS, result=result_lst[max_feel], voice_sent=audio_sentiment)


ALLOWED_EXTENSIONS = ['webm']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        filename = request.form['filename']

        app.logger.info("Incomming filename %s", filename)

        if file and allowed_file(filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # TODO: hacky
            return "/uploads/" + filename

        app.logger.info("File %s uploaded", filename)
    else:
    	return "Get method not implemented"
