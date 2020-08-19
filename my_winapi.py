from win32 import win32gui
import win32con
import win32api
import time

def find_the_hwnd():
    class_name = "TMain"
    title_name = "Minesweeper Arbiter "
    hwnd = win32gui.FindWindow(None,title_name)

    #if hwnd:
    #    print("find the window")
    #else:
    #    print("didnt find")

    return hwnd

def find_the_coordinate(hwnd):
    left = 0
    top = 0
    right = 0
    bottom = 0
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    #print(str(left), str(top), str(right), str(bottom))

    return (left,top,right,bottom)

def mouse_click_left(x,y):
    win32api.SetCursorPos([x,y])
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse_click_right(x,y):
    win32api.SetCursorPos([x,y])
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


