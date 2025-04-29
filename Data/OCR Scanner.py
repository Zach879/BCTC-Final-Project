#Zachary Reese ~ Last Edit: 4/8/2021 ~ Takes the source image of a paragraph and splits it into lines. Then, using the contours of the pixels in the picture of a line, estimates the Region Of Interest of each character. Next, the estimated results are narrowed down and refined to create more accurate images of each character by using a complex series of algorithms. Finally, the trained CNN model evaluates the estimated images of each character, giving the results back to the hub while communicating the status.
import numpy as np
import argparse
import imutils
import cv2
from tensorflow.keras.models import load_model
from imutils.contours import sort_contours
from PIL import Image
import os
import shutil
import numpy
import sys
import pathlib
originalFileLocation, tail = os.path.split(pathlib.Path(__file__).parent.absolute())

model = load_model(originalFileLocation + "\\Character Determiner\\character_recognizer2.h5") #loads trained CNN model

#sourceImage = cv2.imread("D:\\10-12th Grade\\Projects\\Senior Project\\TextbookLine.png")
sourceImage = cv2.imread(originalFileLocation + "\\Data\\Original.png")

graycv2ImageLocation = originalFileLocation + "\\graycv2Image.png" #temporary storage location

white = 255 #[255,255,255]
black = 0 #[0,0,0]
gray = cv2.cvtColor(sourceImage, cv2.COLOR_BGR2GRAY) #converts image to grayscale
sourceImage = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] #makes image black and white only
pilSourceImage = Image.fromarray(sourceImage) #converts cv2 image to pil
sourceWidth, sourceHeight = pilSourceImage.size

indexAccumulator = 0
content = []
with open(originalFileLocation + "\\Data\\Status.txt") as f:
    content = f.readlines()
indexAccumulator = int(content[1])

with open(originalFileLocation + "\\Data\\Status.txt", 'a') as f:
    f.write("Initializing Process\n")
    f.write("0")

def GetPadded(x, y, w, h): #takes the Region Of Interest and splits it into a 32x32 cropped portion with padding.
    roi = gray[y:y + h, x:x + w]

    thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] #gets image thresh (binary black and white)
    if (w >= 5 and w <= 150) and (h >= 5 and h <= 120): #Only uses images that are a certain size
        (tH, tW) = thresh.shape

        if tW > tH:
            thresh = imutils.resize(thresh, width=32)      
        else:
            thresh = imutils.resize(thresh, height=32)
    
    (tH, tW) = thresh.shape
    dX = int(max(0, 32 - tW) / 2.0)
    dY = int(max(0, 32 - tH) / 2.0) #properly resizes the image to be less pixelized
    padded = cv2.copyMakeBorder(thresh, top=dY + 3, bottom=dY + 3, left=dX + 3, right=dX + 3, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255)) #adds padding around image
    padded = cv2.resize(padded, (32, 32))
    return padded

def GetTranslatedOutput(output): #Translates CNN output to readable character output
    if output >= 0 and output <= 26:
        return output + 100
    else:
        return output + 6

def getNewCords(x1, y1, w1, h1, x2, y2, w2, h2): #Given two different ROIs, this calculates the new ROI for a combination of the two images
    newX = 0
    newY = 0
    newWidth = 0
    newHeight = 0
    newY = y1 if y1 <= y2 else y2
    newHeight = (y1 + h1) - newY

    newX = x1 if x1 <= x2 else x2
    rightMostX = (x1 + w1) if (x1 + w1) >= (x2 + w2) else (x2 + w2)
    newWidth = rightMostX - newX

    return (newX, newY, newWidth, newHeight)

def findSplitRange(x, y, w, h): #Finds a line of white pixels in the y-axis to determine if there's multiple chars in the image. If so, then returns the X-axis at which the white pixels are found in the y-axis
    leftBlackPixel = -1
    rightBlackPixel = -1
    leftWhitePixel = -1
    dobreak = False

    for accumulatorX in range(x, x + w):
        if dobreak:
            dobreak = False
            break
        for accumulatorY in range(y, y + h):
            if (pilimage.getpixel((accumulatorX, accumulatorY)) != white):
                leftBlackPixel = accumulatorX
                dobreak = True
    
    for accumulatorX in range(x + w, x, -1):
        if dobreak:
            dobreak = False
            break
        for accumulatorY in range(y, y + h):
            if (pilimage.getpixel((accumulatorX, accumulatorY)) != white):
                rightBlackPixel = accumulatorX
                dobreak = True
    
    if (leftBlackPixel == -1 or rightBlackPixel == -1):
        return (-1)
    else:
        for accumulatorX in range(leftBlackPixel, rightBlackPixel):
            if dobreak:
                dobreak = False
                break
            blackFound = False
            for accumulatorY in range(y, y + h):
                if (pilimage.getpixel((accumulatorX, accumulatorY)) != white):
                    blackFound = True
            if blackFound == False:
                leftWhitePixel = accumulatorX
                dobreak = True

        return leftWhitePixel

