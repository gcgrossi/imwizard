# imwizard
Python utilities for image processing with OpenCV.

<img src="logo.png" width="75%"></img>


#### _Introduction_

In my effort to learn computer vision with OpenCV and Python I always incur in some common tasks I need to accomplish before diving into the real juice of each project. Image preprocessing is always needed when working with images. Most of the times this ecompass different actions:

* changing image format
* resizing
* thresholding
* edging
* contour detection
* many more

I use to write a function each time I end up doing a copy+paste of a snippet more than 2/3 times. I am italian, I don't want to spend time copy pasting code. It's a waste of time I can spend to take a good coffee. But I am also a physicist with some efficiency obsessions. I'm scared to death one day I will write a so messy and inefficient code that the world will crash. Or worse, I would have to pass entire days modifying all the code I wrote. I try to keep it clean, commented, compact and modular.

So I put every utility function I use in my Computer Vision projects in ```imwizard```, my own version of OpenCV Python toolbox. And sincerely, I use it a lot! I have a passion for graphics too, so I always make some logos or banners for my READMEs...don't take it too seriously! it's just a creative caprice.

#### _Desciption_

Here follows a description of the main methods and classes that are so far implemented.

```python 
def create_contour_mask(c,img):
``` 
given an imput contour ```c``` and an image ```img```,returns a mask for the contour.

```python
def contour_center(c):
``` 
given an imput contour ```c```, returns a tuple with the (x,y) coordinates of the contour center.

```python
def process_contours(cnts,image):
``` 
given an imput list of contours ```cnts``` and an image ```image```, returns a dictionary ```obj={"centers":[],"area":[],"masks":[],"mean":[],"std":[]}``` with the center coordinates, areas, masks, mean value and stadard deviation of each contour.

