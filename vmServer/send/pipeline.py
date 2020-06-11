#!/usr/bin/python
"""Script to create the protofile

    It compiles the proto definition and
    then creates the proto file from the text specified
    in query1.txt or query2.txt
"""
import os


os.chdir('proto')
os.system("python .\\compile_proto.py")
os.system("python .\\create_proto.py .\\query2.txt")
