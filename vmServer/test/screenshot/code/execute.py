#!/usr/bin/python
"""Program to take screenshot from a MS Word Document
"""

import os
import shutil
import win32com.client
import pythoncom
import wx
import win32con
import repackage
import win32gui
repackage.up()


def window_enumeration_handler(hwnd, top_windows):
  """Handles window enumeration
  """
  top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def take_screenshot():
  """Take screenshot from the MS word document
  """
  pythoncom.CoInitialize()
  root_path = os.path.dirname(os.getcwd())
  path_to_file = root_path+"\\execute\\action\\data\\sample.docx"
  if os.path.exists(path_to_file):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = 1
    word.Documents.Open(path_to_file)
    top_windows = []
    win32gui.EnumWindows(window_enumeration_handler, top_windows)
    # Select the word document tab and bring it to foreground
    # also maximise the word document
    for window in top_windows:
      if " - Word" in window[1]:
        win32gui.ShowWindow(window[0], win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(window[0])
        break
    app = wx.App()
    screen = wx.ScreenDC()
    size = screen.GetSize()
    bmp = wx.Bitmap(size[0], size[1])
    mem = wx.MemoryDC(bmp)
    mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
    del mem  # Release bitmap
    bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
    word.Quit()
    del word
    dest_path = "\\execute\\action\\output\\screenshot.png"
    shutil.move(root_path+"\\accept\\screenshot.png",
                root_path+dest_path)
    print("Action successfully executed")

if __name__ == "__main__":
  take_screenshot()
