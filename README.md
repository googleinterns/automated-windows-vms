# Automated Windows VMs

Automating tasks that require manual effort over windows machines.
### Install dependencies
* Run `pip install requirements.txt`
## Steps to run the Master server
* Change directory to 'master_server/'
* Run 'python master_server.py DEBUG_MODE'

    DEBUG_MODE = --binary if we want end to end testing, otherwise by default it looks starts in UI mode.
    
## Steps to run the dummy_vm_server
* Change directory to 'master_server/'
* Run 'python dummy_vm_server.py PORT_NO'
 
    PORT_NO is the port number on which the dummy_vm_server starts
    
## Steps to run tests on Master server
* Change directory to 'master_server/'
* Run 'python -m pytest START_PORT TEST_FOLDER COUNT_OF_VM_SERVER NUMBER_OF_TIMES_TO_SEND_REQUEST
    
    START_PORT = --start_port="port_number",port specifies the starting port of the vm server.
    
    TEST_FOLDER = --filename="folder_name",folder name which contains the test.
    
    COUNT_OF_VM_SERVER = --count_of_vm="number",number specifies the number of VM server we want.
    
    NUMBER_OF_TIMES_TO_SEND_REQUEST = --number_of_request="number",number specifies the number of times,we want to send the same request to the Master server. 
   
## Steps to run the VM server
* Change directory to `vm_server/accept/`
* Run `python server.py DEBUG_FLAG PORT_NO`
    
    DEBUG_FLAG = DEBUG if we want to run locally, otherwise by default it looks for the paths in Pantheon
    
    PORT_NO is the port number on which the VM starts
## Steps to run tests on VM server
* Change directory to `vm_server/send/`
* Run `python -m pytest`
    
**This is not an officially supported Google product.**

## Source Code Headers

Every file containing source code must include copyright and license
information. This includes any JS/CSS files that you might be serving out to
browsers. (This is to help well-intentioned people avoid accidental copying that
doesn't comply with the license.)

Apache header:

    Copyright 2020 Google LLC

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
