# DETECTING RED/GREEN NAVIGATIONAL BUOYS
# 31 MARCH 2022
# AUTHOR: Pearson Frank
# adapted from code by sydbelt & lexskeen
import numpy as np
import cv2
from Buoy import Buoy


class Identifier:
    # define ranges for red, green, blue, yellow
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    yellow_lower = np.array([20, 100, 100], np.uint8)
    yellow_upper = np.array([30, 255, 255], np.uint8)

    def __init__(self):
        self.cam = cv2.VideoCapture(0)  # start the camera
        self.width = int(self.cam.get(3))
        self.height = int(self.cam.get(4))

    def destroy(self):
        self.cam.release()

    # main method to return buoys
    def get_closest_buoys(self):
        r, g, y = self.read_frame()
        # dictionary of closest buoys
        return {'Red': r[0] if r else None, 'Green': g[0] if g else None, 'Yellow': y[0] if y else None}

    # read a single frame
    def read_frame(self):
        __, image_frame = self.cam.read()  # read a frame from the image
        shape = image_frame.shape  # dimensions of image
        total_area = shape[0] * shape[1]  # is there a difference between size and imageFrame shape?
        min_area = (1 / 32) * total_area  # empirically determined
        max_area = (1 / 4) * total_area
        # print(total_area, min_area, max_area)

        # ?
        reds = set()
        greens = set()
        yellows = set()

        # Convert the imageFrame in BGR(RGB color space) to HSV(hue-saturation-value) color space
        hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

        # create masks
        red_mask = cv2.inRange(hsv_frame, Identifier.red_lower, Identifier.red_upper)
        green_mask = cv2.inRange(hsv_frame, Identifier.green_lower, Identifier.green_upper)
        blue_mask = cv2.inRange(hsv_frame, Identifier.blue_lower, Identifier.blue_upper)
        yellow_mask = cv2.inRange(hsv_frame, Identifier.yellow_lower, Identifier.yellow_upper)

        # just cv things
        kernal = np.ones((5, 5), "uint8")
        red_mask = cv2.dilate(red_mask, kernal)
        green_mask = cv2.dilate(green_mask, kernal)
        blue_mask = cv2.dilate(blue_mask, kernal)
        yellow_mask = cv2.dilate(yellow_mask, kernal)

        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # __, contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if max_area > area > min_area:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + (w / 2), y + (h / 2))
                reds.add((w*h, center[0], center[1]))
                print("Red", x, y, w, h)

        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # __, contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if max_area > area > min_area:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + (w / 2), y + (h / 2))
                greens.add((w*h, center[0], center[1]))
                print("Green", center, w, h)

        # Creating contour to track blue color
        contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # __, contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if max_area > area > min_area:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + (w / 2), y + (h / 2))
                # not a buoy
                print("Blue", center, w, h)

        # Creating contour to track yellow color
        contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # __, contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if max_area > area > min_area:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + (w / 2), y + (h / 2))
                yellows.add((w*h, center[0], center[1]))
                print("Yellow", center, w, h)

        # return a sorted list of buoys
        return sorted(reds, reverse=True), sorted(greens, reverse=True), sorted(yellows, reverse=True)

