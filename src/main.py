from PIL import Image
import sys

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

    

if __name__ == "__main__":
    main()
