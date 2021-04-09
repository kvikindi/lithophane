![](https://github.com/michaelpineirocode/lithophane/blob/main/images/blog_eye_flashes_1932x862.jpg)

# lithophane
Free to use, open source lithophane maker built using python. The end goal is to be able to convert any image to a lithophane of a specified size.

### Unstable release.

## How to use

As of now, the program must be run with a few command line arguments.  
``` py main.py -inputfile -outputfile -thickness(mm) -layerheight(mm) -max_x(mm) -max_y(mm) ```

The max_x and max_y variables represent the largest x and y value that should be considered for printing, and will typically be the size that the stl is outputed as. The program might give an option to automatically adjust the resolution, but the image still cuts a _little_ off of the bottom and right due to rounding in the program. In the future, I will fix these issues. If the max_x or max_y are far too disproportionate or far too small, it may cut off the sides. I'm not entirely sure why, but it affects some photos more than others. 

The recommended size for a lithograph is 100 on the x and a close approximate to the right proportion on the max_y variable. You can view this result in the "Pics/Output" folder to see if the photo came out properly. _
