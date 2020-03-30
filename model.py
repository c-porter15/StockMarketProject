import tensorflow as tf
import json
import numpy as np
from sklearn.preprocessing import normalize 


def createTFDataSet():
    test_data = np.array([[]])
    i = 0
    with open('StockMarketProject/consolidatedData.json', 'r') as outfile2:
        json_data = json.load(outfile2)

    for obj in json_data:
        temp_data = normalizeData(obj)
        test_data.append(test_data,temp_data,i)

    return test_data

def normalizeData(obj):
    input_List = list(obj['data']['attributes']['result'].values())
    
    return 0

createTFDataSet()