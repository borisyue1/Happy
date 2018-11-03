import cognitive_face as CF
import json

KEY = '5e92cce5700441968ecaaedbb7a4d4bb'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)
BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

def get_emotions(path):
	#Path can either be a link or 
	"""[{'faceId': '78774c2a-95a3-467e-8261-084a267485c0', 
	'faceAttributes': {'smile': 1.0, 
				'emotion': {'surprise': 0.0, 'contempt': 0.0, 'happiness': 1.0, 'neutral': 0.0, 'anger': 0.0, 'sadness': 0.0, 'fear': 0.0, 'disgust': 0.0}}, 'faceRectangle': {'width': 94, 'top': 117, 'height': 94, 'left': 98}}]"""
	  # Replace with your regional Base URL
	
	faces = CF.face.detect(path, attributes="emotion")
	return faces[0]["faceAttributes"]["emotion"]
