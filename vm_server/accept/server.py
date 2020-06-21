#!/usr/bin/python
"""This is the flask server of the a windows VM

  It accepts the requests in the form of protobufs
  and executes the same in the specified path
"""
import shutil
import timeit
import os
import subprocess
import sys
from pathlib import Path
import threading
from google.cloud import storage
from flask import Flask, request, send_file
import repackage
repackage.up(2)
from vm_server.send.proto import Request_pb2

LOCAL = False
sem = threading.Semaphore()

def remove_execute_dir():
  """Deletes the execute directory if it exists
  """
  dirpath = Path("..\\execute")
  if dirpath.exists() and dirpath.is_dir(): # delete leftover files
    shutil.rmtree(dirpath)

def make_directories(task_request):
  """Creates the directories for execution

  Args:
    task_request: TaskRequest() object that is read from the protobuf
  """
  remove_execute_dir()
  current_path = "..\\execute\\action"
  os.mkdir("..\\execute")
  os.mkdir(current_path)
  Path("..\\execute\\__init__.py").touch() # __init__.py for package
  Path(current_path + "\\__init__.py").touch()
  shutil.copytree(task_request.code_path, current_path + "\\code")
  Path(current_path + "\\code\\__init__.py").touch() # __init__.py for package
  shutil.copytree(task_request.data_path, current_path + "\\data")
  shutil.copytree(task_request.output_path, current_path + "\\output")

def download_blob(bucket_name, source_blob_name, destination_file_name):
  """Downloads a blob from the bucket.

  Args:
    bucket_name: Name of the storage bucket
    source_blob_name: Path to sorage object
    destination_file_name: Lacal path where the object needs to be saved
  """
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(source_blob_name)
  blob.download_to_filename(destination_file_name)
  print(
      "Blob {} downloaded to {}.".format(
          source_blob_name, destination_file_name
      )
  )
def upload_output_files(task_request):
  """Downloads the input files from pantheon

  Args:
    task_request: TaskRequest() object that is read from the protobuf
  """
  current_path = "..\\execute\\action"
  bucket_name = "automation-interns"
  source_file_name = current_path+"\\output"
  destination_blob_name = task_request.output_path
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)
  blob.upload_from_filename(source_file_name)
  print(
      "File {} uploaded to {}.".format(
          source_file_name, destination_blob_name
      )
  )

def download_input_files(task_request):
  """Downloads the input files from pantheon

  Args:
    task_request: TaskRequest() object that is read from the protobuf
  """
  remove_execute_dir()
  current_path = "..\\execute\\action"
  os.mkdir("..\\execute")
  os.mkdir(current_path)
  Path("..\\execute\\__init__.py").touch() # __init__.py for package
  Path(current_path + "\\__init__.py").touch()
  download_blob("automation-interns", task_request.code_path,
                current_path + "\\code")
  Path(current_path + "\\code\\__init__.py").touch() # __init__.py for package
  download_blob("automation-interns", task_request.data_path,
                current_path + "\\data")
  download_blob("automation-interns", task_request.output_path,
                current_path + "\\output")

def execute_action(task_request, task_response):
  """ Execute the action

  Args:
    task_request: an object of TaskResponse() that is sent in the request
    task_response: an object of TaskResponse() that will be sent back
  """
  current_path = "..\\execute\\action"
  print(current_path + task_request.target_path)
  encoding = "utf-8"
  out = None
  err = None
  try:
    execute = subprocess.Popen(["powershell.exe", #  execute the target file
                                task_request.target_path],
                               stdout=subprocess.PIPE,
                               cwd=current_path)
    out, err = execute.communicate(timeout=task_request.timeout)
  except Exception as exception:  #catch errors if any
    print(exception)
    print("FAIL")
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
  except Exception as exception:
    print("Error writing in std out, stderr", exception)


APP = Flask(__name__)
@APP.route("/load", methods=["POST"])
def load():
  """load endpoint. Accepts post requests with protobuffer
  """
  task_response = Request_pb2.TaskResponse()
  if sem.acquire(blocking=False):
    print("Accepted request", request)
    task_request = Request_pb2.TaskRequest()
    task_request.ParseFromString(request.files["task_request"].read())
    start = timeit.default_timer()
    if LOCAL:
      make_directories(task_request)
    else:
      download_input_files(task_request)
    execute_action(task_request, task_response)
    stop = timeit.default_timer()
    time_taken = stop-start
    print("Time taken is ", time_taken)
    task_response.time_taken = time_taken
    output_files = [name for name in os.listdir("..\\execute\\action\\output\\")
                    if os.path.isfile("..\\execute\\action\\output\\" + name)]
    task_response.number_of_files = len(output_files)
    if task_response.status != Request_pb2.TaskResponse.FAILURE:
      task_response.status = Request_pb2.TaskResponse.SUCCESS
    with open("response.pb", "wb") as response:
      response.write(task_response.SerializeToString())
      response.close()
    sem.release()
  else:
    task_response.status = Request_pb2.TaskResponse.BUSY
    with open("response.pb", "wb") as response:
      response.write(task_response.SerializeToString())
      response.close()
  print(task_response.status)
  upload_output_files(task_response)
  return send_file("response.pb")

if __name__ == "__main__":
  if len(sys.argv) > 1:
    LOCAL = True
  APP.run(debug=True)
