

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from numpy import mean
from numpy import std
from matplotlib import pyplot
from sklearn.model_selection import KFold
from keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.layers import BatchNormalization
from keras.models import load_model

#so from what I can tell, https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-from-scratch-for-mnist-handwritten-digit-classification/
#... the  tutorial linked above is missing lots of import lines which are necessary. Also, the tutorial uses the keras...
#...api wheras other tutorials may use tf.keras. The difference is that they have slightly different commands/things ...
#...that need to be imported


def load_dataset():
        (trainX, trainY), (testX, testY) = mnist.load_data() 
        #^The dataset has a train part and a test part,...

        trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
        testX = testX.reshape((testX.shape[0], 28, 28, 1))
		#^I know all the images in the dataset are grayscale so...
		#...I can reshape the data to have a single color channel.

        trainY = to_categorical(trainY)
        testY = to_categorical(testY) 
		#^ "to_categorical" uses one hot encoding which is where an...
		#...integer is converted into a binary vector. One hot...
		#...encoding is crucial for neural networks which use...
		#..categorical data.
        return trainX,trainY,testX,testY
        
# summarize loaded dataset
'''
print('Train: X='+str(trainX.shape)+', y='+str(trainY.shape)) 
print('Test: X='+str(testX.shape)+', y='+str(testY.shape))
'''
#so the above 2 lines just show how many data pieces there are in trainX (60,000) and testX (10,000) and obviously...
#... trainy and testy will be the same sizes as trainX and testX correspondingly as they have the class value for each element.

# plot first few images
'''
for i in range(9):
	# define subplot
	pyplot.subplot(330 + 1 + i)
	# plot raw pixel data
	pyplot.imshow(trainX[i], cmap=pyplot.get_cmap('gray'))
# show the figure
pyplot.show()
'''

#The pixel values for each image in the dataset are unsigned integers from...
#...  0 to 255 as they're grayscale images.
#Neural networks process inputs using small weight values and inputs...
#...with large integer values can slow down...
#... the learning process. Therefore normalising the pixel values so...
# ...that each pixel has a value between 0 and 1 is a good idea.
def normalise_pixels(train,test):
        normalised_train_data=train.astype('float32')
        normalised_test_data=test.astype('float32') 
		#The 2 lines above make the data into the float32 type so...
		#...that after division by 255, they have fractional parts.
        normalised_train_data = normalised_train_data / 255.0
        normalised_test_data= normalised_test_data/ 255.0 
		#The 2 lines above normalises the values to make the range 0-1 as the max value is 255.
        return (normalised_train_data,normalised_test_data)



#BASE MODEL

#The model has 2 main parts:  1. Feature extraction part comprised of convolutional and pooling layers.
#                             2. Classification part which predicts the digit. 

#In this function we define the CNN model.
def define_model(): 

	#FEATURE EXTRACTION PART:

	model = Sequential() 
	#^This tells keras that we are making a sequential model. A sequential model is one in which there...
	#... is a linear stack of layers which you can build up.
	
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
	#^The line above defines the first convolutional layer. It has 32 filters. Conv2D filters in the first...
	#...layer of a CNN...
	#... are used to detect features. The size of each filter is (3,3) which means it is a 3x3 matrix. ...
	#... In 2D cnn's, ...
	#... filters are kernels which are applied across the matrix of the image. The activation='relu' part...
	#...means that the activation used will be of the type ReLU (rectified linear unit). The activation ...
	#...function is the function used to get the output of the node.
	#The kernel initializer is the term for which statistical function/distribution to use for initialising...
	#... the weights.
	#The kernel initialiser I use if 'he_uniform'.
	#The input shape is 28,28,1 as the images in the MNIST dataset are 28 by 28 and have 1 color channel.

	model.add(MaxPooling2D((2, 2)))
	#^The max pooling layer of a CNN is a pooling operation that selects the maximum element from the region...
	#...of the feature map covered by the filter. So the output after the max pooling..
	#..layer would be a (smaller) feature map of the most prominent features of the previous feature map.

	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	#the 2 layers above were added to help increase the depth of the feature extractor layer. 
	
	model.add(BatchNormalization())
	#Batch normalization is used to normalise the outputs of the previous layer.
	#It can help make a neural network faster and more stable.
	  
	model.add(MaxPooling2D((2, 2)))
	#^Another max pooling layer is added to help reduce the dimensions of the feature map and thus reduce the...
	#...number of parameters that will have to be learned by the neural network.
	
	model.add(Flatten())
	#^ The pooled feature map created after the max pooling layer is then flattened so that ...
	#...it can be used to provide features to the classifier.
	#The flatten layer serves as a connection between the convolution and dense layers as the output of...
	#...the flatten layer is then used in the classification part.
	
	#CLASSIFICATION PART:

	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	#^Dense layers are part of the classification part. A dense layer is a layer of neurons where...
	#...each neuron recieves input from all the neurons of the previous layer. The dense layers are...
	#...used to classify the image based on the output from the convolutional layers in the feature...
	#...extraction part. This dense layer uses 100 nodes/neurons to interpret the features.
	
	model.add(Dense(10, activation='softmax'))
	#This is the final dense layer and uses 10 nodes to interpret the features as there are 10 digits, meaning...
	#... 10 nodes...
	#...are needed to allow the classification to be any of the 10 digits. This layer uses 'softmax' activation...
	#...unlike 'ReLu' which the other layers use. This is because the best activation for the last layer...
	#... is 'softmax' as it ensures that the outputs
	#...of this layer sum up to one so that they can be interpreted as probabilities. 
	
	
	my_optimiser = SGD(learning_rate=0.011, momentum=0.87)
	#This model uses a stochastic gradient descent optimiser with learning rate 0.011 and momentum 0.87.
	#Momentum adds a fraction of the prevous weight update to the current one. 
	#SO when performing gradient descent, learning rate measures how much the current situation affects ... 
	#... the next step, while momentum measures how much past steps affect the next step. 
	
	model.compile(optimizer=my_optimiser, loss='categorical_crossentropy', metrics=['accuracy'])
	#^Here, I compile the model using the optimiser defined a few lines above.
	#Categorical crossentropy is used as the loss function as it is a good loss function for multi-class...
	#... classification problems and my problem is a multi-class classification one.
	#A loss function is used to calculate the gradients which are used to update the weights of the neural net.

	return model





