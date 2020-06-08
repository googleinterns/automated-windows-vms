import repackage
repackage.up(2)
import http.client
import shutil
import timeit
from vmServer.send import Request_pb2
from flask import Flask, request, send_file
import os
import io
from pathlib import Path
import importlib

app = Flask(__name__)
@app.route('/load', methods=['POST'])
def load():
    task_request = Request_pb2.TaskRequest()
    task_request.ParseFromString(request.files['task_request'].read())
    dirpath=Path('execute')
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)

    os.mkdir('execute')
    f = open(".\\execute\\outputfile.pb", "wb")
    f.write(task_request.SerializeToString())
    f.close()
    start=timeit.default_timer()
    task_response=Request_pb2.TaskResponse()
    #execute tasks here
    actionCount=1
    #TODO
    # os.mkdir('accept\execute')
    for actionPair in task_request.actionPairs:
        if actionPair.key=="execute_macro":
            currentPath='execute\\action'+str(actionCount)
            Path('execute\\__init__.py').touch()
            os.mkdir(currentPath)
            Path(currentPath+"\\__init__.py").touch()
            actionName="action"+str(actionCount)
            #copy code for action from pantheon
            #TODO need to change this to actual pantheon path
            shutil.copytree('..\\test\\code\\',currentPath+"\\code")
            Path(currentPath+"\\code\\__init__.py").touch()
            #copy data for action from pantheon
            shutil.copytree('..\\test\\data\\',currentPath+"\\data")
            Path(currentPath+"\\data\\__init__.py").touch()
            #pantheon path where the output is stored
            shutil.copytree('..\\test\\output\\',currentPath+"\\output")
            Path(currentPath+"\\output\\__init__.py").touch()
            # from vmServer.accept.execute import actionName
            code=importlib.import_module('code',package="vmServer.accept.execute."+actionName)
            # from code import execute
            # code.execute.execute_macro(currentPath)
            execute=__import__("vmServer.accept.execute."+actionName,globals(),locals(),['code','data','output'])
            # execute.code.execute.execute_macro(currentPath)
            execute_=__import__("vmServer.accept.execute."+actionName+".code",globals(),locals(),['execute'])
            print("calling")
            execute_.execute.execute_macro(currentPath)
            print("called")
            # execute.execute_macro(currentPath)
            
        elif actionPair.key=="screenshot":
            #TODO
            pass
        else:
            pass
            #TODO handle this, this might me user specified action
        actionCount=actionCount+1
    os.remove('execute')
    stop=timeit.default_timer()
    timeTaken=stop-start
    print("Time taken is ",timeTaken)
    task_response.timeTaken=timeTaken
    with open("response.pb","wb") as f:
        f.write(task_response.SerializeToString())
        f.close()
    return send_file("respons.pb")
    


if __name__=='__main__':
    app.run(debug=True)






















if __name__=='__main__':
    app.run(debug=True)