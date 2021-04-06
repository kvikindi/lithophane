![](https://github.com/michaelpineirocode/lithophane/blob/main/images/blog_eye_flashes_1932x862.jpg)

# lithophane

Free to use, open source lithophane maker built using python. The end goal is to be able to convert any image to a lithophane of a specified size.

## How to use

As of now, the program must be run with a few command line arguments.  
``` py main.py -inputfile -outputfile -thickness(mm) -layerheight(mm) -max_x(mm) -max_y(mm) ```

A few notes. Both the input file and the output file must be contained within the same directory as main.py for now. The max_x and max_y variables represent the largest x and y value that should be considered for printing, and will typically be the size that the stl is outputed as.
