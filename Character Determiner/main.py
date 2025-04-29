#Zachary Reese ~ Last Edit: 3/25/2021 ~ This program trains a Artificial Neural Network model and saves the trained model for future use.
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.optimizers import SGD
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2
import os
from PIL import Image
from sklearn.model_selection import train_test_split
from keras import utils as np_utils
import keras
import sys
from keras.preprocessing.image import ImageDataGenerator
from keras.models import save_model
from keras.models import load_model
from keras.backend import clear_session

#BCTC DESKTOP
path_train = "C:\\Users\\z_reese\\Desktop\\Characters Dataset\\Train\\"
path_test = "C:\\Users\\z_reese\\Desktop\\Characters Dataset\\Test\\"
test_dataset = "C:\\Users\\z_reese\\Desktop\\Senior Project Test Dataset\\"

#HOME DOCUMENTS
#test_dataset = "C:\\Users\\zcrzc\\OneDrive\\Documents\\Senior Project Test Dataset\\"
#path_train = "C:\\Users\\zcrzc\\OneDrive\\Documents\\Senior Project Dataset\\Train"
#path_test = "C:\\Users\\zcrzc\\OneDrive\\Documents\\Senior Project Dataset\\Test"

#HOME DESKTOP
#test_dataset = "C:\\Users\\zcrzc\\OneDrive\\Desktop\\Senior Project Test Dataset\\"
#path_train = "C:\\Users\\zcrzc\\OneDrive\\Desktop\\Character Dataset\\Train\\" #data file locations
#path_test = "C:\\Users\\zcrzc\\OneDrive\\Desktop\\Character Dataset\\Test\\"

#data augmentation
train_datagen = ImageDataGenerator( #properties for data going into neural network model
    rescale = 1 / 255.0, 
    rotation_range = 5, #20
    zoom_range = 0.00, #0.05
    width_shift_range = 0.00, #0.05
    height_shift_range = 0.00, #0.05
    shear_range = 0.00, #0.05
    horizontal_flip = False,
    fill_mode = "nearest",
    validation_split = 0.20)

test_datagen = ImageDataGenerator(rescale = 1 / 255.0) #black and white

batch_size = 128

train_generator = train_datagen.flow_from_directory( #generates data for neural network model as the model learns
    directory = path_train,
    target_size = (32, 32),
    color_mode = "rgb",
    batch_size = batch_size,
    class_mode = "categorical",
    subset = 'training',
    shuffle = True, #True/False
    seed = 42
)

test_generator = test_datagen.flow_from_directory( #generates data for neural network model as the model 
    directory = path_test,
    target_size = (32, 32),
    color_mode = "rgb",
    batch_size = 1,
    class_mode = None,
    shuffle = False,
    seed = 42
)

def prepare_model(): #Artificial Neural Network model
    model = Sequential()   
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=(32, 32, 3)))
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(94, activation='relu'))
    model.add(Dense(94, activation='softmax'))

    # compile model
    opt = SGD(lr=0.001, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

model = prepare_model()
#trains CNN model
model.fit(train_generator, validation_data = train_generator, steps_per_epoch = train_generator.n//train_generator.batch_size, epochs = 30) #https://keras.io/guides/customizing_what_happens_in_fit/

images = [] #gets extra test data file paths
imagePaths = os.listdir(test_dataset)
for imagePath in imagePaths:
    images.append(test_dataset + imagePath)

testimages = []
for testimage in images: #formats extra test data
    img = cv2.imread(testimage)
    img = cv2.resize(img, (32, 32))
    img = np.reshape(img,[1,32,32,3])
    img = np.array(img, dtype=np.float32) / 255.0
    testimages.append(img)

results = [] #gets results for extra test data
for stuff in testimages:
    results.append(str(model.predict_classes(stuff)))

for morestuff in results: #compares extra test data results to expected results
    splitpath = imagePath.split("_")
    intchar = int(morestuff[1:len(morestuff) - 1]) + 33
    print(morestuff, "  |  ", chr(intchar))

#classes = model.predict_classes(img)
#for item in classes:
#    print(str(item))

print("Save model? (Y/N): ")
    #saves trained CNN model
response = str(input())
if response == 'y' or response == 'Y':
    model.save('character_recognizer1.h5')          #2 is without validation, 1 is with validation
    print("saved")



#helpful links: https://studymachinelearning.com/keras-imagedatagenerator-with-flow_from_directory/
# https://stackoverflow.com/questions/35050753/how-big-should-batch-size-and-number-of-epochs-be-when-fitting-a-model-in-keras
#https://stackoverflow.com/questions/43469281/how-to-predict-input-image-using-trained-model-in-keras