import test_server
import filecmp


# def test_execute_macro():
#   """Test the execute macro action"""
#   execute = test_server.execute_commands(1)
#   output_path = "..\\test\\execute_macro\\output\\output.txt"
#   expected_output_path = "..\\test\\execute_macro\\expected_output\\expected_output.txt"
#   assert filecmp.cmp(output_path, expected_output_path)

# def test_screenshot():
#   """Test the word screenshot action"""
#   execute = test_server.execute_commands(2)
#   assert execute == True

# def test_timeout():
#   """Test the failure due to timeout action"""
#   execute = test_server.execute_commands(3)
#   assert execute == False

# def test_config_pair():
#   """Test if config pairs are being set"""
#   execute = test_server.execute_commands(4)
#   output_path = "..\\test\\config_pair\\output\\output.txt"
#   expected_output_path = "..\\test\\config_pair\\expected_output\\expected_output.txt"
#   assert filecmp.cmp(output_path, expected_output_path)

# def test_time_out_multiple_times():
#   """Test failure due to time out multiple times""" 
#   for i in range(3):
#     execute = test_server.execute_commands(3)
#     assert execute == False

def test_pantheon_config_pair():
  """Test config pair from pantheon"""
  execute = test_server.execute_commands(5)
  assert execute == True