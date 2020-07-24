#!/usr/bin/python
"""This is the program to run tests on the VM server

  The functions in this file are automatically collected by
  pytest and run
"""
import os
import filecmp
from pathlib import Path
from google.cloud import storage
import test_server

BUCKET_NAME = "automation-interns"


def test_execute_macro():
  """Test the execute macro action"""
  test_server.execute_commands(1)
  output_path = "..\\test\\execute_macro\\output\\output.txt"
  expected_output_path = "..\\test\\execute_macro\\expected_output\\expected_output.txt"
  assert filecmp.cmp(output_path, expected_output_path)

def test_screenshot():
  """Test the word screenshot action"""
  execute = test_server.execute_commands(2)
  assert execute

def test_timeout():
  """Test the failure due to timeout action"""
  execute = test_server.execute_commands(3)
  assert execute is False

def test_config_pair():
  """Test if config pairs are being set"""
  test_server.execute_commands(4)
  output_path = "..\\test\\config_pair\\output\\output.txt"
  expected_output_path = "..\\test\\config_pair\\expected_output\\expected_output.txt"
  assert filecmp.cmp(output_path, expected_output_path)

def test_time_out_multiple_times():
  """Test failure due to time out multiple times"""
  for _ in range(3):
    execute = test_server.execute_commands(3)
    assert execute is False

def download_files_to_path(pantheon_path, destination_path):
  """Downloads files from pantheon path to the destination path

  Args:
    pantheon_path: the source path in pantheon
    destination_path: the destination path where files are saved in the VM
  """
  bucket_name = BUCKET_NAME
  storage_client = storage.Client()
  blobs = storage_client.list_blobs(bucket_name, prefix=pantheon_path)
  for blob in blobs:
    source = Path(blob.name)
    destination_file_path = Path(str(destination_path) \
                                 + "\\" + str(source.name))
    if blob.name[len(blob.name)-1] == '/':
      print("Making directory Destination path : ", destination_path)
      os.makedirs(destination_file_path, exist_ok=True)
    else:
      print("Downloading file Destination path : ", destination_path)
      os.makedirs(destination_path, exist_ok=True)
      source = Path(blob.name)
      print("Destination file path: ", destination_file_path)
      blob.download_to_filename(destination_file_path)

# def test_pantheon_config_pair():
#   """Test config pair from pantheon"""
#   test_server.execute_commands(5)
#   pantheon_path = "test/config_pair/expected_output/"
#   destination_path = ".\\"
#   download_files_to_path(pantheon_path, destination_path)
#   pantheon_path = "test/config_pair/output/"
#   download_files_to_path(pantheon_path, destination_path)
#   output_path = ".\\output.txt"
#   expected_output_path = ".\\expected_output.txt"
#   assert filecmp.cmp(output_path, expected_output_path)
