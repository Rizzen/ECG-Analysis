import json
import numpy as np
import pandas as pd
import requests


class FileProcessor(object):

    @staticmethod
    def process(file):
        data = pd.read_csv(file)
        values_without_labels = data.values[:, :-1]
        predictions = []
        for val in values_without_labels:
            val = np.expand_dims(val, 0)
            val = np.expand_dims(val, 2)
            tf_row = val.tolist()
            tf_req = json.dumps({'instances': tf_row})
            req = requests.post('http://localhost:8501/v1/models/cnn_model:predict', data=tf_req)
            prediction = req.json()['predictions']
            predictions.append(prediction)
            print(prediction)

        return predictions