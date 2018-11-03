import os 

def get_frames(path):
	os.system("ffmpeg -i {} -vf fps=1/2 thumb%04d.jpg -hide_banner".format(path))

