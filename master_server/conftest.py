"""Add custom flags to pytest."""
import pytest

def pytest_addoption(parser):
  parser.addoption("--start_port", action="store", help="Start port of VM server")
  parser.addoption("--count_of_vm", action="store", help="Number of VM server")
  parser.addoption("--filename", action="store", help="Name of test folder")
  parser.addoption("--number_of_request", action="store", help="Number of request per test case")
  

@pytest.fixture
def start_port(request):
    return request.config.getoption("--start_port")

@pytest.fixture
def count_of_vm(request):
    return request.config.getoption("--count_of_vm")
    
@pytest.fixture
def filename(request):
    return request.config.getoption("--filename")

@pytest.fixture
def number_of_request(request):
    return request.config.getoption("--number_of_request")
