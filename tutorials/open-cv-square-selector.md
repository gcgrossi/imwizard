# Build a Simple Bounding Box Annotator with OpenCV and Python



#### _Introduction_
It happens many times I have to select regions in an image while dealing with Computer vision tasks of different nature: 
- I need to detect the color of only a particular zone.
- I need to crop the image.
- I need to annotate an image and return bounding box coordinates.

For all of them I have a common boilerplate code that I always copy and paste from other scripts I wrote, so I decided to write a more handy class for it that will help me in all these tasks, and I have integrated it in my imwizard toolbox.

I find it pretty useful when I need to perform bulk annotation of images. I am currently working on some "custom" object detection tool and OpenCV is fantastic, because I can write simple utils and process commands, by bounding an action to a specific key on my keyboard. And example of workflow can be:

1. Loop over the directory where the images are stored
2. Show the image
3. Perform bounding box selection
4. Use one key (i.e. "v" for "validate") to validate the selection
5. Use another key to skip the image (i.e. "s" for "skip")
6. Use yet another key to delete the image from disk (i.e. "d" for "delete")
7. perform the corresponding action (i.e. store the bounding box coordinates)

The workflow can be complicated if we have more classes. I.e. we can assign a key to each class and validate each bounding box with the corresponding class. In this tutorial I will write the simplier case possible: the class return only a list of the boxs' coordinates and we will cover point 2. and 3. We can leave the other points and the multiclass case for exercise, or for a future implementation.

#### _Building the Class_

Originally I used a function to show an image with OpenCV, and two mouse call backs to detect the box. The idea is very simple:

- when you click the mouse record ```(xhigh,yhigh)``` coordinates
- when you release the mouse record the ```(xlow,low)``` coordinates
- draw a rectangle on the image with OpenCV

But I was upset because if I made a mistake in drawing a rectangle I had to start the process again. I decided to implement a simple mechanism of undo. For this reason I decided to wrap the original functions in a more handy class. Let's start by defining it:

```python
class SquareSelector():
    # - The SquareSelector shows the input image
    #   and writes rectangles on user selected areas
    # - Calling the square_selector functiion returns,
    #   at the end of the selction, a mask with the 
    #   selected areas
    # - Built-in undo logic to revert changes
    
    def __init__(self,image):
        #copy original image to handle reset
        self.clone = image.copy()
        
        # original image, masks and box are stored into lists
        # handles undo operations by returning only the 
        # last component
        self.image = [image.copy()]
        self.mask =  [np.zeros(image.shape[:2]+(1,), dtype="uint8")]
        self.bbox =  []
        
        # initialize the cropping points
        self.pt = []
        return
```
the class take an image as input and create a clone to store as a class member. The input image is stored also in a list. A list of masks is also initialized with an array of zeros of the same shapes of the original image. When then initialize a list of bounding boxes. Those lists are key to the undo mechanism as they behave like a buffer: each time a bounding box selection is performed we will append the last image, mask and bounding box created. When we call for _'Undo'_, we will strip the last component of each list. In this way, by selecting only the last component we will obtain the lastest changes. 

#### _Write a callback to handles mouse actions_
Let's now write the callback that will process the mouse actions. 

```python

```

