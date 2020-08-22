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
    print(map_x, map_y)
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
            small_rect = (i*boom_block_width, j*boom_block_height, (i+1)*boom_block_width, (j+1)*boom_block_height)
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







def random_click():
    x = random.randint(0, 99) % map_array.shape[0]
    y = random.randint(0, 99) % map_array.shape[1]


    while (1):
        if map_array[x][y] == 100:
            my_winapi.mouse_click_left(left + x*boom_block_width, top + y*boom_block_height)
            break

        x = random.randint(0, 99) % map_array.shape[0]
        y = random.randint(0, 99) % map_array.shape[1]



def get_around_state(x,y):
    whiteboard_count = 0

    #middle area
    if (x-1) >= 0 and (y-1) >= 0 and \
            (x+1) < map_array.shape[0] and (y+1) < map_array.shape[1]:
        if map_array[x-1][y-1] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x-1][y] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x-1][y+1] == 100:
            whiteboard_count = whiteboard_count + 1

        if map_array[x][y-1] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x+1][y-1] == 100:
            whiteboard_count = whiteboard_count + 1



        if map_array[x+1][y] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x+1][y+1] == 100:
            whiteboard_count = whiteboard_count + 1

        if map_array[x][y+1] == 100:
             whiteboard_count = whiteboard_count + 1

        return whiteboard_count

    #4 corners
    #(left, top)
    if (x-1) < 0 and (y-1) < 0:
        if map_array[x+1][y] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x][y+1] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x+1][y+1] == 100:
            whiteboard_count = whiteboard_count + 1

        return whiteboard_count

    #(right, bottom)
    if (x+1) >= map_array.shape[0] and (y+1) >= map_array.shape[1]:
        if map_array[x-1][y-1] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x][y-1] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x-1][y] == 100:
            whiteboard_count = whiteboard_count + 1

        return whiteboard_count

    #(top, right)
    if (x + 1) >= map_array.shape[0] and (y-1) < 0:
        if map_array[x-1][y] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x-1][y+1] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x][y+1] == 100:
            whiteboard_count = whiteboard_count + 1

        return whiteboard_count

    #(left, bottom)
    if (x - 1) < 0  and (y + 1) >= map_array.shape[1]:
        if map_array[x][y-1] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x+1][y-1] == 100:
            whiteboard_count = whiteboard_count + 1
        if map_array[x+1][y] == 100:
            whiteboard_count = whiteboard_count + 1

        return whiteboard_count

    #4 sides
    #left side
    if (x-1) < 0 and (y-1) >= 0 or \
            (x-1) < 0 and (y+1) <= map_array.shape[1]:
        if (map_array[x][y-1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x+1][y-1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x+1][y] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x+1][y+1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x][y+1] == 100):
            whiteboard_count = whiteboard_count+1

        return whiteboard_count

    #right side
    if (x+1) >= map_array.shape[0] and (y-1) >= 0 or \
            (x+1) >= map_array.shape[0] and (y+1) <= map_array.shape[1]:
        if (map_array[x][y-1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x-1][y-1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x-1][y] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x-1][y+1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x][y+1] == 100):
            whiteboard_count = whiteboard_count+1

        return whiteboard_count

    #top side
    if (x-1) >= 0 and (y-1) < 0 or \
            (x+1) <= map_array.shape[0] and (y-1) <0:
        if (map_array[x-1][y] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x-1][y+1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x][y+1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x+1][y+1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x+1][y] == 100):
            whiteboard_count = whiteboard_count+1

        return whiteboard_count

    #bottom side
    if (x-1) >= 0 and (y+1) >= map_array.shape[1] or \
            (x+1) <= map_array.shape[0] and (y+1) >= map_array.shape[1]:
        if (map_array[x-1][y] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x-1][y-1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x][y-1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x+1][y-1] == 100):
            whiteboard_count = whiteboard_count+1
        if (map_array[x+1][y] == 100):
            whiteboard_count = whiteboard_count+1

        return whiteboard_count





