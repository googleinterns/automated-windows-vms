#!/usr/bin/python
"""Script to create a proto file

  It takes input from the text in the input file
  (second argument, see usage) and creates the corresponding proto file
"""
import sys
from google.protobuf import text_format
import Request_pb2


if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "INPUT_REQUEST_TEXT_FILE")
    sys.exit(-1)
  TEXT_FILE = open(sys.argv[1], 'r')
  TASK_REQUEST = Request_pb2.TaskRequest()
  text_format.Parse(TEXT_FILE.read(), TASK_REQUEST)
  TEXT_FILE.close()
  print(TASK_REQUEST)
  with open("input_request.pb", "wb") as input_request:
    input_request.write(TASK_REQUEST.SerializeToString())
    input_request.close()
