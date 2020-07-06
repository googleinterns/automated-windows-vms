#!/usr/bin/python
"""Script to create the protofile

    It compiles the proto definition and
    then creates the proto file from the text specified
    in query1.txt or query2.txt
"""
import logging
import os
import sys
import requests
from flask import Flask, request, send_file
from waitress import serve
from proto import Request_pb2
import signal
import threading
import trace
import multiprocessing

APP = Flask(__name__)
URL = "http://127.0.0.1:8000/assign_task"
ROOT = ".\\"
RESPONSE = False
REQUEST_ID=0

class KThread(threading.Thread):
  """A subclass of threading.Thread, with a kill() method."""
  
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    """Start the thread."""
    self.__run_backup = self.run
    self.run = self.__run      # Force the Thread to install our trace.
    threading.Thread.start(self)

  def __run(self):
    """Hacked run function, which installs the trace."""
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True

def usage_message():
  """Prints the valid usage details"""
  print("Usage:", sys.argv[0], "TEST_FLAG")
  print("TEST_FLAG : Test description")
  print("--all : Run all tests at once")
  print("--1 : Run query1.txt test")
  print("--2 : Run query2.txt test")
  print("--3 : Run query3.txt test")
  logging.debug("Usage:", sys.argv[0], "TEST_FLAG")

@APP.route("/success", methods=["GET", "POST"])
def success():
  print("I am in success")
  global REQUEST_ID
  global RESPONSE
  print(1)
  task_status_response = Request_pb2.TaskStatusResponse()
  print(2)
  task_status_response.ParseFromString(request.files["task_response"].read())
  print(3)
  # logging.debug("The response proto is : " + str(task_status_response))
  print("The response proto is :" + str(task_status_response))
  print(4)
  if task_status_response.current_task_id == REQUEST_ID:
    if task_status_response.task_response.status == Request_pb2.TaskResponse.SUCCESS:
      RESPONSE = True 
  print(5)
  if RESPONSE == True:
    print("I am here")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
      raise RuntimeError("Not running with the Werkzeug Server")
    func()
  return "Success endpoint"



def start_server():
  # serve(APP, host='127.0.0.1', port=5000)
  APP.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)

def execute_commands(proto_text_number):
  """Executes commands to compile and create a proto file

  Args:
    proto_text_number: File number of the text file from where 
    the input information for the proto request is read.
    For example, query1.txt, query2.txt etc
  """
  global REQUEST_ID
  global RESPONSE
  file_name = "query" + str(proto_text_number) + ".txt"
  print("Executing " + file_name + " test")
  logging.debug("Executing" + file_name + "test")
  logging.debug("Creating proto file from" + file_name)
  os.system("python .\\proto\\create_proto.py .\\proto\\" + file_name)
  task_request = Request_pb2.TaskRequest()
  with open(ROOT + "input_request.pb", "rb") as input_request:
    task_request.ParseFromString(input_request.read())
  with open(ROOT + "input_request.pb", "rb") as input_request:
    print("I am here0")
    response = requests.post(url=URL, files={"task_request": input_request})
    print("I am here1")
    print("Sending this proto: " + str(task_request))
    print(task_request.timeout)
    print("I am here2")
    REQUEST_ID = task_request.request_id
    task_status_response = Request_pb2.TaskStatusResponse()
    task_status_response.ParseFromString((response.content))
    print(task_status_response)
    if task_status_response.status == Request_pb2.TaskStatusResponse.ACCEPTED:
      logging.debug("Request was accepted. Starting up server and listening to the response")
      RESPONSE = False
      print("I am here")
      print("Timeout is " + str(task_request.timeout))
      print(task_request.timeout)
      # thread = threading.Thread(target=start_server)
      thread = KThread(target=start_server)
      thread.start()
      thread.join(int(task_request.timeout))
      print("Done with thread")
      if thread.is_alive():
        # thread.terminate()
        # thread._stop_event.set()
        print("Trying to kill the alive thread")
        thread.kill()
        thread.join()
      print("Response is ", RESPONSE)
      if RESPONSE == True:
        print("Test "+ str(proto_text_number) + "passed")
      else:
        print("Test "+ str(proto_text_number) + "failed")
    else:
      logging.debug("Request was not accepted")
      logging.debug(str(task_status_response))
      return

  print(type(response))
  print(response.content)
  logging.debug(type(response))
  logging.debug(str(response.content))
  if os.path.exists(ROOT + "response.pb"):
    os.remove(ROOT + "response.pb")
  with open(ROOT + "response.pb", "wb") as f:
    f.write(response.content)
    f.close()




if __name__ == "__main__":
  logging.basicConfig(filename="server.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s: %(message)s")
  logging.getLogger().addHandler(logging.StreamHandler())
  # APP.run(debug=True, host='127.0.0.1', port=5000)
  if len(sys.argv) != 2:
    usage_message()
    sys.exit(-1)
  if sys.argv[1] == "--all":
    for file_id in range(1,4):
      try:
        execute_commands(file_id)
      except Exception as err:
        print(err)
        logging.debug(err)
        sys.exit(-1)
  elif sys.argv[1] == "--1":
    file_id = 1
    try:
        execute_commands(file_id)
    except Exception as err:
      print(err)
      logging.debug(err)
      sys.exit(-1)
  elif sys.argv[1] == "--2":
    file_id = 2
    try:
        execute_commands(file_id)
    except Exception as err:
      print(err)
      logging.debug(err)
      sys.exit(-1)
  elif sys.argv[1] == "--3":
    file_id = 3
    try:
        execute_commands(file_id)
    except Exception as err:
      print(err)
      logging.debug(err)
      sys.exit(-1)
  else:
    usage_message()
    sys.exit(-1)
