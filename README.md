# Automated Windows VMs

Automating tasks that require manual effort over windows machines.
### Install dependencies
* Run `pip install requirements.txt`
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
