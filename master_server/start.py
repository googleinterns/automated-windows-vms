"""Python script to bring up the Master server.
   And VM servers on the specified ports."""
import os
import threading
import sys
import time
if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], 'INPUT_PORT', 'COUNT_OF_VMs')
    sys.exit(-1)

port = int(sys.argv[1])
def new_dummy_server():
  """Start a new dummy server of specified port."""
  global port
  port = port + 1
  os.system('python dummy_vm_server.py ' + str(port))

def master_server():
  """Start Master server on default port 5000."""
  os.system('python master_server.py')

if __name__ == '__main__':
  process = threading.Thread(target = master_server)
  process.start()
  time.sleep(5)
  count = int(sys.argv[2])
  for i in range(count):
    time.sleep(2)
    process = threading.Thread(target = new_dummy_server)
    process.start()
  
