#!/usr/bin/python
"""Program to check the value of an environment variable
"""
import logging
import os


if os.environ["MOCHA"] == "Automation":
  print("Environment variable has been set")
  with open(".\\output\\output.txt", "w+") as output_file:
    output_file.write(os.environ["MOCHA"])
    output_file.close()
else:
  raise KeyError()
if os.environ["INTERNSHIP"] == "Extended":
  print("Environment variable has been set")
  with open(".\\output\\output.txt", "a") as output_file:
    output_file.write(os.environ["INTERNSHIP"])
    output_file.close()
else:
  raise KeyError()
