#!/usr/bin/python
"""Script to read the received response proto file
"""
import sys
import request_pb2


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "INPUT_REQUEST_FILE")
    sys.exit(-1)
  TASK_REQUEST = request_pb2.TaskResponse()
  with open(sys.argv[1], "rb") as f:
    TASK_REQUEST.ParseFromString(f.read())
  print(TASK_REQUEST)
