#!/usr/bin/python
"""Program to execute a VBA macro in MS Excel
"""
import os
import shutil
import win32com.client
import pythoncom

import repackage
repackage.up()






def execute_macro(current_path):
  """Execute macro

  Args:
    current_path: path of current directory (for convenience,
    this is executed from some other directory)
  """
  pythoncom.CoInitialize()
  path_to_file = current_path+"\\data\\excelsheet.xlsm"
  if os.path.exists(path_to_file):
    xl_file = win32com.client.Dispatch("Excel.Application")
    xl_run = xl_file.Workbooks.Open(os.path.abspath(path_to_file),
                                    ReadOnly=1)
    xl_run.Application.Run("excelsheet.xlsm!main.simpleMain") #execute macro
    xl_run.Save()
    xl_run.Close()
    xl_file.Quit()
    del xl_file
    shutil.move(path_to_file, current_path+"\\output\\excelsheet.xlsm")
    print("Action successfully executed")

if __name__ == "__main__":
  CURRENT_PATH = '..\\execute\\action'
  execute_macro(CURRENT_PATH)
