# With help from the code of Mathieu Blondel and Jake Vanderplas

import numpy as np
import matplotlib.pyplot as mpl
from sklearn import linear_model
import file_read_in
import scipy.signal as SP

tempData = file_read_in.readIn('Reduced Burt-C3c SN 20461372 2019-04-10 16_38_07 -0400(1).xlsx')
startList = []
endList = []
peakList = []


def main():
    # This functions finds all of the flagged starts (s), ends (e), and peaks (p). It only takes the first letter:
    # The second letter is the number the start, end, or peak belongs to and is not important.
    # If there are no classifications, this is skipped.
    for i in tempData:
        if i.classification() != '':
            if not isinstance(i.classification(), str):
               i.setClassification('null')
            if i.classification()[0] == 's':
                startList.append(i)
            if i.classification()[0] == 'e':
                endList.append(i)
            if i.classification()[0] == 'p':
                peakList.append(i)

    # find_peaks only works with a matrix of just data. In our current format, tempData returns blocks for each temp.
    # It includes time, classification, etc. We need to strip it down to temp only.
    strippedData = []
    for i in tempData:
        strippedData.append(i.temp())

    # foundPeaks returns a list of indexes.
    foundPeaks = SP.find_peaks(strippedData, prominence=2, distance=20)
    # foundStarts works as below, finding all places that fit the spot which increases by the second argument
    # and decreases by the third
    foundStarts = find_start(strippedData, .4, .2)

    organizedPeaks = []
    organizedStarts = []
    # Now, we take those indexes and put them back in organized form.
    for i in list(foundPeaks[0]):
        organizedPeaks.append(tempData[i])
    for i in foundStarts:
        organizedStarts.append(tempData[i])
    polynomial_regression(tempData, counter=9, startList=startList, endList=endList, peakList=organizedPeaks, calculatedStartList=organizedStarts)
    mpl.legend(loc='upper left')
    mpl.show()


