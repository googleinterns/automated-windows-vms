#!/usr/bin/python
"""Script to create the protofile

    It compiles the proto definition and
    then creates the proto file from the text specified
    in query1.txt, query2.txt etc
"""
import logging
import os
import sys

def compile_proto():
  """Executes commands to compile a proto file"""
  logging.debug("Compile proto")
  os.system("protoc  --python_out=.\\ .\\proto\\request.proto")

def create_proto():
  """Executes commands to create a proto file"""
  logging.debug("Creating proto file from %s", sys.argv[1])
  os.system("python .\\proto\\create_proto.py .\\proto\\%s", sys.argv[1])

if __name__ == "__main__":
  logging.basicConfig(filename="response.log",
                      level=logging.DEBUG,
                      format="%(asctime)s:%(levelname)s: %(message)s")
  logging.getLogger().addHandler(logging.StreamHandler())
  if len(sys.argv) != 2:
    logging.debug("Usage: %s QUERY_TEXT_FILE", sys.argv[0])
    sys.exit(-1)
  compile_proto()
  create_proto()
