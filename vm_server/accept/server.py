#!/usr/bin/python
"""This is the flask server of the a windows VM

  It accepts the requests in the form of protobufs
  and executes the same in the specified path
"""
import argparse
import logging
import os
from pathlib import Path
import shutil
import subprocess
import threading
import timeit
import sys
import requests
from waitress import serve
from flask import Flask, request
from google.cloud import storage
import repackage
repackage.up(2)
from vm_server.send.proto import request_pb2

sem = threading.Semaphore()
MASTER_SERVER = "http://127.0.0.1:5000"
task_status_response = request_pb2.TaskStatusResponse()
PORT = 8000
VM_ADDRESS = "127.0.0.1"
EXECUTE_DIR = "..\\execute"
EXECUTE_ACTION_DIR = "..\\execute\\action"
OUTPUT_DIR = "\\output\\"
BUCKET_NAME = "automation-interns"
DEBUG_FLAG = "DEBUG"
parser = argparse.ArgumentParser(description="VM Server")
parser.add_argument("debug_flag",
                    type=str,
                    help="""Usage: " + sys.argv[0] +  DEBUG_FLAG + PORT"""
                    )
parser.add_argument("port",
                    type=int,
                    help="""Usage: " + sys.argv[0] +  DEBUG_FLAG + PORT"""
                    )
arguments = parser.parse_args()

def get_processes(file_name):
  """Logs the current running processes in the file named file_name

  Args:
    file_name: Name of the file where the names of the processes are saved
  """
  logging.debug("Getting the list of processes")
  get_process = subprocess.Popen("powershell.exe \
                                  Get-Process >{file}".format(file=file_name))
  get_process.communicate()

def get_diff_processes():
  """Prints the difference in processes before and
     after execution of a request
  """
  logging.debug("Getting the diff of the processes")
  compare_process = subprocess.Popen("powershell.exe Compare-Object \
                                      (Get-Content process_before.txt)\
                                      (Get-Content process_after.txt)")
  compare_process.communicate()

def remove_execute_dir(task_request, task_response):

  """Deletes the execute directory if it exists

  Args:
    task_request: TaskRequest() object that is read from the protobuf
    task_response: an object of TaskResponse() that will be sent back
  """
  logging.debug("Removing execute directory")
  dirpath = Path(EXECUTE_ACTION_DIR + "_" + str(task_request.request_id))
  print("Dirpath is ", dirpath)
  try:
    if dirpath.exists() and dirpath.is_dir(): # delete leftover files
      shutil.rmtree(dirpath)
  except Exception as exception:  # catch errors if any
    logging.exception(str(exception))
    logging.debug("Error deleting the execute directory")
    task_response.status = request_pb2.TaskResponse.FAILURE

def make_directories(task_request, task_response):
  """Creates the directories for execution

  Args:
    task_request: TaskRequest() object that is read from the protobuf
    task_response: an object of TaskResponse() that will be sent back
  """
  logging.debug("Creating execute directory structure")
  remove_execute_dir(task_request, task_response)
  if task_response.status == request_pb2.TaskResponse.FAILURE:
    return
  current_path = EXECUTE_ACTION_DIR + "_" + str(task_request.request_id)
  os.makedirs(EXECUTE_DIR, exist_ok=True)
  os.mkdir(current_path)
  os.mkdir(current_path + OUTPUT_DIR)
  Path(EXECUTE_DIR + "\\__init__.py").touch() # __init__.py for package
  Path(current_path + "\\__init__.py").touch()
  try:
    shutil.copytree(task_request.code_path, current_path + "\\code")
    Path(current_path + "\\code\\__init__.py").touch() # __init__.py for package
    data_path = Path(task_request.data_path)
    if data_path.exists() is False:
      os.mkdir(data_path)
    shutil.copytree(task_request.data_path, current_path + "\\data")
  except Exception as exception:  # catch errors if any
    logging.exception(str(exception))
    logging.debug("Error copying code and data directories")
    task_response.status = request_pb2.TaskResponse.FAILURE

def move_output(task_request, task_response):
  """Move the genrated output files to the output path specified

  Args:
    task_request: an object of TaskResponse() that is sent in the request
    task_response: an object of TaskResponse() that will be sent back
  """
  logging.debug("Moving the output path to the specified output path")
  current_path = os.getcwd()
  source_path = Path(current_path + "\\" + EXECUTE_ACTION_DIR + "_" + str(task_request.request_id) + OUTPUT_DIR)
  if source_path.exists() is False:
    os.mkdir(source_path)
  destination_path = Path(current_path + "\\" + task_request.output_path)
  if destination_path.exists() is False:
    os.mkdir(destination_path)
  files = os.listdir(source_path)
  try:
    for file in files:
      shutil.move(os.path.join(source_path, file),
                  os.path.join(destination_path, file))
  except Exception as exception:  # catch errors if any
    logging.exception(str(exception))
    logging.debug("Error moving the output \
                   files to the specified output directory")
    task_response.status = Request_pb2.TaskResponse.FAILURE