# This functions goal is to produce a polynomial regression for the array given.
# polynomial_regression needs inputs, but can take an extra 3. It needs a startList, endList, and peakList.
# However, you can choose to make those starts, ends, and peaks appear. By default, they do not.
def polynomial_regression(tempArray2D, startList=[], endList=[], peakList=[], calculatedStartList=[], counter=7):
    x = []
    y = []
    # This creates two arrays: an array of all times (X) and an array of all temps (Y)
    for i in tempArray2D:
        x.append(i.myTime)
        y.append(i.myTemp)
    # Creates a line showing all temperature measurements.
    mpl.plot(x, y, color='black', linewidth=2, label="Full Temp")

    # Tracks all start, end, and peak times and marks them.
    startX = []
    startY = []
    endX = []
    endY = []
    peakX = []
    peakY = []
    calcStartX = []
    calcStartY = []

    # Marks starts from startList in *green*.
    for i in startList:
        startX.append(i.time())
        startY.append(i.temp())
    mpl.scatter(startX, startY, color='green', linewidth=3, label="start")

    # Marks ends from endList in *red*.
    for i in endList:
        endX.append(i.time())
        endY.append(i.temp())
    mpl.scatter(endX, endY, color='red', linewidth=3, label="end")

    # Marks peaks from peakList in *blue*.
    for i in peakList:
        peakX.append(i.time())
        peakY.append(i.temp())
    mpl.scatter(peakX, peakY, color='blue', linewidth=3, label='peak')

    # Marks calculated starts from calculatedStartList in *light green*.
    for i in calculatedStartList:
        calcStartX.append(i.time())
        calcStartY.append(i.temp())
    mpl.scatter(calcStartX, calcStartY, color='lightgreen', linewidth=3, label='calculated Starts')

    # The following creates a number of derivatives equal to counter, up to 7.
    colorList=['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'black']
    for counter in range(counter, 8):
        derive = np.polyfit(x, y, counter)
        derive = np.flip(derive)
        mpl.plot(x, create_function(derive, x), color=colorList[counter-2], linewidth=2)

    # We have calculated fairly accurate starts. We are going to derive quadratics from just before
    # the calculated start to just after the peak
    # To do this, we're going to pair every calculated start with its next peak.
    startPointPairs = []
    for i in calculatedStartList:
        found = False
        for j in peakList:
            if not found:
                if i.myTime < j.myTime:
                    startPointPairs.append([i, j])
                    found = True
    print([x[0].myTime(), x[1].myTime] for x in startPointPairs)
    print(startPointPairs)

    # Now we have every start paired with the next peak.
    # Now, we derive along that distance. We're going to give it a little "wiggle room" on both sides.
    trainingList = []
    testList = []
    for i in startPointPairs:
        xRange = x[int(i[0].myTime) - 2: int(i[1].myTime) + 2]
        yRange = y[int(i[0].myTime) - 2: int(i[1].myTime) + 2]
        derive = np.polyfit(xRange, yRange, 5)
        derive = np.flip(derive)
        function = create_function(derive, xRange)
        steepest = findSteepest(yRange, x[int(i[0].myTime) - 2])
        end = pair_start_and_end(int(i[0].myTime), endList, int(i[1].myTime))
        if end != '0':
            trainingList.append([int(i[0].myTime), int(i[1].myTime), steepest, end.myTime])
        else:
            testList.append([int(i[0].myTime), int(i[1].myTime), steepest])


        # For our machine learning algorithm, we want a set of training data and test data.
        # We're going to give both the training and test data all easily available info: start, peak, and highest
        # velocity times.


        # Dummied out: This would print the first instance that the derivative decelerated.
        # Prediction: the start of deacceleration indicated stopping point.
        # Instead, it seemed to always happen in the middle.
        # accel = find_acceleration(function)
        # negAccel = False
        # i = 1
        # while not negAccel and i < len(accel):
            # if accel[i] < 0:
                # print(i, yRange[i])
                # mpl.scatter(xRange[i], yRange[i], color='pink', linewidth=2)
                # negAccel = True
            # i = i + 1
        mpl.plot(xRange, function, color='darkgreen', linewidth=3)
        # linear_model.SGDRegressor().fit(trainingList, testList)




    # Now, we want to take every peak and model a derivative for it. We'll keep it easy and say degree of 4.
    # First, we want to create subarrays from each half.
    # NOTE: This has been artifacted. It is not how this works anymore, but is kept for the sake of posterity.
    # halfPoints = half_split(peakX)
    # splitPointsX = []
    # splitPointsY = []
    # for i in range(1, len(halfPoints)):
        # splitPointsX.append(x[halfPoints[i-1]: halfPoints[i]])
        # splitPointsY.append(y[halfPoints[i-1]: halfPoints[i]])

    # for i in range(0, len(splitPointsX)):
        # derive = np.polyfit(splitPointsX[i], splitPointsY[i], 61)
        # derive = np.flip(derive)
        # mpl.plot(splitPointsX[i], create_function(derive, splitPointsX[i]), color='red', linewidth=2)





# This function takes two arrays: an array of numbers that creates a function in the following order:
# [a, b, c] -> a + bx + c(x^2). This can take any number of exponents.

def create_function(expArray, xArray):
    def function(x):
        counter = 0
        total = 0
        for i in expArray:
            total = total + pow(x, counter)*i
            counter = counter + 1
        return total
    yArray = []
    for i in xArray:
        yArray.append(function(i))
    return yArray


# We want to split all peaks into their own separate quadrants.
# We do this by finding the half points inbetween the peaks.
# For the authors note:Half point between two items is found by: finding the difference between the smaller and larger,
# and then add that to the smaller.
def half_split(peaks):
    halfArray =[]
    for i in range(1, len(peaks)):
        halfArray.append(int(peaks[i-1] + ((peaks[i] - peaks[i-1])/2)))
    return halfArray


# find_start should, by nature, find the beginning of a sudden increase- the start of a shower.
def find_start(numberArray, upDifference, downDifference):
    changearray = []
    increasing = False
    for i in range(0, len(numberArray)-3):
        if not increasing:
            if numberArray[i+3] > numberArray[i]+upDifference:
                changearray.append(i - 4)
                increasing = True
        if increasing:
            if numberArray[i+3] < numberArray[i]-downDifference:
                increasing = False
    return changearray


def find_acceleration(function):
    velocityArray = []
    for i in range(0, len(function)-1):
        velocityArray.append(function[i]-function[i-1])
    accelerationArray=[]
    for i in range(0, len(velocityArray)-1):
        accelerationArray.append(velocityArray[i]-velocityArray[i-1])
    return accelerationArray

def findSteepest(array, add):
    maxx = -1000
    maxi=0
    for i in range(len(array)-1):
        if array[i+1]-array[i] > maxx:
            maxx = array[i+1]-array[i]
            maxi=i
    mpl.scatter(maxi+add-4, array[maxi-4], color='purple', linewidths=1)
    return maxi+add

def pair_start_and_end(startPoint, endPointArray, peakPoint):
    for i in endPointArray:
        if startPoint < i.myTime < peakPoint:
            return i
    return '0'


main()