#AFTER DEFINING THE MODEL, IT NEEDS TO BE EVALUATED:

#I evaluate the model using five-fold cross validation. k-fold cross validation is where a given data set is split...
#...into k number of folds/sections and each section is used as a testing set at some point. So with 5-fold, ...
#...the MNIST training data set is split into five folds where each fold is 20% of the training dataset ...
#...and each fold is used as a testing set at some point. So each fold has a training and testing dataset ...
#... and is overall 20% of the training dataset.

def evaluate_model(dataX, dataY, number_of_folds=5):
	scores, histories = list(), list()
	#This initialises scores and histories as lists.
	
	folded_data = KFold(number_of_folds, shuffle=True, random_state=1)
	#^ Here I shuffle the data set before splitting it up into 5 folds.
	

	for train_ix, test_ix in folded_data.split(dataX):
	#^This loops lets us iterate through each fold.	
		model = define_model()
		#^The model previously defined is used.

		# select rows for train and test
		trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
		#Train and test sets are created for this particular fold.

		
		history = model.fit(trainX, trainY, epochs=8, batch_size=32, validation_data=(testX, testY), verbose=0)
#In the line above, I fit my train dataset from this fold to the model. 
#The number of epochs is a hyperparameter which is the number of times the learning algorithm will work through the ...
#... this training dataset from this fold.

	
		_, acc = model.evaluate(testX, testY, verbose=0)
		#^ This	uses an inbuilt .evaluate() function to get the accuracy of the model...
		#...trained on this training set from this fold and tested on the testing set from this fold.  	
		print(">" + round((acc * 100.0),3))
		
		scores.append(acc)
		histories.append(history)
	return scores, histories
	#The scores and histories are returned.




#AFTER EVALUATING THE MODEL, the next step is to present the diagnostics.

def summarize_diagnostics(histories):
	for i in range(len(histories)):
		# plot loss
		pyplot.subplot(2, 1, 1)
		pyplot.title('Cross Entropy Loss')
		pyplot.plot(histories[i].history['loss'], color='blue', label='train')
		pyplot.plot(histories[i].history['val_loss'], color='orange', label='test')
		# plot accuracy
		pyplot.subplot(2, 1, 2)
		pyplot.title('Classification Accuracy')
		pyplot.plot(histories[i].history['accuracy'], color='blue', label='train')
		pyplot.plot(histories[i].history['val_accuracy'], color='orange', label='test')
	pyplot.show()


#THEN YOU CAN summarize the performance.

#This function presents the scores.
def show_formatted_scores(scores):
	mean= (mean(scores)*100)
	standard_deviation = (std(scores)*100)
	number=len(scores)
	print('Accuracy: mean='+mean+
	", std=" + standard_deviation+", n="+
	number)
	#This summarises the results.


def run_test_harness():
        trainX,trainY,testX,testY=load_dataset()
        trainX,testX=normalise_pixels(trainX,testX)
		#^ The dataset is loaded and the data is prepped.
        model=define_model()
		#^The previously defined model is chosen
        model.fit(trainX, trainY, epochs=8, batch_size=32, verbose=0)
		#^The model is then fit to the data using the inbuilt...
		#... .fit() function.
        scores, histories = evaluate_model(trainX, trainY)
		#^The fit model is then evaluated.
        show_formatted_scores(scores)
        model.save('final_model.h5')
		#^The trained model is saved with a h5 extension.

        model = load_model('final_model.h5')
        _, acc = model.evaluate(testX, testY, verbose=0)
		#^ The saved model is then tested to see how...
		#...it performs on the test data.
        print('> ' +str((acc*100.0)))

		

run_test_harness()
import keras
import tensorflow as tf
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np

 
# load and prepare the image
def load_image(filename):
	# load the image
	img = load_img(filename, color_mode="grayscale", target_size=(28, 28))
	# convert to array
	img = img_to_array(img)
	# reshape into a single sample with 1 channel
	img = img.reshape(1, 28, 28, 1)
	# prepare pixel data
	img = img.astype('float32')
	img = img / 255.0
	return img
 
# load an image and predict the class
def run_example(filename):
	# load the image
	img = load_image(filename)
	# load model
	model = load_model('final_model.h5')
	# predict the class
	digit=np.argmax(model.predict(img), axis=-1)
	return (digit[0])
 








