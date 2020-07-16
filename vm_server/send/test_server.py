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
import test_initialisation
import threading
import requests
from flask import Flask, request
from proto import request_pb2


APP = Flask(__name__)
URL = "http://127.0.0.1:8000/assign_task"
ROOT = ".\\"
RESPONSE = False
REQUEST_ID = 0
ALL_TESTS = "all"
TEST_1 = "1"
TEST_2 = "2"
TEST_3 = "3"
TEST_4 = "4"
# parser = argparse.ArgumentParser(description="Tets the working of VM Server")
# parser.add_argument("test_flag",
#                     type=str,
#                     help="""Usage: " + sys.argv[0] +  "TEST_FLAG
#                     TEST_FLAG : Test description
#                     1 : Run query1.txt test
#                     2 : Run query2.txt test
#                     3 : Run query3.txt test
#                     """)
# arguments = parser.parse_args()

def usage_message():
  """Prints the valid usage details"""
  logging.debug("Usage: %s TEST_FLAG", sys.argv[0])
  logging.debug("TEST_FLAG : Test description")
  logging.debug("--all : Run all tests at once")
  logging.debug("--1 : Run query1.txt test")
  logging.debug("--2 : Run query2.txt test")
  logging.debug("--3 : Run query3.txt test")

@APP.route("/success", methods=["GET", "POST"])
def success():
  """Endpoint to accept the POST request from the VM Servers when they
     complete the execution of the task
  """
  global REQUEST_ID
  global RESPONSE
  task_status_response = request_pb2.TaskStatusResponse()
  task_status_response.ParseFromString(request.files["task_response"].read())
  test_initialisation.save_proto_to_file("after_response.pb", task_status_response)
  if task_status_response.current_task_id == REQUEST_ID\
     and task_status_response.task_response.status \
     == request_pb2.TaskResponse.SUCCESS:
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
  logging.debug("Executing %s test", file_name)
  logging.debug("Creating proto file from %s", file_name)
  os.system("python .\\proto\\create_proto.py .\\proto\\" + file_name)
  task_request = request_pb2.TaskRequest()
  with open(ROOT + "input_request.pb", "rb") as input_request:
    task_request.ParseFromString(input_request.read())
  with open(ROOT + "input_request.pb", "rb") as input_request:
    response = requests.post(url=URL, files={"task_request": input_request})
    REQUEST_ID = task_request.request_id
    task_status_response = request_pb2.TaskStatusResponse()
    task_status_response.ParseFromString((response.content))
    logging.debug("Initial response : %s", str(task_status_response))
    logging.debug(type(response))
    logging.debug(str(response.content))
    if os.path.exists(ROOT + "response.pb"):
      os.remove(ROOT + "response.pb")
    with open(ROOT + "response.pb", "wb") as f:
      f.write(response.content)
      f.close()
    test_initialisation.save_proto_to_file("initial_response.pb", task_status_response)
    if task_status_response.status == request_pb2.TaskStatusResponse.ACCEPTED:
      logging.debug("Request was accepted.")
      logging.debug("Starting up server and listening to the response")
      RESPONSE = False
      # thread = threading.Thread(target=start_server)
      thread = test_initialisation.KThread(target=start_server)
      thread.start()
      thread.join(int(task_request.timeout) + 10)
      if thread.is_alive():
        thread.kill()
        thread.join()
      if RESPONSE is True:
        logging.debug("Test %s passed", str(proto_text_number))
      else:
        logging.debug("Test %s failed", str(proto_text_number))
      return RESPONSE
    else:
      logging.debug("Request was not accepted")
      logging.debug(str(task_status_response))
      return False
  
if __name__ == "__main__":
  logging.basicConfig(filename="response.log",
                      level=logging.DEBUG,
                      format="%(asctime)s:%(levelname)s: %(message)s")
  logging.getLogger().addHandler(logging.StreamHandler())
