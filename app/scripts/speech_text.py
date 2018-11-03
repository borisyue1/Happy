import http.client, urllib.request, urllib.error, json

speech_key = '1613da9943af4aaaaad4735e5e3a57f7'
text_key = '473f753648de4199a0eb24b38d7b884b'


def speech_to_text(input_file='../test.wav'):
  with open(input_file, mode='rb') as file:
    data = file.read()

  speech_headers = {
      # Request headers for speech to text
      'Content-Type': 'audio/wav; codec=audio/pcm; samplerate=16000',
      'Ocp-Apim-Subscription-Key': speech_key,
  }
  try:
      conn = http.client.HTTPSConnection('westus.stt.speech.microsoft.com')
      conn.request("POST", "/speech/recognition/conversation/cognitiveservices/v1?language=en-US", data, speech_headers)
      response = conn.getresponse()
      text_data = json.loads(response.read().decode("utf-8")) #convert byte array to dictionary
      conn.close()
      return text_data['DisplayText']
  except Exception as e:
      print("[Errno {0}] {1}".format(e.errno, e.strerror))

def sentiment(text):
  text_headers = {
      # Request headers for text sentiment
      'Content-Type': 'application/json',
      'Ocp-Apim-Subscription-Key': text_key,
  }
  request_body = {'documents': [
    {'id': '1', 'language': 'en', 'text': text}
  ]}
  try:
      conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
      conn.request("POST", "/text/analytics/v2.0/sentiment", str(request_body), text_headers)
      response = conn.getresponse()
      sentiment = json.loads(response.read().decode("utf-8")) #convert byte array to dictionary
      conn.close()
      return sentiment['documents'][0]["score"]
  except Exception as e:
      print("[Errno {0}] {1}".format(e.errno, e.strerror))


text = speech_to_text()
print("Sentiment Score:", sentiment(text))