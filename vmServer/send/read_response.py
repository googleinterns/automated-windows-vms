#! /usr/bin/python
import Request_pb2
import sys

def list_proto_file(task_request):
  """Iterates though all people in the Task_Request proto file and prints info about
  them."""
  #TODO print the fields here
  pass

def print_protocol_buffer(filename):
    task_request = Request_pb2.TaskRequest()
    with open(sys.argv[1], "rb") as f:
        task_request.ParseFromString(f.read())
    print(task_request)

if __name__ == '__main__':
  # Main procedure:  Reads the entire Task Request file from a file and prints all
  # the information inside.
  if len(sys.argv) != 2:
    print ("Usage:", sys.argv[0], "INPUT_REQUEST_FILE")
    sys.exit(-1)
  task_request = Request_pb2.TaskResponse()
  # Read the existing task request.
  with open(sys.argv[1], "rb") as f:
      task_request.ParseFromString(f.read())
  # list_proto_file(task_request)
  print(task_request)
