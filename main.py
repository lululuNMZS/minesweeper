import my_winapi
import algorithm
from PIL import Image

#get the colors,just for test
#img = Image.open("C:/Users/Administrator/Desktop/4.png")
#this_img = img.crop((322,501,338,516))
#print(this_img.getcolors())


algorithm.init_minemap()
algorithm.update_minemap()

#for j in range(8):
#    for i in range(8):
 #       print(algorithm.map_array[i][j])

print(algorithm.map_array)
algorithm.random_click()