def put_the_flag(x,y):

    #middle area
    if (x-1) >= 0 and (y-1) >= 0 and \
            (x+1) < map_array.shape[0] and (y+1) < map_array.shape[1]:
        if map_array[x-1][y-1] == 100:
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + (y-1)*boom_block_height)
        if map_array[x-1][y] == 100:
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + y*boom_block_height)
        if map_array[x-1][y+1] == 100:
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + (y+1)*boom_block_height)

        if map_array[x][y-1] == 100:
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y-1)*boom_block_height)
        if map_array[x+1][y-1] == 100:
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + (y-1)*boom_block_height)



        if map_array[x+1][y] == 100:
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + y*boom_block_height)
        if map_array[x+1][y+1] == 100:
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + (y+1)*boom_block_height)

        if map_array[x][y+1] == 100:
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y+1)*boom_block_height)

        return

    #4 corners
    #(left, top)
    if (x-1) < 0 and (y-1) < 0:
        if map_array[x+1][y] == 100:
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + y*boom_block_height)
        if map_array[x][y+1] == 100:
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y+1)*boom_block_height)
        if map_array[x+1][y+1] == 100:
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + (y+1)*boom_block_height)

        return

    #(right, bottom)
    if (x+1) >= map_array.shape[0] and (y+1) >= map_array.shape[1]:
        if map_array[x-1][y-1] == 100:
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + (y-1)*boom_block_height)
        if map_array[x][y-1] == 100:
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y-1)*boom_block_height)
        if map_array[x-1][y] == 100:
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + y*boom_block_height)

        return

    #(top, right)
    if (x + 1) >= map_array.shape[0] and (y-1) < 0:
        if map_array[x-1][y] == 100:
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + y*boom_block_height)
        if map_array[x-1][y+1] == 100:
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + (y+1)*boom_block_height)
        if map_array[x][y+1] == 100:
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y+1)*boom_block_height)

        return

    #(left, bottom)
    if (x - 1) < 0  and (y + 1) >= map_array.shape[1]:
        if map_array[x][y-1] == 100:
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y-1)*boom_block_height)
        if map_array[x+1][y-1] == 100:
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + (y-1)*boom_block_height)
        if map_array[x+1][y] == 100:
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + y*boom_block_height)

        return

    #4 sides
    #left side
    if (x-1) < 0 and (y-1) >= 0 or \
            (x-1) < 0 and (y+1) <= map_array.shape[1]:
        if (map_array[x][y-1] == 100):
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y-1)*boom_block_height)
        if (map_array[x+1][y-1] == 100):
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + (y-1)*boom_block_height)
        if (map_array[x+1][y] == 100):
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + y*boom_block_height)
        if (map_array[x+1][y+1] == 100):
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + (y+1)*boom_block_height)
        if (map_array[x][y+1] == 100):
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y+1)*boom_block_height)

        return

    #right side
    if (x+1) >= map_array.shape[0] and (y-1) >= 0 or \
            (x+1) >= map_array.shape[0] and (y+1) <= map_array.shape[1]:
        if (map_array[x][y-1] == 100):
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y-1)*boom_block_height)
        if (map_array[x-1][y-1] == 100):
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + (y-1)*boom_block_height)
        if (map_array[x-1][y] == 100):
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + y*boom_block_height)
        if (map_array[x-1][y+1] == 100):
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + (y+1)*boom_block_height)
        if (map_array[x][y+1] == 100):
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y+1)*boom_block_height)
        print(map_array[1,0])
        print("test")
        return

    #top side
    if (x-1) >= 0 and (y-1) < 0 or \
            (x+1) <= map_array.shape[0] and (y-1) <0:
        if (map_array[x-1][y] == 100):
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + y*boom_block_height)
        if (map_array[x-1][y+1] == 100):
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + (y+1)*boom_block_height)
        if (map_array[x][y+1] == 100):
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y+1)*boom_block_height)
        if (map_array[x+1][y+1] == 100):
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + (y+1)*boom_block_height)
        if (map_array[x+1][y] == 100):
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + y*boom_block_height)

        return

    #bottom side
    if (x-1) <= 0 and (y+1) >= map_array.shape[1] or \
            (x+1) <= map_array.shape[0] and (y+1) >= map_array.shape[1]:
        if (map_array[x-1][y] == 100):
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + y*boom_block_height)
        if (map_array[x-1][y-1] == 100):
            my_winapi.mouse_click_right(left + (x-1)*boom_block_width, top + (y-1)*boom_block_height)
        if (map_array[x][y-1] == 100):
            my_winapi.mouse_click_right(left + x*boom_block_width, top + (y-1)*boom_block_height)
        if (map_array[x+1][y-1] == 100):
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + (y-1)*boom_block_height)
        if (map_array[x+1][y] == 100):
            my_winapi.mouse_click_right(left + (x+1)*boom_block_width, top + y*boom_block_height)


    return

def test():
    print(left, top)
    put_the_flag(7,7)


def traverse_the_map():
    for j in range(map_array.shape[1]):
        for i in range(map_array.shape[0]):
            state_num = map_array[i][j]
            return (state_num, i, j)

def auto_run():

    """
     for j in range(map_array.shape[1]):
        for i in range(map_array.shape[0]):
            state_num = 0
            around_whiteboard_count = 0
            update_minemap()
            state_num = map_array[i][j]




            if state_num >=1 and state_num <= 8:
                around_whiteboard_count = get_around_state(i, j)

                print(i,j, 'state:', state_num)
                print(around_whiteboard_count, "around count")
                if (state_num == around_whiteboard_count):
                    put_the_flag(i,j)

                continue

            # if (state_num == around_whiteboard_count):
                    #right click


            # boom or red_boom, exit
            if (state_num == 98 or state_num == 99):
                print(i, j, state_num, "game over")
                return

            random_click()




                #if around_whiteboard_count  == state_num:
                #    if map_array[i][j] == 100:
                 #        my_winapi.mouse_click_right(left + 0*boom_block_width, top + 0*boom_block_height)
    """

    x=0
    y=0
    while(1):
        if ((x >= map_array.shape[0]) or (y >= map_array.shape[1])):
            x= 0
            y=0

        random_click()
        update_minemap()

        state_num,x,y = traverse_the_map()
        #print("state num:", state_num)

        if (state_num == 100):
            x = x + 1
            y = y + 1
            continue
        if (state_num == 98 or state_num == 97):
            print("game over")
            return

        if (state_num >= 1 and state_num <= 8):
            around_whiteboard_count = get_around_state(x,y)
            print("state num:", state_num)
            print("around count:", around_whiteboard_count)
            if (state_num == around_whiteboard_count):
                put_the_flag(x, y)

        x = x + 1
        y = y + 1




