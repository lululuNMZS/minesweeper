from PIL import Image
from PIL import ImageGrab
import my_winapi
import colourdata
import numpy
import math
import win32api
import time


#scan the mine screen,save the mine state to a map[][]
def scan_minemap():
    #scan
    hwnd = my_winapi.find_the_hwnd()
    left, top, right, bottom = my_winapi.find_the_coordinate(hwnd)

    left += 15
    top += 101
    right -= 15
    bottom -= 42
    block_width = 16
    block_height = 16

    mine_scan = ImageGrab.grab().crop((left,top,right,bottom))


    return (left,top,right,bottom)

def init_minemap():
    left, top, right, bottom = scan_minemap()
    map_x = round((right - left) / 16)
    map_y = round((bottom - top) / 16)

    map_array = numpy.zeros([map_x, map_y])

    return map_array

def update_minemap():
    #scan
    hwnd = my_winapi.find_the_hwnd()
    left, top, right, bottom = my_winapi.find_the_coordinate(hwnd)

    left += 15
    top += 101
    right -= 15
    bottom -= 42


    mine_scan = ImageGrab.grab().crop((left, top, right, bottom))



    map_x = round((right - left) / 16)
    map_y = round((bottom - top) / 16)


    block_width = 16
    block_height = 16
    # update the map data
    for j in range(map_y):
        for i in range(map_x):
            print(i)
            small_rect = (i*block_width, j*block_height, (i+1)*block_width, (j+1)*block_height)
            img_small_rect = mine_scan.crop(small_rect)
            #win32api.SetCursorPos([left+i*16, top+j*16])
            #time.sleep(0.1)
            #win32api.SetCursorPos([left+i*16+16, top+j*16+16])
            #time.sleep(0.1)
            print(small_rect)




            compare_colourdata(img_small_rect.getcolors(),i,j)
            print(img_small_rect.getcolors())
            print(map_array[i][j])


def compare_colourdata(data,x,y):
    if data == colourdata.rgba_whiteboard:
        map_array[x][y] = 100;

#first ramdon click

map_array = init_minemap()

#