"""Program to send a post request with the proto file and accept and save the response in response.pb"""
import requests
import os
URL='http://127.0.0.1:5000/load'

with open('input_request.pb','rb') as f:
    r=requests.post(url=URL,files={'task_request':f})
print(type(r))
print(str(r.content))
if os.path.exists("response.pb"):
    os.remove("response.pb")
with open("response.pb","wb") as f:
    f.write(r.content)
    f.close()
