import repackage 
repackage.up()
import os, os.path
import win32com.client
import shutil
import pythoncom







#execute the execute_macro
def execute_macro(currentPath):
    pythoncom.CoInitialize()
    pathToFile=currentPath+"\\data\\excelsheet.xlsm"
    if os.path.exists(pathToFile):
        xl=win32com.client.Dispatch("Excel.Application")
        wb=xl.Workbooks.Open(os.path.abspath(pathToFile), ReadOnly=1)
        wb.Application.Run("excelsheet.xlsm!main.simpleMain")
        wb.Save()
        wb.Close()
        # xl.Application.save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
        xl.Quit() # Comment this out if your excel script closes
        # xl.Close(savechanges=1)
        del xl
        shutil.copyfile(pathToFile,currentPath+"\\output\\excelsheet.xlsm")
        os.remove(pathToFile)
        print("Successfully completed...............................................")

if __name__=="__main__":
    currentPath=".."
    execute_macro(currentPath)

