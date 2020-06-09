#!/usr/bin/python
"""This is the flask server of the a windows VM

    It accepts the requests in the form of protobufs and executes the same in the specified path
"""
import shutil
import timeit
import os
import subprocess

from pathlib import Path
from flask import Flask, request, send_file

import repackage
repackage.up(2)
from vmServer.send.proto import Request_pb2


def make_directories(task_request):
    """Creates the directories for execution

    Args:
        task_request: TaskRequest() object that is read from the protobuf
    """
    dirpath = Path('execute')
    if dirpath.exists() and dirpath.is_dir(): # delete leftover files from previous run, if any
        shutil.rmtree(dirpath)
    current_path = 'execute\\action'
    os.mkdir('execute')
    os.mkdir(current_path)
    Path('execute\\__init__.py').touch() # __init__.py for package
    Path(current_path+"\\__init__.py").touch()
    shutil.copytree(task_request.codePath, current_path+"\\code")
    Path(current_path+"\\code\\__init__.py").touch() # __init__.py for package
    shutil.copytree(task_request.dataPath, current_path+"\\data")
    shutil.copytree(task_request.outputPath, current_path+"\\output")


def execute_action(task_request, task_response):
    """ Execute the action

    Args:
        task_request: an object of TaskResponse() that is sent in the request
        task_response: an object of TaskResponse() that will be sent back
    """
    current_path = 'execute\\action'
    try:
        execute = subprocess.Popen(['powershell.exe', current_path+task_request.targetPath], stdout=subprocess.PIPE)   #  execute the target file
        out, err = execute.communicate()
        encoding = 'utf-8'
        if out is None:
            out = "".encode(encoding)
        if err is None:
            err = "".encode(encoding)
        std_out = open(current_path+"\\output\\stdout.txt", "w")
        std_out.write(out.decode(encoding))
        std_out.close()
        std_err = open(current_path+"\\output\\stderr.txt", "w")
        std_err.write(err.decode(encoding))
        std_err.close()
    except Exception as exception:  #catch errors if any
        print(exception)
        print("FAIL")
        task_response.status = "FAILURE"
        std_err = open(current_path+"\\output\\stderr.txt", "w")
        std_err.write(str(exception))
        std_err.close()

APP = Flask(__name__)
@APP.route('/load', methods=['POST'])
def load():
    """load endpoint. Accepts post requests with protobuffer
    """
    task_request = Request_pb2.TaskRequest()
    task_request.ParseFromString(request.files['task_request'].read())
    start = timeit.default_timer()
    task_response = Request_pb2.TaskResponse()
    make_directories(task_request)
    execute_action(task_request, task_response)
    stop = timeit.default_timer()
    time_taken = stop-start
    print("Time taken is ", time_taken)
    task_response.timeTaken = time_taken
    output_files=[name for name in os.listdir(".\\execute\\action\\output\\") if os.path.isfile(".\\execute\\action\\output\\"+name)]
    task_response.numberOfFiles = len(output_files)
    if task_response.status != "FAILURE":
        task_response.status = "SUCCESS"
    with open("response.pb", "wb") as response:
        response.write(task_response.SerializeToString())
        response.close()
    return send_file("response.pb")

if __name__ == '__main__':
    APP.run(debug=True)
