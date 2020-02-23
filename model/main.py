import os
import tempfile

from preprocessing.preprocessor import Preprocessor
from cnn.cnn_model import CNNModel
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns
import numpy as np  # linear algebra

import pandas as pd
from tensorflow import keras

def explore_data(df_train, df_test, abnormal, normal):
    fullmitbih = pd.DataFrame(
        {'Category':pd.concat([df_test, df_train]) [187]})
    fullptbdb = pd.DataFrame({'Category':pd.concat([abnormal, normal]) [187]})

    sns.countplot(x = "Category", label = "Count", data = fullmitbih)
    plt.show()

    sns.countplot(x = "Category", label = "Count", data = fullptbdb)
    plt.show()


def vizualize_history(history):
    history_dict = history.history
    keys = history_dict.keys()

    loss_values = history_dict ['loss']
    val_loss_values = history_dict ['val_loss']
    acc = history_dict ['val_accuracy']

    epochs = range(1, len(acc) + 1)

    plt.plot(epochs, loss_values, 'bo', label = 'Training loss')
    plt.plot(epochs, val_loss_values, 'b', label = 'Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    plt.clf()
    acc_values = history_dict ['accuracy']
    val_acc = history_dict ['val_accuracy']
    plt.plot(epochs, acc_values, 'bo', label = 'Training acc')
    plt.plot(epochs, val_acc, 'b', label = 'Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

def save_model_for_serving(model):
    MODEL_DIR = tempfile.gettempdir()
    version = 1
    export_path = os.path.join(MODEL_DIR, str(version))
    print('export_path = {}\n'.format(export_path))
    if os.path.isdir(export_path):
        print('\nAlready saved a model, cleaning up\n')

    from keras import backend
    sess = backend.get_session()

    tf.compat.v1.saved_model.simple_save(
        sess,
        export_path,
        inputs = {'input_image':model.input},
        outputs = {t.name:t for t in model.outputs})


# working with data
df_train, df_test = Preprocessor.load_mitbih("")
abnormal, normal = Preprocessor.load_ptbdb("")

X_train, y_train, X_val, y_val, X_test, y_test = Preprocessor.CNN_preprocessor(df_train, df_test, 800, 2000)

# define model
n_obs, feature, depth = X_train.shape
model = CNNModel.get_model(n_obs, feature, depth)
h_params = CNNModel.CNN_hyperparameters(n_obs)

model.compile(loss = h_params ['loss'], optimizer = h_params ['optimizer'], metrics = h_params ['metrics'])

history = model.fit(X_train, y_train,
                    epochs = 10,
                    batch_size = h_params ['batch_size'],
                    verbose = 1,
                    validation_data = (X_val, y_val),
                    callbacks = [h_params ['lrate']])

vizualize_history(history)

#save_model_for_serving(model)
#y_pred = model.predict(X_test, batch_size=1000)

print()