def download_files_to_path(pantheon_path, destination_path, task_response):
  """Downloads files from pantheon path to the destination path

  Args:
    pantheon_path: the source path in pantheon
    destination_path: the destination path where files are saved in the VM
    task_response: an object of TaskResponse() that will be sent back
  """
  bucket_name = BUCKET_NAME
  storage_client = storage.Client()
  blobs = storage_client.list_blobs(bucket_name, prefix=pantheon_path)
  for blob in blobs:
    source = Path(blob.name)
    destination_file_path = Path(str(destination_path) \
                                 + "\\" + str(source.name))
    if blob.name[len(blob.name)-1] == '/':
      logging.debug("Making directory Destination path : ", destination_path)
      os.makedirs(destination_file_path, exist_ok=True)
    else:
      logging.debug("Downloading file Destination path : ", destination_path)
      os.makedirs(destination_path, exist_ok=True)
      source = Path(blob.name)
      logging.debug("Destination file path: ", destination_file_path)
      try:
        blob.download_to_filename(destination_file_path)
      except Exception as exception:
        logging.debug("Error while downloading files, \
                       Exception: %s", str(exception))
        task_response.status = Request_pb2.TaskResponse.FAILURE

def download_input_files(task_request, task_response):
  """Downloads the input files from pantheon

  Args:
    task_request: TaskRequest() object that is read from the protobuf
    task_response: an object of TaskResponse() that will be sent back
  """
  remove_execute_dir(task_request, task_response)
  current_path = EXECUTE_ACTION_DIR + "_" + task_request.request_id
  os.mkdir(current_path)
  os.mkdir(current_path + OUTPUT_DIR)
  Path(current_path + "\\__init__.py").touch()
  download_files_to_path(task_request.code_path,
                         current_path + "\\code", task_response)
  download_files_to_path(task_request.data_path,
                         current_path + "\\data", task_response)


def upload_output(task_request, task_response):
  """ Upload the output files to pantheon

  Args:
    task_request: an object of TaskResponse() that is sent in the request
    task_response: an object of TaskResponse() that will be sent back
  """
  bucket_name = BUCKET_NAME
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  source_path = Path(EXECUTE_ACTION_DIR + "_" + str(task_request.request_id) + OUTPUT_DIR)
  destination_path = task_request.output_path
  files = os.listdir(source_path)
  try:
    for file in files:
      destination_blob_path = (destination_path + file)
      blob = bucket.blob(destination_blob_path)
      blob.upload_from_filename(str(source_path) + "/" + str(file))
  except Exception as exception:
    logging.debug("Error while uploading output files, \
                   Exception: %s", str(exception))
    task_response.status = Request_pb2.TaskResponse.FAILURE


def execute_action(task_request, task_response):
  """ Execute the action

  Args:
    task_request: an object of TaskResponse() that is sent in the request
    task_response: an object of TaskResponse() that will be sent back
  """
  if task_response.status == request_pb2.TaskResponse.FAILURE:
    return
  logging.debug("Trying to execute the action")
  current_path = "..\\execute\\action" + "_" + str(task_request.request_id)
  logging.debug("Action path is: %s",
                str(current_path + task_request.target_path))
  encoding = "utf-8"
  out = None
  err = None
  status = None
  try:
    execute = subprocess.Popen(["powershell.exe", # execute the target file
                                task_request.target_path],
                               stdout=subprocess.PIPE,
                               cwd=current_path)
    out, err = execute.communicate(timeout=task_request.timeout)
  except Exception as exception:  # catch errors if any
    logging.debug(str(exception))
    logging.debug("FAILED TO EXECUTE THE ACTION")
    task_response.status = request_pb2.TaskResponse.FAILURE
    err = str(exception).encode(encoding)
  status = execute.returncode
  if status:
    logging.debug("Execution was unsuccessful")
    task_response.status = request_pb2.TaskResponse.FAILURE
  logging.debug("Process is running, force killing the process")
  kill_process = subprocess.Popen("TASKKILL /F \
                                  /PID {pid} /T".format(pid=execute.pid))
  kill_process.communicate()
  if out is None:
    out = "".encode(encoding)
  if err is None:
    err = "".encode(encoding)
  try:
    std_out = open(current_path + OUTPUT_DIR + "stdout.txt", "w")
    std_out.write(out.decode(encoding))
    std_out.close()
    std_err = open(current_path + OUTPUT_DIR + "stderr.txt", "w")
    std_err.write(err.decode(encoding))
    std_err.close()
    output_files = [name for name in os.listdir(current_path + OUTPUT_DIR)
                    if os.path.isfile(current_path + OUTPUT_DIR + name)]
    task_response.number_of_files = len(output_files)
    if arguments.debug_flag == DEBUG_FLAG:
      move_output(task_request, task_response)
    else:
      upload_output(task_request, task_response)
  except Exception as exception:
    logging.debug("Error writing in stdout, stderr %s", str(exception))
    task_response.status = request_pb2.TaskResponse.FAILURE

