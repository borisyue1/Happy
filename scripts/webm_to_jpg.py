import os 

def get_frames(path, fps=1/2):
	os.system("ffmpeg -i {} -vf fps={} thumb%04d.jpg -hide_banner".format(path, fps))

