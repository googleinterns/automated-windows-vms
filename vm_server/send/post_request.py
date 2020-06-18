#!/usr/bin/python
"""Program to send a post request with
  the proto file and accept and
  save the response in response.pb

  It takes the input_request.pb in the .\\proto\\ directory
  sends it to the VM server, and accepts the response as
  response.pb and saves it in .\\proto\\ directory
"""
import logging
import os
import requests

logging.basicConfig(filename='response.log', level=logging.DEBUG)
URL = "http://127.0.0.1:5000/load"
ROOT = ".\\proto\\"
with open(ROOT + 'input_request.pb', 'rb') as input_request:
  RESPONSE = requests.post(url=URL, files={'task_request': input_request})
logging.debug(type(RESPONSE))
logging.debug(str(RESPONSE.content))
if os.path.exists(ROOT + "response.pb"):
  os.remove(ROOT + "response.pb")
with open(ROOT + "response.pb", "wb") as f:
  f.write(RESPONSE.content)
  f.close()
