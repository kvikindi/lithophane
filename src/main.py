from PIL import Image
import sys
import math

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
    img.save(sys.argv[2]) #saves image

def find_heights(pix, x, y):
    thickness = float(sys.argv[3])
    layerheight = float(sys.argv[4])

    light_resolution = (thickness / layerheight)
    light_increments = math.floor(255 / light_resolution)
    
    heightmap = [[0 for i in range(y + 1)] for j in range(x + 1)] # this creates an empty 2D array of size x by y

    for i in range(y):
        for j in range(x):
            pixel = pix[j, i]
            heightmap[j][i] = math.ceil(pixel[0] / light_increments) # since every item in the tuple is the same, this index doesn't matter


def lower_resolution(x, y, pix):
    layer_height = float(sys.argv[4])
    max_x = int(sys.argv[5]) # the physical size in mm
    max_y = int(sys.argv[6]) 
    x_resolution = int((max_x / layer_height)) # the number of pixels that can physically fit given the layer thickness
    y_resolution = int(max_y / layer_height)
    adjustment_x = math.ceil(x - x_resolution) # the number of x that I need to remove
    adjustment_y = math.ceil(y - y_resolution) # the number of y that I need to remove
    intervals_x = x #initializing intervals as 1
    intervals_y = y

    if (adjustment_x) > 0:
        intervals_x = math.floor(x / adjustment_x) #defining how often to SKIP a pixel

    if (adjustment_y) > 0:
        intervals_y = math.floor(y / adjustment_y)
    
    img = Image.new("RGB", (x_resolution, y_resolution), (0, 0, 0)) # creates a new blank image of new size that will be used to modify
    adj_pix = img.load()

    x_offset, y_offset = 0, 0

    for i in range(y_resolution):
        x_offset = 0 #resets the offset every time that we change y's
        if (i % intervals_y == 0): #skips a y ONCE for every time we loop through
                y_offset += 1
        for j in range(x_resolution):
            pixel = pix[j + x_offset, i + y_offset]
            adj_pix[j, i] = pixel

            if (j % intervals_x == 0):
                pass
                x_offset += 1

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

def create_stl(pix, x, y):
    if test_fit(x, y) == False:
        pass
    
def main():
    # instantiating the image
    img = Image.open(sys.argv[1])

    # assigning important variables for image processing
    x = img.size[0]
    y = img.size[1]
    pix = img.load()

    #adjust resolution if needed
    if test_fit(x, y) == False:
        img = lower_resolution(x, y, pix)
        x = img.size[0]
        y = img.size[1]
        pix = img.load()

    # convert to grayscale
    pix = convert_to_grayscale(pix, x, y)
    
    # calculate "heightmap" (or whatever this data structure is) based on grayscale intensities
    find_heights(pix, x, y)
    #create a mesh
    create_stl(pix, x, y)

if __name__ == "__main__":
    main()
