from win32 import win32gui

def find_the_hwnd():
    class_name = "TMain"
    title_name = "Minesweeper Arbiter "
    hwnd = win32gui.FindWindow(None,title_name)

    left = 0
    top = 0
    right = 0
    bottom = 0

    if hwnd:
        print("find the window")
        left,top,right,bottom=win32gui.GetWindowRect(hwnd)
        print(str(left),str(top),str(right),str(bottom))
    else:
        print("didnt find")

    return hwnd