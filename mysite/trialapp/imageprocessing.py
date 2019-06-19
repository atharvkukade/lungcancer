import cv2
import pickle
import numpy as np

class ImageProcessor:

    def getTumourSpots(self,ctimagepath):

        imgname = ctimagepath.split('/')
        imgstring = str('trialapp/media/ctimages/' + imgname[1])

        #Reading Original Image
        img = cv2.imread(imgstring)
        print(img.shape)

        #Removing extra noise present in the image
        shifted = cv2.pyrMeanShiftFiltering(img, 21, 51)

        gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)

        #Binary Thresholding image
        thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

        #Inverted Binary Threshold Image using as Mask for flood fill
        mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

        #Using Flood Fill Algo For finding Tumour Spots
        h, w = thresh1.shape[:2]
        for row in range(h):
            if mask[row, 0] == 255:
                cv2.floodFill(mask, None, (0, row), 0)
            if mask[row, w - 1] == 255:
                cv2.floodFill(mask, None, (w - 1, row), 0)
        for col in range(w):
            if mask[0, col] == 255:
                cv2.floodFill(mask, None, (col, 0), 0)
            if mask[h - 1, col] == 255:
                cv2.floodFill(mask, None, (col, h - 1), 0)

        holes = mask.copy()

        cv2.floodFill(holes, None, (0, 0), 255)

        holes = cv2.bitwise_not(holes)

        mask = cv2.bitwise_or(mask, holes)

        #Final Extracted Tumour Spots
        masked_img = cv2.bitwise_and(thresh1, thresh1, mask=mask)

        return masked_img
