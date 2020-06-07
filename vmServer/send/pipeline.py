#script to send the file, it does everything from compiling to sending POST request
import os
import sys

os.system('python compile_proto.py')
os.system('python create_proto.py')
os.system('python post_request.py')