def onlyWhite(xValue):  #detects any non-white pixels and returns False if one is found
    accumulatorY = 0
    for accumulatorY in range(0, imHeight):
        if pilimage.getpixel((xValue, accumulatorY)) != white:
            return False
    return True

def GetLineYCords(startPixel): #Gets the y-cords of a new line
    if startPixel >= sourceHeight - 1:
        return (-1, -1)
    else:
        blackFoundAt = -1
        whiteLineFoundAt = -1
        for accumulatorY in range(startPixel, sourceHeight):
            if blackFoundAt != -1:
                break
            for accumulatorX in range(0, sourceWidth):
                if pilSourceImage.getpixel((accumulatorX, accumulatorY)) == black:
                    blackFoundAt = accumulatorY
                    break
        
        if blackFoundAt != -1:
            dobreak = False
            for accumulatorY in range(blackFoundAt + 1, sourceHeight):
                if dobreak:
                    break
                blackFound = False
                for accumulatorX in range(0, sourceWidth):
                    if pilSourceImage.getpixel((accumulatorX, accumulatorY)) != white:
                        blackFound = True
                if blackFound == False:
                    whiteLineFoundAt = accumulatorY
                    dobreak = True
            if whiteLineFoundAt == -1:
                whiteLineFoundAt = sourceHeight - 1
            return (blackFoundAt, whiteLineFoundAt)
        return (-1, -1)

def ChangeStatus(statusMessage, percentageComplete): #Changes status text file to update the Senior Project Hub
    if percentageComplete == 500:
        percentageComplete = 100
    elif percentageComplete > 100:
        percentageComplete = 99
    with open(originalFileLocation + "\\Data\\Status.txt",'w',encoding = 'utf-8') as file:
        file.write(statusMessage + "\n")
        file.write(str(percentageComplete))
    file.close()
    if percentageComplete == -1:
        sys.exit()

def GetBinaryImage(x, y, w, h):
    padded = GetPadded(x, y, w, h)
    cv2.imwrite(graycv2ImageLocation, padded)

    temp = cv2.imread(graycv2ImageLocation)
    temp = np.reshape(temp,[1,32,32,3]) #format image to be used in trained CNN
    temp = np.array(temp, dtype=np.float32) / 255.0
    return temp

def GetBinarizedPadded(x, y, w, h):
    padded = GetPadded(x, y, w, h)
    padded = padded.astype("float32") / 255.0
    padded = np.expand_dims(padded, axis=-1)
    return padded

