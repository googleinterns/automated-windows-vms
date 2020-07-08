#!/usr/bin/python
"""Script to create the protofile

    It compiles the proto definition and
    then creates the proto file from the text specified
    in query1.txt or query2.txt
"""
import argparse
import logging
import os
import sys
import threading
import requests
from flask import Flask, request
from proto import Request_pb2


APP = Flask(__name__)
URL = "http://127.0.0.1:8000/assign_task"
ROOT = ".\\"
RESPONSE = False
REQUEST_ID = 0
ALL_TESTS = "all"
TEST_1 = "1"
TEST_2 = "2"
TEST_3 = "3"
parser =  argparse.ArgumentParser(description="Tets the working of VM Server")
parser.add_argument("test_flag", 
                    type=str,
                    help="""Usage: " + sys.argv[0] +  "TEST_FLAG
                    TEST_FLAG : Test description
                    1 : Run query1.txt test
                    2 : Run query2.txt test
                    3 : Run query3.txt test
                    """)
args = parser.parse_args()


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
  logging.debug("Usage: " + sys.argv[0] +  " TEST_FLAG")
  logging.debug("TEST_FLAG : Test description")
  logging.debug("--all : Run all tests at once")
  logging.debug("--1 : Run query1.txt test")
  logging.debug("--2 : Run query2.txt test")
  logging.debug("--3 : Run query3.txt test")
  logging.debug("Usage:" +  sys.argv[0] + "TEST_FLAG")

@APP.route("/success", methods=["GET", "POST"])
def success():
  """Endpoint to accept the POST request from the VM Servers when they
     complete the execution of the task
  """
  global REQUEST_ID
  global RESPONSE
  task_status_response = Request_pb2.TaskStatusResponse()
  task_status_response.ParseFromString(request.files["task_response"].read())
  with open(ROOT + "after_response.pb", "wb") as after_response:
      after_response.write(task_status_response.SerializeToString())
      after_response.close()
  if task_status_response.current_task_id == REQUEST_ID and task_status_response.task_response.status == Request_pb2.TaskResponse.SUCCESS:
    RESPONSE = True
  if RESPONSE is True:
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
  logging.debug("Executing" + file_name + "test")
  logging.debug("Creating proto file from" + file_name)
  os.system("python .\\proto\\create_proto.py .\\proto\\" + file_name)
  task_request = Request_pb2.TaskRequest()
  with open(ROOT + "input_request.pb", "rb") as input_request:
    task_request.ParseFromString(input_request.read())
  with open(ROOT + "input_request.pb", "rb") as input_request:
    response = requests.post(url=URL, files={"task_request": input_request})
    REQUEST_ID = task_request.request_id
    task_status_response = Request_pb2.TaskStatusResponse()
    task_status_response.ParseFromString((response.content))
    logging.debug("Initial response : " + str(task_status_response))
    with open(ROOT + "initial_response.pb", "wb") as initial_response:
      initial_response.write(task_status_response.SerializeToString())
      initial_response.close()
    if task_status_response.status == Request_pb2.TaskStatusResponse.ACCEPTED:
      logging.debug("Request was accepted.")
      logging.debug("Starting up server and listening to the response")
      RESPONSE = False
      # thread = threading.Thread(target=start_server)
      thread = KThread(target=start_server)
      thread.start()
      thread.join(int(task_request.timeout))
      if thread.is_alive():
        thread.kill()
        thread.join()
      if RESPONSE is True:
        logging.debug("Test "+ str(proto_text_number) + " passed")
      else:
        logging.debug("Test "+ str(proto_text_number) + " failed")
    else:
      logging.debug("Request was not accepted")
      logging.debug(str(task_status_response))
  logging.debug(type(response))
  logging.debug(str(response.content))
  if os.path.exists(ROOT + "response.pb"):
    os.remove(ROOT + "response.pb")
  with open(ROOT + "response.pb", "wb") as f:
    f.write(response.content)
    f.close()

if __name__ == "__main__":
  logging.basicConfig(filename="server.log",
                      level=logging.DEBUG,
                      format="%(asctime)s:%(levelname)s: %(message)s")
  logging.getLogger().addHandler(logging.StreamHandler())
  # APP.run(debug=True, host='127.0.0.1', port=5000)
  if len(sys.argv) != 2:
    usage_message()
    sys.exit(-1)
  if args.test_flag == ALL_TESTS:
    for file_id in range(1, 4):
      try:
        execute_commands(file_id)
      except Exception as err:
        logging.debug(err)
        sys.exit(-1)
  elif args.test_flag == TEST_1:
    file_id = 1
    try:
      execute_commands(file_id)
    except Exception as err:
      logging.debug(err)
      sys.exit(-1)
  elif args.test_flag == TEST_2:
    file_id = 2
    try:
      execute_commands(file_id)
    except Exception as err:
      logging.debug(err)
      sys.exit(-1)
  elif args.test_flag == TEST_3:
    file_id = 3
    try:
      execute_commands(file_id)
    except Exception as err:
      logging.debug(err)
      sys.exit(-1)
  else:
    usage_message()
    sys.exit(-1)
