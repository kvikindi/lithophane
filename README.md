![](https://github.com/michaelpineirocode/lithophane/blob/main/images/blog_eye_flashes_1932x862.jpg)

# Lithophane
Free to use, open source lithophane maker built using python. The end goal is to be able to convert any image to a lithophane of a specified size.

## How to use

As of now, the program must be run with a few command line arguments.  
``` py main.py -inputfile -outputfile -thickness(mm) -layerheight(mm) -max_x(mm) -max_y(mm) -normalizing_multiplier(float)```

The max_x and max_y variables represent the largest x and y value that should be considered for printing, and will typically be the size that the STL is optimized for. The program has an option to automatically adjust resolution. Before loading the STL, check the "/src/Pics/Outputs" folder for your image. If the image is too low of resolution, then you will need to crop it manually or increase the max_x and max_y 

The normalizing factor is for adjusting the x if the peaks and valleys are far too large. I typically use a value of 1.2, although this is not neccessary. I recommend playing around with it.

When the 3D model is made, it will be scaled far too large. In the slicer, you need to scale it down to the dimensions you entered for optimal results. In the future I may automatically adjust this, but for now it is easy enough to adjust in the slicer. The reason for a max_x and max_y is for optimal resolution for the size that can fit on the printer.  

The recommended size for a lithograph is close to 100 on either axis and a close approximate to the same proportion on the other. You can view this result in the "src/Pics/Output" folder to see if the photo came out properly.   

## Dependencies  
Python 3.9 or higher: www.python.org  
Ultimaker Cura or another slicer of your choosing.  
numpy: ```pip3 install numpy```  
numpy-stl: ```pip3 install numpy-stl```  
Pillow: ```pip3 install pillow```  

Or you can open the terminal in the main directory "/lithophane" and run:  
```pip3 install -r requirements.txt```  
This will automatically install all of the dependencies (except for Python), which are listed in the requirements.txt file. If it does not work, then I would go through each dependency and troubleshoot which one does not work.

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

If you'd like, you can click on the output photo to see the grayscale image and see if the details are displaying properly.
![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%201.24.14%20PM.png)

### 4.) Import the STL file into Cura (or a slicer of your choosing)
![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%2010.21.20%20PM.png)

All instructions will be for the Cura slicer, although this should work in any slicer.

When importing the STL, it will come in _way_ larger than the max_x and max_y were assigned to. That is fine, we will be adjusting that shortly. You may also notice an error that appears at the bottom about the object not being manifold. Although this could create some issues, I have not run into an issue slicing due to this yet (the vertices that are missing that cause this bug are off so little that Cura can automatically fix them).

![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%2010.22.09%20PM.png)
You can move the file to the center by editing the transform to 0, and then rescale the STL to the right size. I like to use uniform scaling, then adjust the larger axis. There may be times where the uniform scaling will not scale to the proper value that was entered into the program. This is due to being too disproportionate. You can disable uniform scaling and adjust the second axis accordingly.

The STL should become highlighted red and yellow at this point.

![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%2010.22.22%20PM.png)
Finally, you can disable uniform scaling and adjust the z axis to what was entered for the thickness in the program. From a side view, if the peaks and valleys seem far too high or low, then this may mean adjusting the "normalizing value" in the command line and reloading the mesh.

![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%2010.22.53%20PM.png)
Next is ensuring that the proper settings are enabled. Make sure the proper layer thickness is set, 100% infill is set, and retraction with z-hop.

![](https://github.com/michaelpineirocode/lithophane/blob/main/images/Screen%20Shot%202021-04-10%20at%2010.23.27%20PM.png)
You can tab over to "preview" to get a better look at the model before printing, without all of the highlighted colors.

If you need to make adjustments, as long as the STL has the same output name, then if you run the command line again, a prompt will appear in Cura asking if you want to reload the file. This will save the transformations and translations, so it doesn't need to be resized or moved every single time.

### Happy Printing!