def register_vm_address():
  """Send request to master server to inform that VM is free"""
  data = "http://{}:{}".format(VM_ADDRESS, str(PORT))
  try:
    requests.get(MASTER_SERVER + str("/register"), data=data)
  except Exception as exception:
    logging.debug(str(exception))
    logging.debug("Can't connect to the master server")

def task_completed(task_request, task_response):
  """Send response to the master server when the task has been executed

  Args:
    task_request: TaskRequest() object that is read from the protobuf
    task_response: an object of TaskResponse() that will be sent back
  """
  global task_status_response
  if task_response.status != request_pb2.TaskResponse.FAILURE:
    task_response.status = request_pb2.TaskResponse.SUCCESS
  task_status_response.task_response.CopyFrom(task_response)
  current_path = os.path.dirname(os.path.realpath("__file__"))
  response_proto = os.path.join(current_path, ".\\task_completed_response.pb")
  with open(response_proto, "wb") as status_response:
    status_response.write(task_status_response.SerializeToString())
    status_response.close()
  remove_execute_dir(task_request, task_response)
  logging.debug("Response Proto: %s", str(task_response))
  # get_processes("process_after.txt")
  # get_diff_processes()
  with open(response_proto, "rb") as status_response:
    try:
      requests.post(url=MASTER_SERVER + "/success",
                    files={"task_response": task_status_response.SerializeToString()})
    except Exception as exception:
      logging.debug(str(exception))
      logging.debug("Can't connect to the master server")
    status_response.close()
  logging.debug("Releasing semaphore")
  sem.release()

def set_environment_variables(task_request):
  """Set the environment variables in config pair

  Args:
    task_request: an object of TaskResponse() that is sent in the request
  """
  for config_pair in task_request.config_pairs:
    os.environ[config_pair.key] = config_pair.value

def execute_wrapper(task_request, task_response):
  """Execute the tasks in the request

  Args:
    task_request: an object of TaskResponse() that is sent in the request
    task_response: an object of TaskResponse() that will be sent back
  """
  global task_status_response
  start = timeit.default_timer()
  set_environment_variables(task_request)
  if arguments.debug_flag == DEBUG_FLAG:
    make_directories(task_request, task_response)
  else:
    download_input_files(task_request, task_response)
  execute_action(task_request, task_response)
  stop = timeit.default_timer()
  time_taken = stop-start
  logging.debug("Time taken is %s", str(time_taken))
  task_response.time_taken = time_taken
  task_status_response.status = request_pb2.TaskStatusResponse.COMPLETED
  task_completed(task_request, task_response)
  register_vm_address()


APP = Flask(__name__)

@APP.route("/get_status", methods=["POST"])
def get_status():
  """Endpoint for the master to know the status of the VM"""
  global task_status_response
  request_task_status_response = request_pb2.TaskStatusResponse()
  request_task_status_response.ParseFromString(
      request.files["task_request"].read()
  )
  response_task_status = task_status_response
  if task_status_response.current_task_id != \
     request_task_status_response.current_task_id:
    response_task_status.status = request_pb2.TaskStatusResponse.INVALID_ID
  return response_task_status.SerializeToString()

@APP.route("/assign_task", methods=["POST"])
def assign_task():
  """Endpoint to accept post requests with protobuffer"""
  task_response = request_pb2.TaskResponse()
  global task_status_response
  # get_processes("process_before.txt")
  if sem.acquire(blocking=False):
    logging.debug("Accepted request: %s", str(request))
    task_request = request_pb2.TaskRequest()
    task_request.ParseFromString(request.files["task_request"].read())
    logging.debug("Request Proto: %s", str(task_request))
    thread = threading.Thread(target=execute_wrapper,
                              args=(task_request, task_response,))
    thread.start()
    task_status_response = request_pb2.TaskStatusResponse()
    task_status_response.current_task_id = task_request.request_id
    task_status_response.status = request_pb2.TaskStatusResponse.ACCEPTED
  else:
    task_status_response.status = request_pb2.TaskStatusResponse.REJECTED
    # task_response.status = request_pb2.TaskResponse.BUSY
  current_path = os.path.dirname(os.path.realpath("__file__"))
  response_proto = os.path.join(current_path, ".\\response.pb")
  logging.debug("Task Status Response: %s", str(task_status_response))
  with open(response_proto, "wb") as response:
    response.write(task_status_response.SerializeToString())
    response.close()
  task_request = request_pb2.TaskRequest()
  task_request.ParseFromString(request.files["task_request"].read())
  return task_status_response.SerializeToString()

@APP.route('/active', methods=['GET', 'POST'])
def is_active():
#  Master can check here if VM is active or not.
  return "Hello World"
  
@APP.route('/status', methods=['GET', 'POST'])
def flag_status():
#  Returns the state of VM
  return "False"

if __name__ == "__main__":
  logging.basicConfig(filename="server.log",
                      level=logging.DEBUG,
                      format="%(asctime)s:%(levelname)s: %(message)s")
  logging.getLogger().addHandler(logging.StreamHandler())
  # APP.run(debug=True)
  PORT = sys.argv[2]
  register_vm_address()
  serve(APP, host="127.0.0.1", port=PORT)
