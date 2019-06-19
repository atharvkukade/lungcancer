import cv2
import numpy as np

class FeatureExtractor:

    def extractfeaturs(self,tumourspotimage):

        contours, hierarchy = cv2.findContours(tumourspotimage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        areas = []

        for c in contours:
            if (cv2.contourArea(c) != 0):
                areas.append(cv2.contourArea(c))

        maxWhiteSpotArea = 0
        minWhiteSpotArea = 0
        for pix in areas:
            maxWhiteSpotArea = np.max(areas)
            minWhiteSpotArea = np.min(areas)

        # print("No of white spots    :   ", len(contours))

        totalNumOfWhiteSpots = len(contours)
        totalWhiteSpotArea = 0
        totalWhiteSpotPerimetre = 0
        totalPixelsLessThanThirtyFive = 0
        totalPixelsGreaterThanThirtyFive = 0
        totalPixelsGreaterThanHundred = 0

        for i in range(0, len(contours)):
            cnt = contours[i]
            currentWhiteSpotArea = cv2.contourArea(cnt)
            currentWhiteSpotPerimetre = cv2.arcLength(cnt, True)
            # print("Area of ", (i + 1), "th white spot : ", currentWhiteSpotArea)
            totalWhiteSpotArea += currentWhiteSpotArea
            # print("Perimeter of ", (i + 1), "th white spot : ", currentWhiteSpotPerimetre)
            totalWhiteSpotPerimetre += currentWhiteSpotPerimetre
            if currentWhiteSpotArea < 35:
                totalPixelsLessThanThirtyFive += 1
            elif currentWhiteSpotArea >= 35:
                totalPixelsGreaterThanThirtyFive += 1
            elif currentWhiteSpotArea > 100:
                totalPixelsGreaterThanHundred += 1

        extractedfeatures = dict()

        extractedfeatures['totalNumOfWhiteSpots'] = totalNumOfWhiteSpots
        extractedfeatures['totalWhiteSpotArea'] = totalWhiteSpotArea
        extractedfeatures['totalWhiteSpotLength'] = totalWhiteSpotPerimetre
        extractedfeatures['totalPixelsLessThanThirtyFive'] = totalPixelsLessThanThirtyFive
        extractedfeatures['totalPixelsGreaterThanThirtyFive'] = totalPixelsGreaterThanThirtyFive
        extractedfeatures['totalPixelsGreaterThanHundred'] = totalPixelsGreaterThanHundred
        extractedfeatures['MaxWhiteSpotArea'] = maxWhiteSpotArea
        extractedfeatures['MinWhiteSpotArea'] = minWhiteSpotArea

        return extractedfeatures