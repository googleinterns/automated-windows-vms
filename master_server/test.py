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
  os.system('python master_server.py -d b')

def send_request():
  print(os.getcwd())
  
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
  
  for i in range(args.number):
    RESPONSE = requests.post(url='http://127.0.0.1:5000/assign_task',
        files={'file': TASK_REQUEST.SerializeToString()})
    file_A = Request_pb2.TaskStatusResponse()
    file_A.ParseFromString(RESPONSE.content)
    if file_A.status == Request_pb2.TaskStatusResponse.ACCEPTED :
      t = threading.Thread(target = response, args= (file_a, file_A,
          file_b, TASK_REQUEST.timeout, TASK_REQUEST.number_of_retries))
      t.start()
    else:
      print(file_A)
    
def response(file_a, file_A, file_b, timeout, number_of_retries):
  timer = timeout * (number_of_retries + 10)
  time.sleep(timer)
  task_status_request = Request_pb2.TaskStatusRequest()
  task_status_request.request_id = file_A.current_task_id
  RESPONSE = requests.post(url= 'http://127.0.0.1:5000/get_status',
      files = {'file': task_status_request.SerializeToString()})
  file_B = Request_pb2.TaskStatusResponse()
  file_B.ParseFromString(RESPONSE.content)
  match_proto(file_a, file_A , file_b, file_B)

def match_proto(file_a, file_A ,file_b, file_B):
  if file_b.status == file_B.status and file_b.task_response.status == file_B.task_response.status:
    print('Task request ' + str(file_A.current_task_id) + ' matched successfully')
  else:
    print('Task request ' + str(file_A.current_task_id) + ' did not matched successfully')

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
  folder_list = args.filename.split(',')
  for folder in folder_list:
    os.chdir(os.path.join(os.getcwd(), folder))
    send_request()
    os.chdir('..')
