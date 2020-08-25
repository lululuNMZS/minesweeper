from PIL import Image
from PIL import ImageGrab
import my_winapi
import colourdata
import numpy
import math
import win32api
import time
import random

hwnd = my_winapi.find_the_hwnd()
left, top, right, bottom = my_winapi.find_the_start_pixel(hwnd)
boom_block_width = 16
boom_block_height = 16


#scan the mine screen,save the mine state to a map[][]
def scan_minemap():
    #grab the pic ,start from the boom area
    mine_scan = ImageGrab.grab().crop((left, top, right, bottom))

    return mine_scan

def init_minemap():
    #get the map indexs
    map_x, map_y = my_winapi.get_the_map_boundary(left, top, right, bottom)
    #print(map_x, map_y)
    #init the map with zero
    map_array = numpy.zeros([map_x, map_y],dtype=numpy.int8)

    return map_array

#the state map
map_array = init_minemap()

def update_minemap():
    image_mine_scan = scan_minemap()
    map_x, map_y = my_winapi.get_the_map_boundary(left, top, right, bottom)


    # update the map data
    for j in range(map_y):
        for i in range(map_x):
            small_rect = (i*boom_block_width, j*boom_block_height, \
                          (i+1)*boom_block_width, (j+1)*boom_block_height)
            img_small_rect = image_mine_scan.crop(small_rect)

            compare_colourdata(img_small_rect.getcolors(), i, j)


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







def random_click():

    for y in range(map_array.shape[1]):
        for x in range(map_array.shape[0]):
            if map_array[x][y] == 100:
                my_winapi.mouse_click_left(left + x*boom_block_width,\
                                           top + y*boom_block_height)
                return



def get_around_state(x,y):
    white_count = 0
    flag_count = 0


    for j in range(y-1, y+1+1):
        for i in range(x-1, x+1+1):
            if (i < 0 or j < 0 or \
                   i >= map_array.shape[0] or \
                   j >= map_array.shape[1]):
                continue

            print((i,j))
            if (map_array[i][j] == 100):
                white_count = white_count +1
            if (map_array[i][j] == 99):
                flag_count = flag_count +1
    print(white_count,flag_count)
    return white_count, flag_count

def put_the_flag(x,y):

    for j in range(y-1, y+1+1):
        for i in range(x-1, x+1+1):
            if (i < 0 or j < 0 or \
                   i >= map_array.shape[0] or \
                   j >= map_array.shape[1]):
                continue


            if (map_array[i][j] == 100):
                my_winapi.mouse_click_right(left + i*boom_block_width, \
                                            top + j*boom_block_height)

    return


def traverse_the_map():
    #if there is a state_num that have the right flag and the white board
    #havent been clicked , we should go back and double click the state_num,
    #skip the random click
    for j in range(map_array.shape[1]):
        for i in range(map_array.shape[0]):

            state_num = map_array[i][j]
            white_count = get_around_state(i, j)[0]
            flag_count = get_around_state(i,j)[1]
            if (state_num == flag_count and \
                    (flag_count+white_count > state_num)):
                return 0
            if (state_num != 0 and state_num == white_count \
                    and flag_count == 0):
                return 0


    return  1



def auto_run():
    while(1):
        update_minemap()
        if traverse_the_map():
            random_click()
            update_minemap()

        for y in range(map_array.shape[1]):
            for x in range(map_array.shape[0]):
                #update_minemap()

                state_num = map_array[x][y]

                if (state_num == 98 or state_num == 97):
                    print("game over")
                    return

                white_count = get_around_state(x,y)[0]
                flag_count = get_around_state(x,y)[1]

                if (state_num >= 1 and state_num <= 8):
                    #onle double click the sure state_num
                    if (flag_count == state_num and \
                            flag_count+white_count >state_num):
                        my_winapi.mouse_click_leftandright(left + x*boom_block_width, \
                                                       top + y*boom_block_height)
                        update_minemap()


                    around_state_count = white_count + flag_count

                    if (state_num == around_state_count):
                        put_the_flag(x, y)
                        update_minemap()






