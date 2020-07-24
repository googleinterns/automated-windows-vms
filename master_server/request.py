"""Query the master server about any previous request."""
import requests
import sys
if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], 'Request_id')
    sys.exit(-1)
RESPONSE = requests.post(url="http://127.0.0.1:5000/request_status", data={"request_id": int(sys.argv[1])})
print(RESPONSE.content)
