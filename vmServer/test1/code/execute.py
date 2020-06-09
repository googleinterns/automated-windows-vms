import repackage 
repackage.up()
import os, os.path
import win32com.client
import shutil
import pythoncom
import wx
import win32gui, win32con

def windowEnumerationHandler(hwnd,top_windows):
    top_windows.append((hwnd,win32gui.GetWindowText(hwnd)))





#execute the execute_macro
def execute_macro(currentPath):
    pythoncom.CoInitialize()
    # print("I am also here")
    # print(currentPath)
    rootPath=os.path.dirname(os.getcwd())
    pathToFile=rootPath+"\\accept\\execute\\action\\data\\sample.docx"
    # print(os.listdir())
    print(pathToFile)
    if os.path.exists(pathToFile):
        print("I'm not here")
        # os.startfile(pathToFile)
        word=win32com.client.Dispatch("Word.Application")
        # # wb=xl.Workbooks.Open(os.path.abspath(pathToFile), ReadOnly=1)
        # # wb.Application.Run("excelsheet.xlsm!main.simpleMain")
        # # wb.Save()
        # # wb.Close()
        # xl.Visible=1
        # print(pathToFile)
        # xl.Documents.Open(pathToFile)
        word.Visible=1
        word.Documents.Open(pathToFile)
        results = []
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        print(top_windows)
        for i in top_windows:
            if " - Word" in i[1]:
                print("ooooooooooooooooooooooooooooooooooooooo")
                print (i)
                # win32gui.ShowWindow(i[0],5)
                win32gui.ShowWindow(i[0],win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(i[0])
                break
        A=wx.App()  
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.Bitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
        # word.Application.save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
        word.Quit() # Comment this out if your excel script closes
        # # xl.Close(savechanges=1)
        del word
        shutil.move(rootPath+"\\accept\\screenshot.png",rootPath+"\\accept\\execute\\action\\output\\screenshot.png")
        # os.remove(pathToFile)
        print("Successfully completed...............................................")

if __name__=="__main__":
    print("I'm here")
    currentPath='execute\\action'
    execute_macro(currentPath)


