from PIL import Image
from PIL import ImageGrab
import my_winapi
import colourdata
import numpy
import math
import win32api
import time
import random


#scan the mine screen,save the mine state to a map[][]
def scan_minemap():
    #scan
    hwnd = my_winapi.find_the_hwnd()
    left, top, right, bottom = my_winapi.find_the_coordinate(hwnd)

    left += 15
    top += 100
    right -= 15
    bottom -= 42

    mine_scan = ImageGrab.grab().crop((left,top,right,bottom))

    return {'image_rect':(left,top,right,bottom), 'image':mine_scan}

def init_minemap():
    left, top, right, bottom = scan_minemap()['image_rect']
    map_x = round((right - left) / 16)
    map_y = round((bottom - top) / 16)

    map_array = numpy.zeros([map_x, map_y],dtype=numpy.int8)

    return map_array

def update_minemap():
    left, top, right, bottom = scan_minemap()['image_rect']
    image_mine_scan = scan_minemap()['image']

    map_x = round((right - left) / 16)
    map_y = round((bottom - top) / 16)

    block_width = 16
    block_height = 16

    # update the map data
    for j in range(map_y):
        for i in range(map_x):
            small_rect = (i*block_width, j*block_height, (i+1)*block_width, (j+1)*block_height)
            img_small_rect = image_mine_scan.crop(small_rect)

            #win32api.SetCursorPos([left+i*16, top+j*16])
            #time.sleep(0.1)
            #win32api.SetCursorPos([left+i*16+16, top+j*16+16])
            #time.sleep(0.1)
            #print(small_rect)




            compare_colourdata(img_small_rect.getcolors(),i,j)
            #print(img_small_rect.getcolors())
            #print(map_array[i][j])


def compare_colourdata(data,x,y):
    #100: white board ,didnt clicked
    #99: flag
    if data == colourdata.rgba_whiteboard:
        map_array[x][y] = 100;
    elif data == colourdata.rgba_0:
        map_array[x][y] = 0;
    elif data == colourdata.rgba_1:
        map_array[x][y] = 1;
    elif data == colourdata.rgba_2:
        map_array[x][y] = 2;
    elif data == colourdata.rgba_3:
        map_array[x][y] = 3;
    elif data == colourdata.rgba_4:
        map_array[x][y] = 4;
    elif data == colourdata.rgba_5:
        map_array[x][y] = 5;
    elif data == colourdata.rgba_6:
        map_array[x][y] = 6;
    elif data == colourdata.rgba_8:
        map_array[x][y] = 8;
    elif data == colourdata.rgba_flag:
        map_array[x][y] = 99;
    elif data == colourdata.rgba_boom:
        map_array[x][y] = 98;
    elif data == colourdata.rgba_boom_red:
        map_array[x][y] = 97;


#the state map
map_array = init_minemap()




def random_click():
    left, top, right, bottom = scan_minemap()['image_rect']
    x = random.randint(0, 99) % map_array.shape[0]
    y = random.randint(0, 99) % map_array.shape[1]


    while (1):
        if map_array[x][y] == 97 or map_array[x][y] == 98 :
            break

        if map_array[x][y] == 100:
            my_winapi.mouse_click_left(left + x*16, top + y*16)
            break

        x = random.randint(0, 99) % map_array.shape[0]
        y = random.randint(0, 99) % map_array.shape[1]


def get_around_state(x,y):
    whiteboard_count = 0
    for j in range(8):
        if map_array[x-1][y-1] == 100:
            whiteboard_count = whiteboard_count +1
        if map_array[x][y-1] == 100:
            whiteboard_count = whiteboard_count + 1

    return


def auto_run():
    state_num = 0
    for j in range(map_array.shape[1]):
        for i in range(map_array.shape[0]):
            state_num = map_array[i][j]

