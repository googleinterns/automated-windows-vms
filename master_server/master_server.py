"""This script works on the asssumption of a certain directory structure.
     It then acts the master server and load balances the incoming
     requests.
     A database is created to store the incoming requests from user.
"""
import os
import requests
from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import Request_pb2

class MyFlaskApp(Flask):
  """This class configures the flask APP and executes function
    pre_task before starting flask server.

  """
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        pre_tasks()
    super(MyFlaskApp, self).run(
        host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

APP = MyFlaskApp(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.DB'
DB = SQLAlchemy(APP)


working_vm_address_list = []
available_vm_address_list = []

class Newrequestentry(DB.Model):
  """This class creates a table Newrequestentry

    init function in this class inserts a new row
    the table.
  """
  request_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
  request_proto_file = DB.Column(DB.BLOB)
  response_proto_file = DB.Column(DB.BLOB)

  request_status = DB.Column(DB.String(50))
  last_vm_assigned = DB.Column(DB.String(100))
  number_of_retries_allowed = DB.Column(DB.Integer)
  number_of_retries_till_now = DB.Column(DB.Integer)

  datetime_of_accepting_request = DB.Column(DB.DateTime, default=datetime.now())

  def __init__(
      self, request_proto_file, request_status, last_vm_assigned,
      number_of_retries_allowed, number_of_retries_till_now):
    self.request_proto_file = request_proto_file

    self.request_status = request_status
    self.last_vm_assigned = last_vm_assigned
    self.number_of_retries_allowed = number_of_retries_allowed
    self.number_of_retries_till_now = number_of_retries_till_now

def create_new_request(

    request_proto_file, request_status, last_vm_assigned,
    number_of_retries_allowed, number_of_retries_till_now):
#  This function adds a new row to database.
  dessert = Newrequestentry(
      request_proto_file, request_status, last_vm_assigned,
      number_of_retries_allowed, number_of_retries_till_now)

  DB.session.add(dessert)
  DB.session.commit()
  return dessert

def get_status(request_id):
#  Get status of previous request.
  get_row_data = Newrequestentry.query.get(request_id)
  return get_row_data


def change_state(request_id, input_file):
#  Change request_status of a request.
  Newrequestentry.query.filter_by(request_id=request_id).\
  update({Newrequestentry.response_proto_file: input_file})
  DB.session.commit()

def change_state_again(request_id, last_vm_assigned,
      number_of_retries_till_now):
#  Change request_status of a request.
  
  Newrequestentry.query.filter_by(request_id=request_id).\
  update({Newrequestentry.last_vm_assigned: last_vm_assigned, Newrequestentry.\
      number_of_retries_till_now: number_of_retries_till_now})

  DB.session.commit()

@APP.route('/', methods=['GET', 'POST'])
def hello_world():

  return(' You have reached master server \n')

@APP.route('/register', methods=['GET', 'POST'])
def add_vm_address():
#  Add a VM to working_vm_address_list list.

  address = request.data.decode('utf-8')
  if address not in working_vm_address_list:
    working_vm_address_list.append(address)
  return {'message': 'success'}

@APP.route('/upload')

def upload_file_webpage():

#  Serve web page
  return render_template('upload.html')

@APP.route('/uploader', methods=['GET', 'POST'])

def upload_file():
  """Accept proto file from user and
     assign it to VM.
  """

  f = request.files['file']
  read = f.read()
  vm_n = find_working_vm()
  if vm_n == 'NOT':
    return 'try again later'
  else:
    try:
      working_vm_address_list.remove(vm_n)
      task_request = Request_pb2.TaskRequest()
      task_request.ParseFromString(read)
      requ = create_new_request(

          read, 'accepted', vm_n, task_request. number_of_retries, 0)
      task_request.request_id = requ.request_id
      response = requests.post(url=vm_n, files={'task_request':
          task_request.SerializeToString()})
      return 'file uploaded successfully,your request_id is '+ \
          str(requ.request_id)+'  ' + ' address is ' + str(requ.last_vm_assigned)+ \

          ' number of retries allowed is ' + str(requ.number_of_retries_allowed)
    except:
      return 'try again later'

@APP.route('/vm_status', methods=['GET', 'POST'])

def vm_status():

#  Return VM address which are active.
  return str(working_vm_address_list)

@APP.route('/success', methods=['GET', 'POST'])
def task_completed():

#  Receive response from vm_server.
  input_file = request.files['task_response']
  req = request.files['request_id'].read()
  task_response = Request_pb2.TaskResponse()
  task_response.ParseFromString(input_file.read())
  request_id = int(req.decode('utf-8'))
  change_state(int(request_id), task_response.SerializeToString())
  if task_response.status == 2:
    result = retry_again(request_id)

  return 'success'

@APP.route('/request_status', methods=['GET', 'POST'])
def status_of_request():
#  Check status of a request
  req_id = request.form['request_id']
  request_row = get_status(req_id)
  if request_row is None:
    return 'invalid request'
  else:

    a = request_row.response_proto_file
    if a is None:
      return 'request pending'
    else:
      task_response = Request_pb2.TaskResponse()
      task_response.ParseFromString(request_row.response_proto_file)
      return str(task_response)

def retry_again(request_id):
#  Retry again if request fails.
  
  request_row = get_status(request_id)
  if request_row.number_of_retries_allowed > request_row.number_of_retries_till_now:
    vm_n = find_working_vm()
    if vm_n == 'NOT':
      return 'try again later'
    else:
      try:
        task_request = Request_pb2.TaskRequest()
        task_request.ParseFromString(request_row.request_proto_file)
        task_request.request_id = request_id
        working_vm_address_list.remove(vm_n)
        response = requests.post(url=vm_n, files={'task_request':
             task_request.SerializeToString()})
        change_state_again(request_id, vm_n, request_row.number_of_retries_till_now+1)
        return 'success'
      except:
        return 'try again later'


def is_healthy(node):
  """Check given VM is healthy or not.
     Args:
       node:
  """
  try:

    req = requests.get(node+str('/active'))

    return True
  except:
    return False

def is_engaged(node):
  """Check whether given VM is engaged in any
     task or not.
     Args:
       node:
  """
  if is_healthy(node):
    try:

      req = requests.get(node+str('/status'))

      a = req.json()
      return bool(a['status'])
    except:
      return False
  return False

def find_working_vm():

#  Find working VM address.

  for address in working_vm_address_list:
    if not is_engaged(address):
      return address
  return 'NOT'

def get_working_vm_address():

#   Append IP addresses of working VMs to a list.

  for address in available_vm_address_list:
    if is_healthy(address) and not is_engaged(address):
      working_vm_address_list.append(address)

def get_available_vm_address():
  """Append IP addresses of available VMs to a list.

     It assumes IP addresses are present in a text file.

  """
  with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
      new_address = line[:-1]
      available_vm_address_list.append(new_address)

def pre_tasks():

#   Tasks to do before flask server starts.

  DB.create_all()
  get_available_vm_address()
  get_working_vm_address()

if __name__ == '__main__':
  APP.run()
