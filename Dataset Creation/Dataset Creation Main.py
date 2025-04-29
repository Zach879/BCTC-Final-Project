#Zachary Reese ~ Last Edit: 4/8/2021 ~ This program creates a synthetic dataset for the CNN model to train and test off of.
import PIL
from PIL import Image, ImageFont, ImageDraw, ImageChops
import random
import os
import shutil
import cv2
import numpy as np
import pathlib
originalFileLocation, tail = os.path.split(pathlib.Path(__file__).parent.absolute())

max = 30 #120
ratio = 0.8 #Percentage of Train to Test
boxsize = 60 #original character image size
datasetfolderpath = "D:\\testrandomdataset\\"
pathsuffixTrain = "Train"
pathsuffixTest = "Test" #Data file locations
tempImageFolderPath = originalFileLocation + "\\Dataset Creation\\TempImage.png"
                                                                                                                                                                                                                                                                                                                    #single slash is used for string commands, double slash outputs as a singular slash
characters = ['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[','\\',']','^','_','`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','{','|','}','~']
fonts = ["arial.ttf", "baskvl.ttf", "SansSerifExbFLFCond.ttf", "BitterPro-BoldItalic.ttf", "Jura-VariableFont_wght.ttf", "ArialCE.ttf", "ArialCEBold.ttf", "ArialCEBoldItalic.ttf", "ArialCEItalic.ttf", "georgia bold italic.ttf", "georgia bold.ttf", "georgia italic.ttf", "Georgia.ttf", "OpenSans-Regular.ttf", "times new roman bold italic.ttf", "times new roman bold.ttf", "times new roman italic.ttf", "times new roman.ttf", "Verdana Bold.ttf", "Verdana.ttf", "arial.ttf", "times new roman.ttf"]
white = [255,255,255]
print("length: " + str(len(characters)))

maxTrain = max * ratio
maxTest = max * (1 - ratio)

if os.path.exists(datasetfolderpath + pathsuffixTrain): #resets output folders
    shutil.rmtree(datasetfolderpath + pathsuffixTrain)
if os.path.exists(datasetfolderpath + pathsuffixTest):
    shutil.rmtree(datasetfolderpath + pathsuffixTest)
os.makedirs(datasetfolderpath + pathsuffixTrain)
os.makedirs(datasetfolderpath + pathsuffixTest)

def getRandom():
    return random.randrange(1,7)

def trim(): #Removes any whitespace around character
    img = cv2.imread(tempImageFolderPath) # Read in the image and convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
    coords = cv2.findNonZero(gray) # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
    rect = img[y:y+h, x:x+w] # Crop the image
    return rect
    
for character in characters: #Creates training dataset
    current = 0
    while current < maxTrain:
        im = PIL.Image.new(mode = "1", size = (boxsize, boxsize), color = 1)
        draw = ImageDraw.Draw(im) #Initializes PIL drawing image
        fontstyle = fonts[random.randrange(0,len(fonts) - 1,1)] #Gets random font
        while character == 'I' and (fontstyle == "ArialCEBoldItalic.ttf" or fontstyle == "ArialCEItalic.ttf"): #Fixes known bugged characters in certain fonts
            fontstyle = fonts[random.randrange(0,len(fonts) - 1,1)]
        for font_size in range(50, 1, -1): #Gets proper font size to fit in PIL drawing image
            font = ImageFont.truetype(fontstyle, font_size)
            if font.getsize(character)[0] <= boxsize:
                font = ImageFont.truetype(fontstyle, (font_size - random.randrange(0, 5)))
                break
        font = ImageFont.truetype(fontstyle, font_size)
        draw.text((0, 0), character, 0, font=font) #Draws character on PIL drawing image
        #im.save(tempImageFolderPath)
        im = trim()
        im = cv2.copyMakeBorder(im, getRandom(), getRandom(), getRandom(), getRandom(), cv2.BORDER_CONSTANT,value=white) #Adds random sized padding to character image
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #Makes image black and white
        im = cv2.resize(im, (32, 32))
        if os.path.exists(datasetfolderpath + pathsuffixTrain + "\\" + str(ord(character))): #If character folder already exists
            cv2.imwrite(datasetfolderpath + pathsuffixTrain + "\\" + str(ord(character)) + "\\" + str(current) + ".png", im)
        else: #If character folder doesn't exist
            os.makedirs(datasetfolderpath + pathsuffixTrain + "\\" + str(ord(character)))
            cv2.imwrite(datasetfolderpath + pathsuffixTrain + "\\" + str(ord(character)) + "\\" + str(current) + ".png", im)
        current += 1
    print("Train: " + character + " (" + str(ord(character)) + ")")

total = 0
for character in characters: #Creates testing dataset
    current = 0
    while current < maxTest:
        im = PIL.Image.new(mode = "1", size = (boxsize, boxsize), color = 1)
        draw = ImageDraw.Draw(im) #Initializes PIL drawing image
        fontstyle = fonts[random.randrange(0,len(fonts) - 1,1)] #Gets random font
        while character == 'I' and (fontstyle == "ArialCEBoldItalic.ttf" or fontstyle == "ArialCEItalic.ttf"): #Fixes known bugged characters in certain fonts
            fontstyle = fonts[random.randrange(0,len(fonts) - 1,1)]
        for font_size in range(50, 1, -1): #Gets proper font size to fit in PIL drawing image
            font = ImageFont.truetype(fontstyle, font_size)
            if font.getsize(character)[0] <= boxsize:
                font = ImageFont.truetype(fontstyle, (font_size - random.randrange(0, 5)))
                break
        font = ImageFont.truetype(fontstyle, font_size)
        draw.text((0, 0), character, 0, font=font) #Draws character on PIL drawing image
        #im.save(tempImageFolderPath)
        im = trim()
        im = cv2.copyMakeBorder(im, getRandom(), getRandom(), getRandom(), getRandom(), cv2.BORDER_CONSTANT,value=white) #Adds random sized padding to character image
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #Makes image black and white
        im = cv2.resize(im, (32, 32))
        cv2.imwrite(datasetfolderpath + pathsuffixTest + "\\" + str(total) + ".png", im)
        current += 1
        total += 1
    print("Test: " + character + " (" + str(ord(character)) + ")")
    
print("finished")
cv2.waitKey(0)