try:
    percentageComplete = 0
    with open(originalFileLocation + "\\Data\\Status.txt",'w',encoding = 'utf-8') as file:
        file.write("Sectioning Image Into Lines\n")
        file.write(str(0))  #Writes first message into status text document
    file.close()

    totalImageAccumulator = 0
    images = [] #holds line images
    newLineEnd = 0
    while(newLineEnd <= sourceHeight - 1 and newLineEnd != -1): #splits original source image into lines
        newLineStart, newLineEnd = GetLineYCords(newLineEnd)
        if newLineStart != -1:
            croppedPil = pilSourceImage.crop((0, newLineStart, sourceWidth - 1, newLineEnd))
            openCVImage = cv2.cvtColor(numpy.array(croppedPil), cv2.COLOR_RGB2BGR) #Converts PIL Image to cv2 Image and converts RGB to BGR
            openCVImage = cv2.copyMakeBorder(openCVImage,5,5,5,5,cv2.BORDER_CONSTANT,value=[255,255,255])
            images.append(openCVImage)
            wtest, htest = croppedPil.size

    for image in images: #for each line in paragraph
        lineStatusMessage = " (Line " + str(totalImageAccumulator + 1) + "/" + str(len(images)) + ")"
        percentageComplete += (100 // len(images)) // 10
        ChangeStatus("Editing Image Properties and Guessing Character Locations" + lineStatusMessage, percentageComplete)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converts line to grayscale
        blurred = cv2.GaussianBlur(gray, (5, 5), 0) #add blur

        edged = cv2.Canny(blurred, 30, 150) #removes blur (improves image quality slightly)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finds image contours
        cnts = imutils.grab_contours(cnts) #make contours into images
        cnts = sort_contours(cnts, method="left-to-right")[0] #sorts contours from left to right

        chars = [] #holds binarized images and dimensions
        binaryImages = [] #holds binarizied images
        charDimensions = [] #holds dimensions
        charImages = [] #holds unchanged images

        percentageComplete += (100 // len(images)) // 10
        ChangeStatus("Character Binarization" + lineStatusMessage, percentageComplete)
        for c in cnts: #for each contour image
            (x, y, w, h) = cv2.boundingRect(c) #get contour image's location and dimensions
                #w >= 5; h >= 15
            padded = GetPadded(x, y, w, h)

            charImages.append(padded)

            charDimensions.append((x, y, w, h))

        accumulator = 0
        accumulator2 = 0
        
        percentageComplete += (100 // len(images)) // 10
        ChangeStatus("Refining Character Accuracy" + lineStatusMessage, percentageComplete)

        if len(charDimensions) >= 2:
            while accumulator >= 0 and accumulator < len(charImages):    #combines boxes when other boxes are above and touching the 1st box
                if accumulator < len(charImages): #REMOVE??
                    (xcord, ycord, width, height) = charDimensions[accumulator]
                    set1 = set({xcord})
                    for setAccumulator in range(xcord, xcord + width):
                        set1.add(setAccumulator)
                    for accumulator2 in range(accumulator - 2, accumulator + 3):
                        if accumulator != accumulator2 and accumulator2 < len(charImages) and accumulator2 > -1: #if box 2 is above box 1
                            (xcord2, ycord2, width2, height2) = charDimensions[accumulator2]
                            rayDetection = False
                            rayAccumulator = xcord2
                            rayDetectionCount = 0
                            while (rayDetection == False and rayAccumulator < width2 + xcord2):
                                if (rayAccumulator in set1):
                                    rayDetectionCount += 1
                                    if (rayDetectionCount >= 3): #if there are at least 3 pixels in box 2 above box 1 then merge box 1 and box 2
                                        if (ycord + height >= ycord2 + height2 and ycord >= ycord2):
                                            (newX, newY, newWidth, newHeight) = getNewCords(xcord, ycord, width, height, xcord2, ycord2, width2, height2)
                                            padded = GetPadded(newX, newY, newWidth, newHeight)
                                            charImages[accumulator] = padded                                           
                                            charImages.pop(accumulator2)
                                            charDimensions[accumulator] = (newX, newY, newWidth, newHeight)
                                            charDimensions.pop(accumulator2)
                                            accumulator -= 1
                                        rayDetection = True
                                rayAccumulator += 1
                accumulator += 1

            percentageComplete += (100 // len(images)) // 10
            ChangeStatus("Removing Characters Inside Other Characters" + lineStatusMessage, percentageComplete)

            accumulator = 0
            accumulator2 = 0
            for accumulator in range (0, len(charImages) - 1):    #removes boxes completely inside boxes; most of the time not required, but is a more efficient solution for larger images where boxes can remain inside boxes despite the previous check
                if accumulator < len(charImages):
                    (xcord, ycord, width, height) = charDimensions[accumulator]
                    for accumulator2 in range(accumulator - 2, accumulator + 2):
                        if accumulator2 < len(charImages):
                            (xcord2, ycord2, width2, height2) = charDimensions[accumulator2]
                            if accumulator != accumulator2 and width >= width2 and height >= height2 and ycord <= ycord2 and ycord + height >= ycord2 + height2 and xcord <= xcord2 and xcord + width >= xcord2 + width2:
                                charDimensions.pop(accumulator2)
                                charImages.pop(accumulator2)

        cv2image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        pilimage = Image.fromarray(cv2image) #used for getting image size and color at pixel coordinates

        percentageComplete += (100 // len(images)) // 10
        ChangeStatus("Splitting Multi-Char Images" + lineStatusMessage, percentageComplete)

        #seperates images with multiple chars by splitting the chars if there is space between the chars
        accumulator = 0
        while accumulator < len(charImages):
            (x, y, w, h) = charDimensions[accumulator]
            leftWhitePixel = findSplitRange(x, y, w, h)
            if leftWhitePixel != -1:
                x, y, w, h = charDimensions[accumulator]
                newY1 = y
                newY2 = y
                newHeight1 = h
                newHeight2 = h
                newX1 = x
                newX2 = leftWhitePixel
                newWidth1 = leftWhitePixel - x
                newWidth2 = (x + w) - leftWhitePixel

                #first (left) char
                padded = GetPadded(newX1, newY1, newWidth1, newHeight1)
                charImages[accumulator] = padded               
                charDimensions[accumulator] = (newX1, newY1, newWidth1, newHeight1)

                #second (right) char
                padded = GetPadded(newX2, newY2, newWidth2, newHeight2)
                charImages.insert(accumulator + 1, padded)                
                charDimensions.insert(accumulator + 1, (newX2, newY2, newWidth2, newHeight2)) 

                accumulator -= 2
            accumulator += 1

        percentageComplete += (100 // len(images)) // 10
        ChangeStatus("Detecting Whitespace" + lineStatusMessage, percentageComplete)
        imWidth, imHeight = pilimage.size

        spaces = []
        firstWhiteLine = -1
        accumulatorX = 0
        for accumulatorX in range(0, imWidth): #detects the spaces between characters
            if onlyWhite(accumulatorX):
                if firstWhiteLine == -1:
                    firstWhiteLine = accumulatorX
            elif firstWhiteLine != -1:
                if accumulatorX - firstWhiteLine >= 5:
                    spaces.append((firstWhiteLine, accumulatorX - 1))
                firstWhiteLine = -1

        #removes any images that are 95%+ white or black
        pixelCount = 1024 #32 * 32
        accumulator = 0
        while accumulator < len(charImages):
            whitePixelCount = np.sum(charImages[accumulator] == 255)
            blackPixelCount = np.sum(charImages[accumulator] == 0)
            if whitePixelCount / pixelCount >= 0.95 or blackPixelCount / pixelCount >= 0.95:
                charDimensions.pop(accumulator)
                charImages.pop(accumulator)
            accumulator += 1

        for accumulator in range(0, len(charDimensions)): #makes all char images binary (useable input for neural network)
            (x, y, w, h) = charDimensions[accumulator]
            binaryImages.append(GetBinaryImage(x, y, w, h))

            chars.append((GetBinarizedPadded(x, y, w, h), (x, y, w, h)))

        boxes = [b[1] for b in chars] #gets the top, bottom, left, and right of the bounding boxes of each character

        chars = np.array([c[0] for c in chars], dtype="float32")

        percentageComplete += (100 // len(images)) // 10
        ChangeStatus("Getting Neural Network Results" + lineStatusMessage, percentageComplete)

        preds = []
        for char in binaryImages:
            #preds.append(GetTranslatedOutput(model.predict_classes(char))) #predict_classes not found?
            predict_x = model.predict(char)
            #print("kkkkkkkkkkkkkkkk: " + str(predict_x))
            preds.append(GetTranslatedOutput(np.argmax(predict_x,axis=1)))
            #print("mmmmmmmmmmmmmmmmmm: " + str(GetTranslatedOutput(np.argmax(predict_x,axis=1))))

                #determines an underscore from a minus sign
        width, height, _ = image.shape
        height = int(height * 0.8)
        for accumulator in range(0,len(preds)):
            if preds[accumulator] == 45:
                (x, y, w, h) = charDimensions[accumulator]
                if x >= height:
                    preds[accumulator] = 95
        for accumulator in range(0,len(preds)):         #STRANGELY ERRORS (with bottom loop)!!!
            if preds[accumulator] == 95:
                (x, y, w, h) = charDimensions[accumulator]
                if x < height:
                    preds[accumulator] = 45
        
        #determines a double quote from a single quote
        #while accumulator < len(preds - 1):              #STRANGELY ERRORS!!!
        #    if preds[accumulator] == 39 and preds[accumulator + 1] == 39:
        #        accumulator2 = accumulator + 1
        #        (xcord, ycord, width, height) = charDimensions[accumulator]
        #        (xcord2, ycord2, width2, height2) = charDimensions[accumulator2]
        #        (newX, newY, newWidth, newHeight) = getNewCords(xcord, ycord, width, height, xcord2, ycord2, width2, height2)
        #        padded = GetPadded(newX, newY, newWidth, newHeight)
        #        charImages[accumulator] = padded                                           
        #        charImages.pop(accumulator2)
        #        charDimensions[accumulator] = (newX, newY, newWidth, newHeight)
        #        charDimensions.pop(accumulator2)
        #        binaryImages[accumulator] = GetBinaryImage(newX, newY, newWidth, newHeight)
        #        binaryImages.pop(accumulator2)
        #        chars[accumulator] = (GetBinarizedPadded(newX, newY, newWidth, newHeight), (newX, newY, newWidth, newHeight))
        #        chars.pop(accumulator2)
        #    accumulator += 1

        percentageComplete += (10 // len(images))
        ChangeStatus("Drawing Character Bounding Boxes and Whitespace" + lineStatusMessage, percentageComplete)

        for (pred, (x, y, w, h)) in zip(preds, boxes):
            #label = str(pred[0]) + " (" + str(chr(pred[0])) + ")"
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) #draws bounding box on line image
            #cv2.putText(image, label, (x + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)         clutters image

        for acc in range(0, len(spaces)): #writes spaces on line image
            start, end = spaces[acc]
            cv2.rectangle(image, (start, imHeight//2), (end, imHeight//2 + 2), (0, 0, 255), 2)

        for pred in preds: #prints all results onto command line (when run on visual studio code)
            pred = pred
            try:
                print(str(pred) + " " + chr(pred[0]))
            except:
                print(str(pred) + " " + chr(pred))
            #print(str(pred) + " " + chr(pred[0]))

        #cv2.imshow("Image" + str(totalImageAccumulator), image)

        percentageComplete += (100 // len(images)) // 10
        ChangeStatus("Sorting Characters" + lineStatusMessage, percentageComplete)

        characterList = []
        accumulator = 0
        for accumulator in range(0, len(charDimensions)): #adds x value of each character to characterList
            (x, y, w, h) = charDimensions[accumulator]
            characterList.append(x)
        accumulator = 0
        for accumulator in range(0, len(spaces)): #adds x value of each space to characterList
            (startX, endX) = spaces[accumulator]
            characterList.append(startX)

        characterList.sort()
        mainCharacterList = []
        accumulator1 = 0
        accumulator2 = 0
        accumulator3 = 0 
        for accumulator1 in range(0, len(characterList)): #because each starting x value is unique for characters and spaces on each line, the x values are sorted from least to greatest (left to right) and then replaced with the CNN results for their corresponding character image
            blnFound = False
            for accumulator2 in range(0, len(preds)):
                (x, y, w, h) = charDimensions[accumulator2]
                if characterList[accumulator1] == x:
                    try:
                        mainCharacterList.append(str(chr(preds[accumulator2][0])))
                    except:
                        mainCharacterList.append(str(chr(preds[accumulator2])))
                    #mainCharacterList.append(str(chr(preds[accumulator2][0])))
                    blnFound = True
            if blnFound == False:
                for accumulator3 in range(0, len(spaces)):
                    (startX, endX) = spaces[accumulator3]
                    if characterList[accumulator1] == startX:
                        mainCharacterList.append(" ")
        
        cv2.imwrite(originalFileLocation + "\\Data\\BoundingBoxes\\BoundingBoxImage" + str(totalImageAccumulator+ indexAccumulator) + ".png", image)
        
        #Saves results to file
        combinedChars = ""
        for character in mainCharacterList:
            combinedChars += character
        
        resultsFileLocation = originalFileLocation + "\\Data\\Results.txt"

        if totalImageAccumulator == 0:
            with open(resultsFileLocation, 'w') as file: #creates a new file if it doesn't already exist
                file.write(combinedChars)
        else:
            with open(resultsFileLocation, 'a') as file: #appends to the file if it already exists
                if totalImageAccumulator == 0:
                    file.write(combinedChars)
                else:
                    file.write("\n" + combinedChars)       
        
        totalImageAccumulator += 1
    percentageComplete = 500
    ChangeStatus("Finishing Data Transfer and Interpretation" + lineStatusMessage, percentageComplete)
    #cv2.waitKey(0)
except Exception as e:
    print (str(e))
    ChangeStatus("An unknown error has occurred. Restarting process...", -1)