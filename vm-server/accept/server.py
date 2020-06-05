import repackage
repackage.up(2)
import http.client
import shutil
import timeit
from vm-server.send import Request_pb2
from vm-server.accept import execute
from flask import Flask, request, send_file


app = Flask(__name__)
@app.route('/load', methods=['POST'])
def load():
    task_request = Request_pb2.TaskRequest()
    task_request.ParseFromString(request.files['task_request'].read())
    f = open(".\execute\outputfile.pb", "wb")
    f.write(task_request.SerializeToString())
    f.close()
    start=timeit.default_timer()
    task_response=Request_pb2.TaskResponse()
    #execute tasks here
    actionCount=1
    #TODO
    os.mkdir('accept\execute')
    for actionPair in task_request.actionPairs:
        if actionPair.key=="execute_macro":
            currentPath='vm-server\accept\execute\action'+str(actionCount)
            os.mkdir(currentPath)
            #copy code for action from pantheon
            #TODO need to change this to actual pantheon path
            shutil.copytree('vm-server\test\code',currentPath)
            #copy data for action from pantheon
            shutil.copytree('vm-server\test\data',currentPath)
            #pantheon path where the output is stored
            shutil.copytree('vm-server\test\output',currentPath)
            execute.execute_macro(currentPath)
            
        elif actionPair.key=="screenshot":
            #TODO
            pass
        else:
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