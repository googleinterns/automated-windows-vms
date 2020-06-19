#!/usr/bin/python

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
import Request_pb2

class MyFlaskApp(Flask):
  """
    This class configures the flask app and executes function
    pre_task before starting flask server.
  """
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        pre_tasks()
    super(MyFlaskApp, self).run(
        host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = MyFlaskApp(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


working_vm_address_list = []
available_vm_address_list = []

class Newrequestentry(db.Model):
  """
    This class creates a table Newrequestentry
    init function in this class inserts a new row
    the table.
  """
  request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  proto_file = db.Column(db.BLOB)
  request_status = db.Column(db.String(50))
  last_vm_assigned = db.Column(db.String(100))
  number_of_retries_allowed = db.Column(db.Integer)
  number_of_retries_till_now = db.Column(db.Integer)

  def __init__(
      self, proto_file, request_status, last_vm_assigned,
      number_of_retries_allowed, number_of_retries_till_now):
    self.proto_file = proto_file
    self.request_status = request_status
    self.last_vm_assigned = last_vm_assigned
    self.number_of_retries_allowed = number_of_retries_allowed
    self.number_of_retries_till_now = number_of_retries_till_now

def create_new_request(
    proto_file, request_status, last_vm_assigned,
    number_of_retries_allowed, number_of_retries_till_now):
  """This function adds a new row to database.
  """
  dessert = Newrequestentry(
      proto_file, request_status, last_vm_assigned, number_of_retries_allowed,
      number_of_retries_till_now)
  db.session.add(dessert)
  db.session.commit()
  return dessert

def get_status(request_id):
  """Get status of previous request.
  """
  get_row_data = Newrequestentry.query.get(request_id)
  return get_row_data

def change_state(request_id):
  """Change request_status of a request.
  """
  Newrequestentry.query.filter_by(request_id=request_id).\
  update({Newrequestentry.request_status: 'completed'})
  db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
  print(' You have reached master server \n')

@app.route('/register', methods=['GET', 'POST'])
def add_vm_address():
  """Add a VM to working_vm_address_list list.
  """
  address = request.data.decode('utf-8')
  if address not in working_vm_address_list:
    working_vm_address_list.append(address)
  return {'message': 'success'}

@app.route('/upload')
def upload_file():
  """Serve web page
  """
  return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_fil():
  """
    Accept proto file from user and
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
          read, 'accepted', vm_n, task_request. numner_of_retries, 0)
      response = requests.post(url=vm_n, files={'task_request': read,\
      'request_id': ('', str(requ.request_id))})
      return 'file uploaded successfully,your request_id is '+ \
          str(requ.request_id)+'  '+' address is '+str(requ.last_vm_assigned)+ \
          ' number of retries allowed is '+str(requ.number_of_retries_allowed)
    except:
      return 'try again later'

@app.route('/vm_status', methods=['GET', 'POST'])
def upload_fi():
  """Return VM address which are active.
  """
  return str(working_vm_address_list)

@app.route('/success', methods=['GET', 'POST'])
def task_completed():
  """Completed request
  """
  request_id = request.data.decode('utf-8')
  change_state(int(request_id))
  return 'success'

@app.route('/request_status', methods=['GET', 'POST'])
def status_of_request():
  """Check status of a request
  """
  req_id = request.form['request_id']
  request_row = get_status(req_id)
  if request_row is None:
    return 'invalid request'
  else:
    return request_row.request_status

def is_healthy(node):
  """
    Check given VM is healthy or not.
    Args:
      node:
  """
  try:
    req = requests.get(node+str('/active'))
    return True
  except:
    return False

def is_engaged(node):
  """
    Check whether given VM is engaged in any
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
  """
    Find working VM address.
  """
  for address in working_vm_address_list:
    if not is_engaged(address):
      return address
  return 'NOT'

def get_working_vm_address():
  """
    Append IP addresses of working VMs to a list.
  """
  for address in available_vm_address_list:
    if is_healthy(address) and not is_engaged(address):
      working_vm_address_list.append(address)

def get_available_vm_address():
  """
    Append IP addresses of available VMs to a list.
    It assumes IP addresses are present in a text file.
  """
  with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
      new_address = line[:-1]
      available_vm_address_list.append(new_address)

def pre_tasks():
  """
    Tasks to do before flask server starts.
  """
  db.create_all()
  get_available_vm_address()
  get_working_vm_address()

if __name__ == '__main__':
  app.run()
