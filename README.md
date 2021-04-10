![](https://github.com/michaelpineirocode/lithophane/blob/main/images/blog_eye_flashes_1932x862.jpg)

# lithophane
Free to use, open source lithophane maker built using python. The end goal is to be able to convert any image to a lithophane of a specified size.

### Unstable release.

## How to use

As of now, the program must be run with a few command line arguments.  
``` py main.py -inputfile -outputfile -thickness(mm) -layerheight(mm) -max_x(mm) -max_y(mm) -normalizing_multiplier(float)```

The max_x and max_y variables represent the largest x and y value that should be considered for printing, and will typically be the size that the stl is outputed as. The program might give an option to automatically adjust the resolution, but the image still cuts a _little_ off of the bottom and right due to rounding in the program. In the future, I will fix these issues. If the max_x or max_y are far too disproportionate or far too small, it may cut off the sides. I'm not entirely sure why, but it affects some photos more than others.  

The normalizing factor is for adjusting the x if the peaks and valleys are far too large.  

When the 3D model is made, it will be scaled far too large. In the slicer, you need to scale it down to the dimensions you entered for optimal results. In the future I may automatically adjust this, but for now it is easy enough to adjust in the slicer. The reason for a max_x and max_y is for optimal resolution. For the size.  

The recommended size for a lithograph is 100 on the x and a close approximate to the right proportion on the max_y variable for a landscape orientated photo. You can view this result in the "Pics/Output" folder to see if the photo came out properly.   

## Dependencies  
Python 3.9 or higher: www.python.org  
Ultimaker Cura or another slicer of your choosing.  
numpy: ```pip3 install numpy```  
numpy-stl: ```pip3 install numpy-stl```  
Pillow: ```pip3 install pillow```  

There is a possibility that numpy won't install properly on a Mac, I believe that this could be due to the M1 chip. This is what worked for me when I installed it in my project directory (src), and then installing numpy-stl also worked: 
```pip3 install Cython. 
git clone https://github.com/numpy/numpy.git  
cd numpy  
pip3 install . --no-binary :all: --no-use-pep517  
```
This code will clone numpy into the directory locally.

## Demo  
### 1.) Ensure that "beach_hut.jpeg" is in the src/Pics/Input directory.
![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%201.11.23%20PM.png)

### 2.) Within the src directory, execute the command following the arguments above.  
![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%201.23.26%20PM.png)  

```python3 main.py beach_hut.jpeg beach 2 0.12 100 50 1.2```  

I find that a thickness of 3-4 mm is ideal. I am running an Ender 3 Pro, so a layer thickness 0.12 mm is going to be the finest layer height that I can afford. The maximum size that I am comfortable with this lithophane being is 100 mm x 50 mm, so I am going to put those for max_x and max_y.

### 3.) Adjust the resolution if needed.  
![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%201.23.54%20PM.png)  

The resolution may need to be adjusted. In that case, go ahead and hit "y" for yes and it will automatically adjust. If the proportions are _far_ off, then it is possible that the program will fail. For example, obviously it can't create a mesh that is 1 mm x 500 mm, it just won't work.  
  
The program may take a while to run depending on how beefy your machine is. It will output the time in seconds that it took to complete when it is done. Now there should be a photo in the "src/Pics/Output" directory, as well as an stl in the "src/STLS" directory.
