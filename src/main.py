from PIL import Image
import sys
import math
import numpy as np
from stl import mesh, stl
import time
from fractions import Fraction

def mean(pixel):
    sum__ = pixel[0] + pixel[1] + pixel[2]
    mean = int(sum__ / 3)
    return (mean, mean, mean)

def convert_to_grayscale(pix, x, y):
    for i in range(y):
        for j in range(x):
            pixel = pix[j, i]
            pix[j, i] = mean(pixel)
    return pix

def save_image(img):
    img.save("Pics/Outputs/" + sys.argv[2] + ".png") #saves image

def find_heights(pix, x, y):
    thickness = float(sys.argv[3])
    layerheight = float(sys.argv[4])

    light_resolution = (thickness / layerheight)
    light_increments = math.floor(255 / light_resolution)
    
    heightmap = [[0 for i in range(y + 1)] for j in range(x + 1)] # this creates an empty 2D array of size x by y


    for i in range(y):
        for j in range(x):
            pixel = pix[j, i]
            heightmap[j][i] = abs(round(light_increments - ((255 - pixel[0]) / (light_increments * float(sys.argv[7]))))) # since every item in the tuple is the same, this index doesn't matter. Also argc[7] is normalizing value
            if heightmap[j][i] == 0: #ensures that there will be a bottom
                heightmap[j][i] = 1
    return heightmap

def lower_resolution(x, y, pix):
    '''
        First thing is first, I need to work out  a lot of different variables that will be useful
    '''
    
    layer_height = float(sys.argv[4]) # the layer height of the printer
    max_x = int(sys.argv[5]) # the physical size in mm
    max_y = int(sys.argv[6])
    x_resolution = math.ceil(max_x / layer_height)
    y_resolution = math.ceil(max_y / layer_height)
    x_factor = math.ceil(x / x_resolution)
    y_factor = math.ceil(y / y_resolution)

    rows_tokeep = []
    cols_tokeep = []
    
    for i in range(y): # loops through every row
        if (i % y_factor == 0): # adjusts offset for y ONCE for every time we hit an interval
            rows_tokeep.append(i)
    for j in range(x):
        if (j % x_factor == 0):
            cols_tokeep.append(j)
    
    img = Image.new("RGB", (len(cols_tokeep), len(rows_tokeep)), (0, 0, 0)) # creates a new blank image of new size that will be used to modify
    adj_pix = img.load()
    print(rows_tokeep)

    for i in range(len(rows_tokeep) - 1):
        for j in range(len(cols_tokeep) - 1):
            # print(i, j)
            pixel = pix[cols_tokeep[j], rows_tokeep[i]]
            adj_pix[j, i] = pixel
    
    return img

def test_fit(x, y):
    layer_height = float(sys.argv[4])
    max_x = int(sys.argv[5])
    max_y = int(sys.argv[6])

    if (max_x / layer_height) < x:

        if input("Picture cannot fit within the space determined. Would you like to automatically adjust the resolution? (y/n)") == "y":
            return False
        else:
            raise Exception("Picture cannot fit into the maximum x length provided. Please increase the x or reduce the resolution of the image.")
    if (max_y / layer_height) < y:
        if input("Picture cannot fit within the space determined. Would you like to automatically adjust the resolution? (y/n)") == "y":
            return False
        else:
            raise Exception("Picture cannot fit into the maximum y length provided. Please increase the y or reduce the resolution of the image")
    else:
        return True

def save_data(data, filename):
    file_ = open("Data/" + filename, "w")
    for i in range(len(data)):
        file_.write(str(data[i]) + "\n")
    file_.close()

def change_vectors(surfaces, vert_index, array_content):
    surfaces["vectors"][vert_index] = np.array(array_content)
    vert_index += 1
    return surfaces, vert_index

