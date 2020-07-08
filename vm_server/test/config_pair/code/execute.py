#!/usr/bin/python
"""Program to check the value of an environment variable
"""
import os


if os.environ["MOCHA"] == "Automation":
  print("Environment variable has been set")
else:
  raise KeyError()
if os.environ["INTERNSHIP"] == "Extended":
  print("Environment variable has been set")
else:
  raise KeyError()
