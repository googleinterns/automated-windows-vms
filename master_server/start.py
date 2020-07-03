import os
import threading
import sys
port=5000

def new_serve():
  global port
  port=port + 1
  os.system('python dummy_vm_server.py '+str(port))
def master_server():
  os.system('python master_server.py')
if __name__ == '__main__':
  t=threading.Thread(target=master_server)
  t.start()
  z=int(sys.argv[1])
  for i in range(z):
    t=threading.Thread(target=new_serve)
    t.start()
  
