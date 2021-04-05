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

def find_heights(pix):
    thickness = sys.argv[3]
    layerheight = sys.argv[4]

def lower_resolution(x, y, pix):
    layer_height = float(sys.argv[4])
    max_x = int(sys.argv[5]) # the physical size in mm
    max_y = int(sys.argv[6]) 

    x_resolution = int((max_x / layer_height)) # the number of pixels that can physically fit given the layer thickness
    y_resolution = int(max_y / layer_height)

    adjustment_x = math.ceil(x - x_resolution) # the number of x that I need to remove
    adjustment_y = math.ceil(y - y_resolution) # the number of y that I need to remove

    intervals_x = 1 #initializing intervals as 1
    intervals_y = 1

    if (adjustment_x) > 0:
        # print(x, x_resolution)
        intervals_x = math.floor(x / adjustment_x) #defining how often to SKIP a pixel

    
    if (adjustment_y) > 0:
        # print(y, y_resolution)
        intervals_y = math.floor(y / adjustment_y)
    
    img = Image.new("RGB", (x_resolution, y_resolution), (0, 0, 0)) # creates a new blank image of new size that will be used to modify

    adj_pix = img.load()
    # print(adj_pix[1, 1])
    
    for i in range(y_resolution):
        for j in range(x_resolution):
            if (i % intervals_y != 0) or (j % intervals_x != 0):
                pixel = pix[j, i]
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
    if (max_y / layer_height) > y:
        if input("Picture cannot fit within the space determined. Would you like to automatically adjust the resolution? (y/n)") == "y":
            return False
        else:
            raise Exception("Picture cannot fit into the maximum y length provided. Please increase the y or reduce the resolution of the image")
    else:
        return True

def create_stl(pix, x, y):
    if test_fit(x, y) == False:
        pix = lower_resolution(x, y, pix)
        save_image(pix)

def main():
    # instantiating the image
    img = Image.open(sys.argv[1])

    # assigning important variables for image processing
    x = img.size[0]
    y = img.size[1]
    pix = img.load()

    # convert to grayscale
    pix = convert_to_grayscale(pix, x, y)
    save_image(img)
    
    create_stl(pix, x, y)

if __name__ == "__main__":
    main()
