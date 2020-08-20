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

#return the boom start pixel
def find_the_start_pixel(hwnd):
    left = 0
    top = 0
    right = 0
    bottom = 0
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    left += 15
    top += 100
    right -= 15
    bottom -= 42

    #print(str(left), str(top), str(right), str(bottom))

    return (left,top,right,bottom)

def get_the_map_boundary(left, top, right, bottom):
    x = round((right - left) / 16)
    y = round((bottom - top) / 16)
    return x, y


def mouse_click_left(x,y):

    win32api.SetCursorPos([x, y])
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse_click_right(x,y):
    win32api.SetCursorPos([x, y])
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

def mouse_click_leftandright(x,y):
    win32api.SetCursorPos([x, y])
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN and win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP and win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

