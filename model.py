import tensorflow as tf
import json
import numpy as np
import random
import keras as keras
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn import linear_model
from sklearn.utils import shuffle
import sklearn

def createTFDataSet():

    with open('consolidatedData.json', 'r') as outfile:
        json_data = json.load(outfile)
        data = getRequiredData(json_data)
        random.shuffle(data)
        data = pd.DataFrame.from_records(data)
        X = np.array(data.drop(columns=4))
        Y = np.array(data[4])
        train_in, test_in, train_out, test_out = sklearn.model_selection.train_test_split(X, Y, test_size=0.2)

    return train_in, train_out, test_in, test_out

def getRequiredData(json_data):
    data_array = []
    for i in range (174):
        data_array.insert(i, [json_data[i].get("data").get("attributes").get("result").get("EPS_Surprise"), 
                            json_data[i].get("data").get("attributes").get("result").get("EPS Growth %"), 
                            json_data[i].get("data").get("attributes").get("result").get("%RevenueGrowth"), 
                            json_data[i].get("data").get("attributes").get("result").get("%Net Income Growth"), 
                            json_data[i].get("data").get("attributes").get("result").get("%OvernightMovement(CloseVsOpen)")])

    return data_array

train_in, train_out, test_in, test_out = createTFDataSet()
linear = linear_model.LinearRegression()
linear.fit(train_in, train_out)
acc = linear.score(test_in, test_out)
print(acc)

print("CO: \n" , linear.coef_)
print("Intercept \n" , linear.intercept_)

predictions = linear.predict(test_in)

for i in range(len(predictions)):
    print(predictions[i], test_in[i], test_out[i])

#####MODEL 2
# clf = ensemble.GradientBoostingRegressor(n_estimators = 500, max_depth = 5, min_samples_split = 2, learning_rate = 0.01, loss = 'ls')
# clf.fit(train_in, train_out)
# print(mean_squared_error(test_out, clf.predict(test_in)))

#####MODEL 3
# model = keras.Sequential([
#     keras.layers.Dense(4, activation='relu'),
#     keras.layers.Dense(7, activation="relu"),
#     keras.layers.Dense(7, activation="relu"), #fully connected linear activation
#     keras.layers.Dense(1, activation = "linear") #fully connected sigmoid function
#     ])

# model.compile(optimizer="adam", loss="mean_squared_error", metric=["accuracy"])
# output_layers = ['output1']

# # history = model.fit(train_in, train_out, validation_split=0.33, epochs=150, batch_size=10, verbose=0) #epoch is number of times model will see any given image

# summarize history for loss
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper left')
# plt.show()