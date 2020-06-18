#!/usr/bin/python
"""Program to execute a VBA macro in MS Excel
"""
import os
import shutil
import win32com.client
import pythoncom
import repackage
repackage.up()


def execute_macro():
  """Execute VBA macro in MS Excel
  """
  pythoncom.CoInitialize()
  current_path = os.path.dirname(os.getcwd())
  path_to_file = current_path+"\\action\\data\\excelsheet.xlsm"
  if os.path.exists(path_to_file):
    xl_file = win32com.client.Dispatch("Excel.Application")
    xl_run = xl_file.Workbooks.Open(os.path.abspath(path_to_file),
                                    ReadOnly=1)
    xl_run.Application.Run("excelsheet.xlsm!main.simpleMain") #execute macro
    xl_run.Save()
    xl_run.Close()
    xl_file.Quit()
    del xl_file
    shutil.move(path_to_file, current_path+"\\action\\output\\excelsheet.xlsm")
    print("Action successfully executed")

if __name__ == "__main__":
  execute_macro()
