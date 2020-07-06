import os
import threading
import sys
import time
import requests

port = int(sys.argv[1])

def new_dummy_server():
  global port
  port = port + 1
  os.system('python dummy_vm_server.py ' + str(port))

def master_server():
  os.system('python master_server.py')

if __name__ == '__main__':
  if len(sys.argv) != 5:
    print('Usage:', sys.argv[0], 'INPUT_PORT_START_NUMBER NUMBER_OF_VMs NUMBER_OF_TIMES_TO_SEND_REQUEST_FILE1 NUMBER_OF_TIMES_TO_SEND_REQUEST_FILE2')
    sys.exit(-1)
  t = threading.Thread(target = master_server)
  t.start()
  time.sleep(5)
  count = int(sys.argv[2])
  for i in range(count):
    t = threading.Thread(target = new_dummy_server)
    t.start()
    
  time.sleep(5)
  for i in range(int(sys.argv[3])):
    with open("input_request_1.pb", "rb") as input_request:
      RESPONSE = requests.post(url="http://127.0.0.1:5000/assign_task", files={"file": input_request})
      print(RESPONSE.content)
  for i in range(int(sys.argv[4])):
    with open("input_request.pb", "rb") as input_request:
      RESPONSE = requests.post(url="http://127.0.0.1:5000/assign_task", files={"file": input_request})
      print(RESPONSE.content)
