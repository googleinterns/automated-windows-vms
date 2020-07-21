import time
import requests
import Request_pb2
import start_server
import pytest

list_ = []

def test_initial_task_response(start_port, count_of_vm, filename, number_of_request):
  global final_task_response
  start_port = int(start_port)
  count_of_vm = int(count_of_vm)
  number_of_request = int(number_of_request)
  result = start_server.start_server(start_port, count_of_vm, filename)
  final_task_response = result[2] 
  time.sleep(20)
  for i in range(number_of_request):
    response = requests.post(url='http://127.0.0.1:5000/assign_task',
          files={'task_request': result[0].SerializeToString()})
    initial_task_response = Request_pb2.TaskStatusResponse()
    initial_task_response.ParseFromString(response.content)
    pytest.assume(initial_task_response.status == result[1].status)
    if initial_task_response.status == result[1].status:
      list_.append(initial_task_response)


def test_final_task_response():
  time.sleep(50)
  task_status_request = Request_pb2.TaskStatusRequest()
  for task_status_response in list_:
    task_status_request.request_id = task_status_response.current_task_id
    response = requests.post(url= 'http://127.0.0.1:5000/get_status',
        files = {'task_response': task_status_request.SerializeToString()})
    final_response = Request_pb2.TaskStatusResponse()
    final_response.ParseFromString(response.content)
    flag = True
    if task_status_response.current_task_id != final_response.current_task_id:
      flag = False
    elif final_task_response.status != final_response.status or \
        final_task_response.task_response.status != final_response.task_response.status:
      flag = False
    pytest.assume(flag)
