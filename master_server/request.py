import requests
import sys
RESPONSE = requests.post(url="http://127.0.0.1:5000/request_status", data={"request_id": int(sys.argv[1])})
print(RESPONSE.content)
