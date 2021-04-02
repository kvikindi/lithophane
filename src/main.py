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
    max_x = int(sys.argv[5]) #the physical size
    max_y = int(sys.argv[6]) 

    x_resolution = (max_x / layer_height) #the number of pixels that can physically fit
    y_resolution = (max_y / layer_height)

    adjustment_x = math.ceil(x - x_resolution) # the number of x that I need to remove
    adjustment_y = math.ceil(y - y_resolution)

    if (adjustment_x) > 0:
        
        print(x, x_resolution)
        intervals = math.floor(x / adjustment_x)
        
        blank = Image.new("RGB", (adjustment_x, adjustment_y), (0, 0, 0)) # creates a new blank image of new size that will be used to modify

        for i in range(x):
            pass #this will be the part that systematically creates a new image based on the ones that need to be removed
    
    if (adjustment_y) > 0:
        print(y, y_resolution)

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
        lower_resolution(x, y, pix)



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
