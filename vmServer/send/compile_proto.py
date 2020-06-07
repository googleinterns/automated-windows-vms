"""Script to compile the proto file"""
import os
os.system(' protoc  --python_out=.\ .\Request.proto')
