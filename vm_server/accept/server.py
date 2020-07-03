#!/usr/bin/python
"""This is the flask server of the a windows VM

  It accepts the requests in the form of protobufs
  and executes the same in the specified path
"""
import logging
import shutil
import timeit
import os
import subprocess
from pathlib import Path
import threading
from flask import Flask, request, send_file
import repackage
repackage.up(2)
from vm_server.send.proto import Request_pb2


sem = threading.Semaphore()

def remove_execute_dir(task_response):
  """Deletes the execute directory if it exists

  Args:
    task_response: an object of TaskResponse() that will be sent back
  """
  logging.debug("Removing execute directory")
  dirpath = Path("..\\execute")
  try:
    if dirpath.exists() and dirpath.is_dir(): # delete leftover files
      shutil.rmtree(dirpath)
  except Exception as exception:  #catch errors if any
    logging.exception(str(exception))
    logging.debug("Error deleting the execute directory")
    task_response.status = Request_pb2.TaskResponse.FAILURE

def make_directories(task_request, task_response):
  """Creates the directories for execution

  Args:
    task_request: TaskRequest() object that is read from the protobuf
    task_response: an object of TaskResponse() that will be sent back
  """
  logging.debug("Creating execute directory structure")
  remove_execute_dir(task_response)
  if task_response.status == Request_pb2.TaskResponse.FAILURE:
    return
  current_path = "..\\execute\\action"
  os.mkdir("..\\execute")
  os.mkdir(current_path)
  os.mkdir(current_path + "\\output\\")
  Path("..\\execute\\__init__.py").touch() # __init__.py for package
  Path(current_path + "\\__init__.py").touch()
  try:
    shutil.copytree(task_request.code_path, current_path + "\\code")
    Path(current_path + "\\code\\__init__.py").touch() # __init__.py for package
    shutil.copytree(task_request.data_path, current_path + "\\data")
  except Exception as exception:  #catch errors if any
    logging.exception(str(exception))
    logging.debug("Error copying code and data directories")
    task_response.status = Request_pb2.TaskResponse.FAILURE

def move_output(task_request, task_response):
  """Move the genrated output files to the output path specified

  Args:
    task_request: an object of TaskResponse() that is sent in the request
    task_response: an object of TaskResponse() that will be sent back
  """
  logging.debug("Moving the output path", end=" ")
  logging.debug("to the specified output path")
  source_path = "..\\execute\\action\\output\\"
  destination_path = task_request.output_path
  files = os.listdir(source_path)
  try:
    for file in files:
      shutil.move(source_path + file, destination_path)
  except Exception as exception:  #catch errors if any
    logging.exception(str(exception))
    logging.debug("Error moving the output files", end=" ")
    logging.debug("to the specified output directory")
    task_response.status = Request_pb2.TaskResponse.FAILURE


def execute_action(task_request, task_response):
  """ Execute the action

  Args:
    task_request: an object of TaskResponse() that is sent in the request
    task_response: an object of TaskResponse() that will be sent back
  """
  if task_response.status == Request_pb2.TaskResponse.FAILURE:
    return
  logging.debug("Trying to execute the action")
  current_path = "..\\execute\\action"
  logging.debug("Action path is:", end=" ")
  logging.debug(str(current_path + task_request.target_path))
  encoding = "utf-8"
  out = None
  err = None
  try:
    execute = subprocess.Popen(["powershell.exe", # execute the target file
                                task_request.target_path],
                               stdout=subprocess.PIPE,
                               cwd=current_path)
    out, err = execute.communicate(timeout=task_request.timeout)
  except Exception as exception:  # catch errors if any
    logging.debug(str(exception))
    logging.debug("FAILED TO EXECUTE THE ACTION")
    task_response.status = Request_pb2.TaskResponse.FAILURE
    err = str(exception).encode(encoding)
  if out is None:
    out = "".encode(encoding)
  if err is None:
    err = "".encode(encoding)
  try:
    std_out = open(current_path + "\\output\\stdout.txt", "w")
    std_out.write(out.decode(encoding))
    std_out.close()
    std_err = open(current_path + "\\output\\stderr.txt", "w")
    std_err.write(err.decode(encoding))
    std_err.close()
    output_files = [name for name in os.listdir("..\\execute\\action\\output\\")
                    if os.path.isfile("..\\execute\\action\\output\\" + name)]
    task_response.number_of_files = len(output_files)
    move_output(task_request, task_response)
  except Exception as exception:
    logging.debug("Error writing in std out, stderr" + str(exception))
    task_response.status = Request_pb2.TaskResponse.FAILURE


APP = Flask(__name__)
@APP.route("/load", methods=["POST"])
def load():
  """load endpoint. Accepts post requests with protobuffer"""
  task_response = Request_pb2.TaskResponse()
  if sem.acquire(blocking=False):
    logging.debug("Accepted request: " + str(request))
    task_request = Request_pb2.TaskRequest()
    task_request.ParseFromString(request.files["task_request"].read())
    logging.debug("Request Proto: " + str(task_request))
    start = timeit.default_timer()
    make_directories(task_request, task_response)
    execute_action(task_request, task_response)
    stop = timeit.default_timer()
    time_taken = stop-start
    logging.debug("Time taken is " + str(time_taken))
    task_response.time_taken = time_taken
    if task_response.status != Request_pb2.TaskResponse.FAILURE:
      task_response.status = Request_pb2.TaskResponse.SUCCESS
    current_path = os.path.dirname(os.path.realpath("__file__"))
    response_proto = os.path.join(current_path, "..\\execute\\response.pb")
    with open(response_proto, "wb") as response:
      response.write(task_response.SerializeToString())
      response.close()
    sem.release()
  else:
    task_response.status = Request_pb2.TaskResponse.BUSY
    with open(response_proto, "wb") as response:
      response.write(task_response.SerializeToString())
      response.close()
  logging.debug("Response Proto: " + str(task_response))
  return send_file(response_proto)

if __name__ == "__main__":
  logging.basicConfig(filename="server.log",
                      level=logging.DEBUG,
                      format="%(asctime)s:%(levelname)s: %(message)s")
  logging.getLogger().addHandler(logging.StreamHandler())
  APP.run(debug=True)
