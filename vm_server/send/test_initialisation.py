import sys
import threading


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
  with open(file_name, "wb") as proto_response:
    proto_response.write(str(proto_instance))
    proto_response.close()