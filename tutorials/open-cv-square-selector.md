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



#### _Desciption_

H

```python
def create_contour_mask(c,img):
```
