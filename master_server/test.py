import argparse
import os
import sys
import threading
import time
import requests
from google.protobuf import text_format
import Request_pb2

parser = argparse.ArgumentParser()

#-db DATABSE -u USERNAME -p PASSWORD -size 20
parser.add_argument('-st', '--start_port', help='Starting port number', type=int)
parser.add_argument('-c', '--count', help='Number of port needed' ,type=int)
parser.add_argument('-f', '--filename', help='File name of text file')
parser.add_argument('-n', '--number', help='Number of times to repeat the request', type=int)
args = parser.parse_args()
port = args.start_port

def new_dummy_server():
  global port
  port = port + 1
  os.system('python dummy_vm_server.py ' + str(port))

def master_server():
  os.system('python master_server.py')

if __name__ == '__main__':
  print( 'Starting_port {} Count {} filename {} number {} '.format(
        args.start_port,
        args.count,
        args.filename,
        args.number
        ))
  t = threading.Thread(target = master_server)
  t.start()
  time.sleep(5)
  count = args.count
  for i in range(count):
    t = threading.Thread(target = new_dummy_server)
    t.start()
    
  time.sleep(5)
  TEXT_FILE = open(args.filename, 'r')
  TASK_REQUEST = Request_pb2.TaskRequest()
  text_format.Parse(TEXT_FILE.read(), TASK_REQUEST)
  TEXT_FILE.close()
  
  for i in range(args.number):
    RESPONSE = requests.post(url='http://127.0.0.1:5000/assign_task', files={'file': TASK_REQUEST.SerializeToString()})
    print(RESPONSE.content)
