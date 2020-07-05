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
from waitress import serve
import requests


sem = threading.Semaphore()
MASTER_SERVER = "http://127.0.0.1:5000"
request_id=""
task_response = Request_pb2.TaskResponse()
task_request = Request_pb2.TaskRequest()
task_status_response = Request_pb2.TaskStatusResponse()
PORT = 8000
VM_ADDRESS = "127.0.0.1"

def get_processes(file_name):
  """Logs the current running processes in the file named file_name

  Args:
    file_name: Name of the file where the names of the processes are saved 
  """
  logging.debug("Getting the list of processes")
  get_process = subprocess.Popen("powershell.exe Get-Process >{file}".format(file=file_name))
  get_process.communicate()

def get_diff_processes():
  """Prints the difference in processes before and after execution of a request"""
  logging.debug("Getting the diff of the processes")
  compare_process = subprocess.Popen("powershell.exe Compare-Object (Get-Content process_before.txt) (Get-Content process_after.txt)")
  compare_process.communicate()

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
    data_path = Path(task_request.data_path)
    if data_path.exists() == False:
      os.mkdir(data_path)
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
  logging.debug("Moving the output path to the specified output path")
  current_path = os.getcwd()
  source_path = Path(current_path + "\\..\\execute\\action\\output\\")
  if source_path.exists() == False:
      os.mkdir(source_path)
  destination_path = current_path + "\\" + task_request.output_path
  files = os.listdir(source_path)
  try:
    for file in files:
      shutil.move(os.path.join(source_path, file), os.path.join(destination_path, file))
  except Exception as exception:  #catch errors if any
    logging.exception(str(exception))
    logging.debug("Error moving the output files to the specified output directory")
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
  logging.debug("Action path is: " + str(current_path + task_request.target_path))
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
  try:
    os.kill(execute.pid, 0)
  except OSError:
    logging.debug("PID is unassigned. The process exited on its own")
  else:
    logging.debug("Process is running, force killing the process")
    kill_process = subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=execute.pid))
    kill_process.communicate()
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

def register_vm_address():
  data = "http://" + VM_ADDRESS + ":" + str(PORT)
  try:
    request = requests.get(MASTER_SERVER + str("/register"), data=data)
  except:
    logging.debug("Can't connect to the master server")

def task_completed(task_request, task_response):
  if task_response.status != Request_pb2.TaskResponse.FAILURE:
      task_response.status = Request_pb2.TaskResponse.SUCCESS
  current_path = os.path.dirname(os.path.realpath("__file__"))
  response_proto = os.path.join(current_path, ".\\response.pb")
  with open(response_proto, "wb") as response:
    response.write(task_response.SerializeToString())
    response.close()
  remove_execute_dir(task_response)
  logging.debug("Response Proto: " + str(task_response))
  get_processes("process_after.txt")
  get_diff_processes()
  sem.release()
  response = requests.post(url="http://" + MASTER_SERVER + "/success",
                            files={
                              "task_response" : response_proto,
                              "request_id" : ("", str(task_request.request_id)) 
                            }
                          )
  # return send_file(response_proto)
  

def execute_wrapper(task_request, task_response):
  global task_status_response
  start = timeit.default_timer()
  make_directories(task_request, task_response)
  execute_action(task_request, task_response)
  stop = timeit.default_timer()
  time_taken = stop-start
  logging.debug("Time taken is " + str(time_taken))
  task_response.time_taken = time_taken
  task_status_response.status = Request_pb2.TaskStatusResponse.COMPLETED
  task_completed(task_request, task_response)
  register_vm_address()


APP = Flask(__name__)

@APP.route("/get_status", methods=["POST"])
def get_status():
  global task_status_response
  request_task_status_response = Request_pb2.TaskStatusResponse()
  request_task_status_response.ParseFromString(request.files["task_request"].read())
  response_task_status = task_status_response
  if task_status_response.current_task_id != request_task_status_response.current_task_id:
    response_task_status.status = Request_pb2.TaskStatusResponse.INVALID_ID
  response_proto = os.path.join(current_path, ".\\response.pb")
  with open(response_proto, "wb") as response:
    response.write(response_task_status.SerializeToString())
    response.close()
  return send_file(response_proto)

@APP.route("/assign_task", methods=["POST"])
def assign_task():
  """load endpoint. Accepts post requests with protobuffer"""
  task_response = Request_pb2.TaskResponse()
  global task_status_response
  get_processes("process_before.txt")
  if sem.acquire(blocking=False):
    logging.debug("Accepted request: " + str(request))
    task_request = Request_pb2.TaskRequest()
    task_request.ParseFromString(request.files["task_request"].read())
    logging.debug("Request Proto: " + str(task_request))
    thread = threading.Thread(target=execute_wrapper, args=(task_request, task_response,))
    thread.start()
    task_status_response.current_task_id = task_request.request_id
    task_status_response.status = Request_pb2.TaskStatusResponse.ACCEPTED
  else:
    task_status_response.status = Request_pb2.TaskStatusResponse.REJECTED
    task_response.status = Request_pb2.TaskResponse.BUSY
  current_path = os.path.dirname(os.path.realpath("__file__"))
  response_proto = os.path.join(current_path, ".\\response.pb")
  with open(response_proto, "wb") as response:
    response.write(task_status_response.SerializeToString())
    response.close()
  return send_file(response_proto)
  

if __name__ == "__main__":
  logging.basicConfig(filename="server.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s: %(message)s")
  logging.getLogger().addHandler(logging.StreamHandler())
  # APP.run(debug=True)
  serve(APP, host="127.0.0.1", port=PORT)
