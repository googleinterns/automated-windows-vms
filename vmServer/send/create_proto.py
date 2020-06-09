"""Program to puopulate the populate and create the proto file"""
#! /usr/bin/python
import sys
import Request_pb2

def prompt_for_details(task_request):
  # task_request.codePath=input("Enter the pantheon path where the code is stored: ")
  task_request.codePath="..\\test1\\code\\"
  # task_request.dataPath=input("Enter the pantheon path where the data is stored: ")
  task_request.dataPath="..\\test1\\data\\"
  # task_request.outputPath=input("Enter the pantheon path where the output will be stored: ")
  task_request.outputPath="..\\test1\\output\\"
  # task_request.targetPath =input("Enter the target path from code root that is to be executed: ")
  task_request.targetPath="..\\test1\\code\\action.ps1"
  try:
    task_request.timeout=float(input("Enter timeout in seconds (defalut value 3600s): "))
  except ValueError:
    task_request.timeout=float(3600)  #default value of timeout is 1 hour
  while True:
    action="execute_macro"
    if action=="":
      break
    if action=="execute_macro":
      macro_name="macro"
      actionPair=Request_pb2.configPair()
      actionPair.key=action
      actionPair.value=macro_name
      task_request.actionPairs.append(actionPair)
    break
    
    #TODO screenshot


if __name__ == '__main__':
  TaskRequest = Request_pb2.TaskRequest()
  prompt_for_details(TaskRequest)
  with open("input_request.pb", "wb") as f:
    f.write(TaskRequest.SerializeToString())
    f.close()
