# -*- coding: utf-8 -*-
"""
Created on Fri May  7 09:50:00 2021
@author: Giulio Cornelio Grossi Ph.D
@email: giulio.cornelio.grossi@gmail.com

The code below implements some useful 
function and classes used to perform
different basic image processing tasks
"""

# Import necessary packages
import cv2
import numpy as np
import plotly.express as px
from scipy.spatial import distance as dist
from plotly.offline import plot
from plotly.subplots import make_subplots

def contour_center(c):
    # - Computes the center of the contour  
    M = cv2.moments(c)
    if M["m00"]>0: 
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
    else:    
        cX=-999
        cY=-999 
    return cX,cY

def create_contour_mask(c,img):
    # - Constructs a mask for the contour
    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    return mask

def mean_std(image,mask):
    # - Calculates mean and std of a masked region
    # - Returns a more handy tuple with the values
    mean, std = cv2.meanStdDev(image, mask=mask)
    m=(mean[0][0],mean[1][0],mean[2][0])
    s=(std[0][0],std[1][0],std[2][0]) 
    return m,s

def min_dist(mean1,mean2):
    # - Find the minimum distance in the L*a*b* space
    #   between a color (2nd input) and a set of colors (1st input)
    # - Returns a tuple with distance and index of the minimum 
   
    # convert to lab
    lab2 = np.zeros((1, 1, 3), dtype="uint8")
    lab2[0]=mean2
    lab2 = cv2.cvtColor(lab2, cv2.COLOR_RGB2LAB)
    
    # loop over the known teeth shades color values
    # compute the minimum distance    
    minDist = (np.inf, None)
    for i,s in enumerate(mean1):
        
       # convert to Lab
       lab1 = np.zeros((1, 1, 3), dtype="uint8")
       lab1[0] = s
       lab1 = cv2.cvtColor(lab1, cv2.COLOR_RGB2LAB)
       
       d=dist.euclidean(lab1,lab2)
       if d<minDist[0]:
           minDist=(d,i)
    return minDist

def process_contours(cnts,image):    
    # - Grabs the center of the contour
    # - Calculates area of contours
    # - Grabs a mask for the contour
    # - Grabs mean and std of the masked region
    # - Returns a dictionary with all contours information
    
    obj={"centers":[],"area":[],"masks":[],"mean":[],"std":[]}
    for i,c in enumerate(cnts):
       obj["centers"].append(contour_center(c))
       obj["area"].append(cv2.contourArea(c))
       mask = create_contour_mask(c,image)
       obj["masks"].append(mask)
       mean, std = mean_std(image,mask)
       obj["mean"].append(mean)
       obj["std"].append(std)
    return obj

def create_shade_square(mean,std,h,w,library="plotly"):
    # number of sigmas from the mean
    # used to draw shading
    nsigma=1
    
    # construct a square with shading
    # h,w is the measure of the square box 
    shade = np.zeros((h,w,3),dtype="uint8") 
    
    # binning equal to the square box height
    bins = range(0,h+1)
    
    # create a linear shading gradient
    # from -3 to +3 sigma
    for j,i in enumerate(range(int(-h/2),int(h/2))):
        # remap range (-h/2,h/2) to (-3,3) sigma
        f = (i/(h/2))*nsigma
        
        # use rgb in plotply and bgr in cv2
        rgb = (mean[2]+f*std[2],mean[1]+f*std[1],mean[0]+f*std[0])
        if library=="cv2": rgb = (mean[0]+f*std[0],mean[1]+f*std[1],mean[2]+f*std[2])
        rgb = tuple(map(lambda x: 255 if x>255 else x, rgb))
        
        # set each bin to a particular value of gradient
        shade[bins[j]:bins[j+1],:]=rgb
    
    return shade

def plot_shade(mean,std,library="plotly"):
    # construct a square with shading
    shade = create_shade_square(mean,std,300,600,library) 
    
    # Draw the actual shade
    # in cv2 or in plotly
    if library=="cv2":
        cv2.imshow("color masked", shade)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif library=="plotly":
        fig = px.imshow(shade)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        plot(fig)
    return

