import argparse
import os
import sys
import threading
import time
import requests
from google.protobuf import text_format
import Request_pb2

def new_dummy_server(port):
  try:
    os.system('python server.py gsutil ' + str(port))
  except Exception as e:
    print(e)

def master_server():
  try:
    os.system('python master_server.py -d b')
  except Exception as e:
    print(e)

def start_server(starting_port, number_of_vms, test_directory):
  t = threading.Thread(target = master_server)
  t.start()
  time.sleep(5)
  count = number_of_vms
  for port in range(count):
    t = threading.Thread(target = new_dummy_server, args= (starting_port + port,))
    t.start()
  time.sleep(10)
  os.chdir(os.path.join(os.getcwd(), test_directory))

  TEXT_FILE = open('task_request.txt', 'r')
  TASK_REQUEST = Request_pb2.TaskRequest()
  text_format.Parse(TEXT_FILE.read(), TASK_REQUEST)
  TEXT_FILE.close()
    
  file_a = Request_pb2.TaskStatusResponse()
  file_b = Request_pb2.TaskStatusResponse()
  fil = open('initial_task_response.txt', 'r')
  text_format.Parse(fil.read(), file_a)
  fil.close()
  fil = open('final_task_response.txt', 'r')
  text_format.Parse(fil.read(), file_b)
  fil.close()
  os.chdir('..')
  return TASK_REQUEST,file_a,file_b
