import winapi
from PIL import Image

#get the colors,just for test
#img = Image.open("C:/Users/Administrator/Desktop/4.png")
#this_img = img.crop((322,501,338,516))
#print(this_img.getcolors())

hwnd = winapi.find_the_hwnd()

