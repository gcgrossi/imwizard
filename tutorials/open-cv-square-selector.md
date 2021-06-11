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

1. when you click the mouse record ```(xhigh,yhigh)``` coordinates
2. when you release the mouse record the ```(xlow,low)``` coordinates
3. draw a rectangle on the image with OpenCV

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
    def click_and_crop(self,event, x, y, flags, param): 
        # if the left mouse button was clicked, record the starting
        #( x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.pt = [(x, y)]
            self.cropping = True
        
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            #record the ending (x, y) coordinates and indicate that
            #the cropping operation is finished
            self.pt.append((x, y))
            self.cropping = False
            
            # pushes to the images list to handle undo
            self.image.append(self.image[-1].copy())
            self.mask.append(self.mask[-1].copy())
            self.bbox.append((self.pt[0],self.pt[1]))
            
            # draw a rectangle around the region of interest
            cv2.rectangle(self.image[-1], self.pt[0], self.pt[1], (0, 255, 0), 2)
            cv2.rectangle(self.mask[-1],  self.pt[0], self.pt[1], 255,-1)
            
            cv2.imshow("image", self.image[-1])
            return
```

Let's analyse the code. the function click and crop will be called each time a mouse action happens. If the action is _'Click left button'_ (```cv2.EVENT_LBUTTONDOWN```) the x,y coordinates are stored as a 2-tuple into the corresponing list. When the action is '_Left button released_' (```cv2.EVENT_LBUTTONUP```) different actions take place:

1. the (x,y) coordinates are pushed to the points list and to the bounding box list.
2. the image and mask list is updated with the copy of the lastest element in the list.
3. a rectangle is drawn on the latest component of the image and mask list.
4. Finally the newly updated image (the last component of the list) is shown.

In this way we are sure all the changes will be stored in memory by constantly pushing a list with the modified image and coordinates of the bounding boxes. We need just to write a function to handle the callback. 

#### _Show the image with mouse callback_

The complete function looks like this:

```python
    def square_selector(self):
        # a mouse callback
        # passes the mouse actions to the callback
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)
        
        # keep looping until the 'v' key is pressed
        while True:
            # disisplay the last stored image and wait for a keypress
            cv2.imshow("image", self.image[-1])
            key = cv2.waitKey(1) & 0xFF
            
            # if the 'r' key is pressed, delete the last image/mask
            # restores the last action performed on image/mask
            if key == ord("r"):
                del self.image[-1]
                del self.mask[-1]
                del self.bbox[-1]
               
            # if f the 'c' key is pressed, break from the loop
            elif key == ord("v"):
                break
                    
        # show mask for output control
        cv2.imshow("mask", self.mask[-1])
        cv2.waitKey(0)
        
        # cleanup
        self.clean() 
        return (self.mask[-1],self.bbox[-1])
```

Let's break it down in pieces. We first create a new window using OpenCV and name it 'image'. On the window we set mouse callback to be the function we just defined. We then start a infinite loop showing only the last image in the buffer and we wait of a key to be pressed. If the key "_r_" is pressed the "_Undo_" is triggered and the last element stored in the buffer is removed. if the key "_v_" (for validate) is pressed, the loop is stopped, the last image in the buffer is shown. We then call a function called ```clean()``` to reset the session:
  
```python
    def clean(self):
        # close all open windows and reset original image
        cv2.destroyAllWindows()
        self.image = [self.clone.copy()]
        return
```

The function will destroy all the windows and re-instantiate the original image. Finally the mask and the bounding boxes are returned.

#### _Usage_

After reading an image with OpenCV, you can initialize and call the selctor function in this way:
```python
import cv2

# Load Image and Prepare for processing
img = cv2.imread("path_to_image")

# Obtain mask and bounding box with a manual region selector
ss = SquareSelector(image)
mask,bbox = ss.square_selector()
```
