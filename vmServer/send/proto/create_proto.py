import Request_pb2
from google.protobuf import text_format
import sys

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print ("Usage:", sys.argv[0], "INPUT_REQUEST_TEXT_FILE")
    sys.exit(-1)
  f=open(sys.argv[1],'r')
  task_request=Request_pb2.TaskRequest()
  text_format.Parse(f.read(),task_request)
  f.close()
  print(task_request)
  with open("input_request.pb", "wb") as f:
    f.write(task_request.SerializeToString())
    f.close()

  
