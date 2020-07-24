import sys
import threading
from google.protobuf import text_format
from proto import request_pb2


class KThread(threading.Thread):
  """A subclass of threading.Thread, with a kill() method."""

  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    """Start the thread."""
    self.__run_backup = self.run
    self.run = self.__run      # Force the Thread to install our trace.
    threading.Thread.start(self)

  def __run(self):
    """Hacked run function, which installs the trace."""
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True

def save_proto_to_file(file_name, proto_instance):
  """Save the protocol buffer to a file

  Args:
    file_name: Name of the file to be created and saved.
    proto_instance: Proto instance which is going to be written to a file
  """
  with open(file_name, "w") as proto_response:
    proto_response.write(str(proto_instance))
    proto_response.close()

def compare_response(received_response, saved_response):
  """Save the protocol buffer to a file

  Args:
    received_response: Path to the received text proto.
    saved_response: Path to the saved text proto response.
  """
  received_proto = request_pb2.TaskStatusResponse()
  saved_proto = request_pb2.TaskStatusResponse()
  text_file = open(received_response, "r")
  text_format.Parse(text_file.read(), received_proto)
  text_file.close()
  text_file = open(saved_response, "r")
  text_format.Parse(text_file.read(), saved_proto)
  text_file.close()
  if received_proto.status == saved_proto.status and\
     received_proto.task_response.status == saved_proto.task_response.status:
    return True
  else:
    return False




