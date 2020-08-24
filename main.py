import my_winapi
import algorithm
from PIL import Image

#get the colors,just for test
#img = Image.open("C:/Users/Administrator/Desktop/4.png")
#this_img = img.crop((322,501,338,516))
#print(this_img.getcolors())


algorithm.init_minemap()
algorithm.update_minemap()
algorithm.auto_run()