def find_surfaces(heightmap):
    number_of_vertices = (((len(heightmap[0]) - 1) * (len(heightmap) - 1)) * 2) + (((len(heightmap[0]) - 1) * 4) + ((len(heightmap) - 1) * 5)) + 2 # the number of vertices is 2(x-1 * y-1) + 4(x-1 + y-1) + 2
    surfaces = np.zeros(number_of_vertices, dtype=mesh.Mesh.dtype) # need to add 10 because of the sides and bottom

    vert_index = 0
    for y in range(len(heightmap)):
        if y != len(heightmap) - 1: #do not need to complete in the last row
            for x in range(len(heightmap[y])):
                if x != len(heightmap[y]) - 1: # do not need last column
                    surfaces, vert_index = change_vectors(surfaces, vert_index, [[x, y, heightmap[y][x]], [x, y+1, heightmap[y+1][x]], [x+1, y, heightmap[y][x+1]]]) #creates "first" triangle
                    surfaces, vert_index = change_vectors(surfaces, vert_index, ([[x, y+1, heightmap[y+1][x]], [x+1, y+1, heightmap[y+1][x+1]], [x+1, y, heightmap[y][x+1]]]))
    
    for y in range(len(heightmap)): # for creating the bottom section
            # this is for creating the sides ALONG the y-axis
            row_size = len(heightmap[y]) - 1
            surfaces, vert_index = change_vectors(surfaces, vert_index, [[0, y, heightmap[y][0]], [0, y, 0], [0, y+1, heightmap[y][0]]]) # sides closest to 0 index
            surfaces, vert_index = change_vectors(surfaces, vert_index, [[0, y+1, heightmap[y][0]], [0, y, 0], [0, y+1, 0]])
            surfaces, vert_index = change_vectors(surfaces, vert_index, [[row_size, y, heightmap[y][row_size]], [row_size, y, 0], [row_size, y+1, heightmap[y][0]]]) # sides furthest from 0 index
            surfaces, vert_index = change_vectors(surfaces, vert_index, [[row_size, y+1, heightmap[y][row_size]], [row_size, y, 0], [row_size, y+1, 0]])

    for x in range(len(heightmap[0])): # this creates the sides ALONG the x-axis
            column_size = len(heightmap) - 1

            surfaces, vert_index = change_vectors(surfaces, vert_index, [[x, 0, heightmap[0][x]], [x, 0, 0], [x+1, 0, heightmap[0][x]]]) # sides closest to 0 index
            surfaces, vert_index = change_vectors(surfaces, vert_index, [[x+1, 0, heightmap[0][x]], [x, 0, 0], [x+1, 0, 0]])
            surfaces, vert_index = change_vectors(surfaces, vert_index, [[x, column_size, heightmap[column_size][x]], [x, column_size, 0], [x+1, column_size, heightmap[0][x]]]) # sides furthest from 0 index
            surfaces, vert_index = change_vectors(surfaces, vert_index, [[x+1, column_size, heightmap[column_size][x]], [x, column_size, 0], [x+1, column_size, 0]])
    
    # add last two vertices on the bottom!
    surfaces, vert_index = change_vectors(surfaces, vert_index, [[0, 0, 0], [row_size, 0, 0], [0, column_size, 0]])
    surfaces, vert_index = change_vectors(surfaces, vert_index, [[row_size, column_size, 0], [row_size, 0, 0], [0, column_size, 0]])

    return surfaces

def create_mesh(surfaces):
    stl_mesh = mesh.Mesh(surfaces, remove_empty_areas = False)
    stl_mesh.normals
    stl_mesh.save("STLS/" + sys.argv[2] + ".stl", mode=stl.Mode.ASCII)

def main():
    # starting a timer
    start = time.time()

    # instantiating the image
    img = Image.open("Pics/Inputs/" + sys.argv[1])

    # assigning important variables for image processing
    x = img.size[0]
    y = img.size[1]
    pix = img.load()
    print(x, y)
    
    # convert to grayscale
    pix = convert_to_grayscale(pix, x, y)

    #adjust resolution if needed
    if test_fit(x, y) == False:
        img = lower_resolution(x, y, pix)
        x = img.size[0]
        y = img.size[1]
        pix = img.load()

    save_image(img)
    
    # calculate "heightmap" (or whatever this data structure is) based on grayscale intensities
    heightmap = find_heights(pix, x, y)
    save_data(heightmap, sys.argv[2])
    #find surfaces
    surfaces = find_surfaces(heightmap)
    
    #create a mesh
    create_mesh(surfaces)

    ellapsed = time.time() - start
    print(ellapsed)

if __name__ == "__main__":
    main()
