#!/usr/bin/python
"""Script to create the protofile

    It compiles the proto definition and
    then creates the proto file from the text specified
    in query1.txt or query2.txt
"""
import os
import sys

def execute_commands():
  """Executes commands to compile and create a proto file"""
  os.chdir("proto")
  os.system("protoc  --python_out=.\\ .\\Request.proto")
  os.system("python .\\create_proto.py .\\" + sys.argv[1])

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "QUERY_TEXT_FILE")
    sys.exit(-1)
  execute_commands()
