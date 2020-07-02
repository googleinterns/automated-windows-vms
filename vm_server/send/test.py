#!/usr/bin/python
"""Script to create the protofile

    It compiles the proto definition and
    then creates the proto file from the text specified
    in query1.txt or query2.txt
"""
import logging
import os
import sys
import requests


URL = "http://127.0.0.1:5000/load"
ROOT = ".\\"

def usage_message():
  """Prints the valid usage details"""
  print("Usage:", sys.argv[0], "TEST_FLAG")
  print("TEST_FLAG : Test description")
  print("--all : Run all tests at once")
  print("--1 : Run query1.txt test")
  print("--2 : Run query2.txt test")
  print("--3 : Run query3.txt test")
  logging.debug("Usage:", sys.argv[0], "TEST_FLAG")

def execute_commands(proto_text_number):
  """Executes commands to compile and create a proto file

  Args:
    proto_text_number: File number of the text file from where 
    the input information for the proto request is read.
    For example, query1.txt, query2.txt etc
  """
  file_name = "query" + str(proto_text_number) + ".txt"
  print("Executing " + file_name + " test")
  logging.debug("Executing" + file_name + "test")
  logging.debug("Creating proto file from" + file_name)
  os.system("python .\\proto\\create_proto.py .\\proto\\" + file_name)
  with open(ROOT + "input_request.pb", "rb") as input_request:
    response = requests.post(url=URL, files={"task_request": input_request})
  print(type(response))
  print(response.content)
  logging.debug(type(response))
  logging.debug(str(response.content))
  if os.path.exists(ROOT + "response.pb"):
    os.remove(ROOT + "response.pb")
  with open(ROOT + "response.pb", "wb") as f:
    f.write(response.content)
    f.close()

if __name__ == "__main__":
  logging.basicConfig(filename = "response.log", level = logging.DEBUG)
  if len(sys.argv) != 2:
    usage_message()
    sys.exit(-1)
  if sys.argv[1] == "--all":
    for file_id in range(1,4):
      try:
        execute_commands(file_id)
      except Exception as err:
        print(err)
        logging.debug(err)
        sys.exit(-1)
      print("Test " + str(file_id) + " successfully passed")
      logging.debug("Test " + str(file_id) + " successfully passed")
  elif sys.argv[1] == "--1":
    file_id = 1
    try:
        execute_commands(file_id)
    except Exception as err:
      print(err)
      logging.debug(err)
      sys.exit(-1)
    print("Test " + str(file_id) + " successfully passed")
    logging.debug("Test "+ str(file_id) +" successfully passed")
  elif sys.argv[1] == "--2":
    file_id = 2
    try:
        execute_commands(file_id)
    except Exception as err:
      print(err)
      logging.debug(err)
      sys.exit(-1)
    print("Test " + str(file_id) + " successfully passed")
    logging.debug("Test "+ str(file_id) +" successfully passed")
  elif sys.argv[1] == "--3":
    file_id = 3
    try:
        execute_commands(file_id)
    except Exception as err:
      print(err)
      logging.debug(err)
      sys.exit(-1)
    print("Test " + str(file_id) + " successfully passed")
    logging.debug("Test "+ str(file_id) +" successfully passed")
  else:
    usage_message()
    sys.exit(-1)
  print("All tests successfully passed")
  logging.debug("All tests successfully passed")
