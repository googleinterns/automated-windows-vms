import test


def test_execute_macro():
  execute = test.execute_commands(1)
  assert execute == True

def test_screenshot():
  execute = test.execute_commands(2)
  assert execute == True

def test_timeout():
  execute = test.execute_commands(3)
  assert execute == False

def test_config_pair():
  execute = test.execute_commands(4)
  assert execute == True


