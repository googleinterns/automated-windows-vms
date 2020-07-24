"""This script sends the task requests to the Master server."""
import requests
with open("input_request_1.pb", "rb") as input_request:
  RESPONSE = requests.post(url="http://127.0.0.1:5000/uploader", files={"file": input_request})
  print(RESPONSE.content)
with open("input_request.pb", "rb") as input_request:
  RESPONSE = requests.post(url="http://127.0.0.1:5000/uploader", files={"file": input_request})
  print(RESPONSE.content)
