import os
import threading
import sys
port = int(sys.argv[1])

def new_dummy_server():
  global port
  port = port + 1
  os.system('python dummy_vm_server.py ' + str(port))
def master_server():
  os.system('python master_server.py')
if __name__ == '__main__':
#  t = threading.Thread(target = master_server)
#  t.start()
  count = int(sys.argv[2])
  for i in range(count):
    t = threading.Thread(target = new_dummy_server)
    t.start()
  
