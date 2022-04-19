# DETECTING RED/GREEN NAVIGATIONAL BUOYS
# 24 MARCH 2022
# AUTHORS: sydbelt & lexskeen
import numpy as np
import cv2

def findBuoys(imageFrame):
    cam = cv2.VideoCapture(0)
    __, imageFrame = cam.read()
    shape=imageFrame.shape

    total_area=shape[0]*shape[1]
    min_area=(1/32)*total_area
    max_area=(1/4)*total_area
    
    # Convert the imageFrame in BGR(RGB color space) to HSV(hue-saturation-value) color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and define mask
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for green color and define mask
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)    

    # Set range for blue color and define mask
    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # Set range for yellow color and define mask
    yellow_lower = np.array([20, 100, 100], np.uint8)
    yellow_upper = np.array([30, 255, 255], np.uint8)
    yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)
    
    # Morphological Transform, Dilation for each color and bitwise_and operator
    # between imageFrame and mask determines to detect only that particular color
    kernal = np.ones((5, 5), "uint8")
    # For red color
    red_mask = cv2.dilate(red_mask, kernal)
    # For green color
    green_mask = cv2.dilate(green_mask, kernal)
    # For blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    # For yellow color
    yellow_mask = cv2.dilate(yellow_mask, kernal)
    
    for mask in [red_mask, green_mask, blue_mask, yellow_mask]:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for _, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(max_area > area > min_area):
                x, y, w, h = cv2.boundingRect(contour)
                center=(x+(w/2), y+(h/2))

    cam.release()
