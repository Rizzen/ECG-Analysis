import math

from keras import backend as K
from keras.callbacks import LearningRateScheduler
from keras.layers import Input, Dense, Conv1D, MaxPooling1D, Softmax, Add, Flatten, Activation
from keras.models import Model
from keras.optimizers import Adam


class CNNModel (object):

    @staticmethod
    def get_model(n_obs, feature, depth):
        K.clear_session ()

        inp = Input (shape = (feature, depth))
        C = Conv1D (filters = 32, kernel_size = 5, strides = 1) (inp)

        C11 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (C)
        A11 = Activation ("relu") (C11)
        C12 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (A11)
        S11 = Add () ([C12, C])
        A12 = Activation ("relu") (S11)
        M11 = MaxPooling1D (pool_size = 5, strides = 2) (A12)

        C21 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (M11)
        A21 = Activation ("relu") (C21)
        C22 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (A21)
        S21 = Add () ([C22, M11])
        A22 = Activation ("relu") (S11)
        M21 = MaxPooling1D (pool_size = 5, strides = 2) (A22)

        C31 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (M21)
        A31 = Activation ("relu") (C31)
        C32 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (A31)
        S31 = Add () ([C32, M21])
        A32 = Activation ("relu") (S31)
        M31 = MaxPooling1D (pool_size = 5, strides = 2) (A32)

        C41 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (M31)
        A41 = Activation ("relu") (C41)
        C42 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (A41)
        S41 = Add () ([C42, M31])
        A42 = Activation ("relu") (S41)
        M41 = MaxPooling1D (pool_size = 5, strides = 2) (A42)

        C51 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (M41)
        A51 = Activation ("relu") (C51)
        C52 = Conv1D (filters = 32, kernel_size = 5, strides = 1, padding = 'same') (A51)
        S51 = Add () ([C52, M41])
        A52 = Activation ("relu") (S51)
        M51 = MaxPooling1D (pool_size = 5, strides = 2) (A52)

        F1 = Flatten () (M51)

        D1 = Dense (32) (F1)
        A6 = Activation ("relu") (D1)
        D2 = Dense (32) (A6)
        D3 = Dense (5) (D2)
        A7 = Softmax () (D3)

        model = Model (inputs = inp, outputs = A7)
        return model

    @staticmethod
    def CNN_hyperparameters(n_obs):
        batch_size = 500

        def exp_decay(epoch):
            initial_lrate = 0.001
            k = 0.75
            t = n_obs // (10000 * batch_size)  # every epoch we do n_obs/batch_size iteration
            lrate = initial_lrate * math.exp (-k * t)
            return lrate

        params = {
            'lrate':LearningRateScheduler (exp_decay),
            'optimizer':Adam (lr = 0.001, beta_1 = 0.9, beta_2 = 0.999),
            'loss':'categorical_crossentropy',
            'metrics':['accuracy'],
            'batch_size':batch_size

        }
        return params