def plot_shade_comparison(shade_dict):
    ncols = 4
    nrows = int(len(shade_dict["mean_bench"][0])/ncols)
    sp=[[{"colspan": ncols},None,None,None]]
    for x in range (0,nrows):
        struct = []
        for y in range(0,ncols):
            struct.append({})
        sp.append(struct)

  
    print(sp)
    fig = make_subplots(rows=nrows+1, cols=ncols, specs=sp,horizontal_spacing = 0.01,vertical_spacing = 0.01,print_grid=True)
    idxmax=shade_dict["mean"][1]
    shade=create_shade_square(shade_dict["mean"][0][idxmax],shade_dict["std"][0][idxmax],300,600)
    fig.add_trace(px.imshow(shade).data[0],row=1, col=1)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
   
    r=2
    c=1
    for i,x in enumerate(shade_dict["mean_bench"][0]):
        if c>ncols:
            r+=1
            c=1
        shade=create_shade_square(shade_dict["mean_bench"][0][i],shade_dict["std_bench"][0][i],50,100)
        fig.add_trace(px.imshow(shade).data[0],row=r, col=c)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        c+=1
    
    fig.update_layout(autosize=False,width=1400,height=800)
    plot(fig)
    return
    
def show_image_masked(image,mask):
    #### Apply mask and draw image    
    output = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow("image", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

def scale_image(image,scale_percent=60):
    # calculate scaling dimensions
    # using percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    # resize image
    scaled = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return scaled

def nothing(x):
    pass

def manual_thresholder(image):  
    # Create a window
    cv2.namedWindow('image')
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # create trackbars for color change
    cv2.createTrackbar('threshold','image',0,255,nothing)
    cv2.createTrackbar('erosion','image',0,255,nothing)

    while(1):
        # read the values from the trackbar
        t = cv2.getTrackbarPos('threshold','image')
        e = cv2.getTrackbarPos('erosion','image')
        
        # create and apply mask
        # with threshold and erode values
        thresh = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY)[1]
        mask = thresh.copy()
        mask = cv2.erode(mask, None, iterations=e)
        output = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow("image", output)

        if cv2.waitKey(1) & 0xFF == ord('x'): break    
    
    cv2.destroyAllWindows()
    return mask

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
        
        # initialize the cropping points and flag
        self.pt = []
        self.cropping=False
        return
    
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
        
    def clean(self):
        # close all open windows and reset original image
        cv2.destroyAllWindows()
        self.image = [self.clone.copy()]
        return
    
    def square_selector(self):
        # a mouse callback to crop function
        # passes the mouse actions to the callback
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)
        
        # keep looping until the 'q' key is pressed
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
            elif key == ord("c"):
                break
                    
        # show mask for output control
        cv2.imshow("mask", self.mask[-1])
        cv2.waitKey(0)
        
        # cleanup
        self.clean() 
        return (self.mask[-1],self.bbox[-1])
    
class ColorFilter():
    # - The SquareSelector shows the input image
    #   and writes rectangles on user selected areas
    # - Calling the square_selector functiion returns,
    #   at the end of the selction, a mask with the 
    #   selected areas
    # - Built-in undo logic to revert changes
    
    def __init__(self,image):
        #copy original image to handle reset
        self.image = image.copy()
        self.filter="BGR"
        return
    
    def callback(self,value):
        pass
    
    def trackbars(self):
        cv2.namedWindow("Trackbars", 0)
        
        for i in ["MIN", "MAX"]:
            v = 0 if i == "MIN" else 255
            
            for j in self.filter:
                cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, self.callback)
        return
    
    def trackbar_values(self):
        values = []

        for i in ["MIN", "MAX"]:
            for j in self.filter:
                v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
                values.append(v)

        return values
    
    def color_filter(self):
        self.image_to_filter = self.image.copy()
        self.trackbars()
        while True:
            v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = self.trackbar_values()
            thresh = cv2.inRange(self.image_to_filter, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
            preview = cv2.bitwise_and(self.image, self.image, mask=thresh)
            cv2.imshow("Preview", preview)
            
            if cv2.waitKey(1) & 0xFF is ord('q'):
                break
            
        cv2.destroyAllWindows()  
        return [(v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max)]
