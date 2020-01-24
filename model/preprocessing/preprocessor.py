import random
import numpy as np  # linear algebra
import pandas as pd
from scipy.signal import resample
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle

np.random.seed (42)


class Preprocessor (object):

    @staticmethod
    def stretch(x):
        l = int (187 * (1 + (random.random () - 0.5) / 3))
        y = resample (x, l)
        if l < 187:
            y_ = np.zeros (shape = (187,))
            y_ [:l] = y
        else:
            y_ = y [:187]
        return y_

    @staticmethod
    def amplify(x):
        alpha = (random.random () - 0.5)
        factor = -alpha * x + (1 + alpha)
        return x * factor

    @staticmethod
    def augment(x):
        result = np.zeros (shape = (4, 187))
        for i in range (3):
            if random.random () < 0.33:
                new_y = Preprocessor.stretch (x)
            elif random.random () < 0.66:
                new_y = Preprocessor.amplify (x)
            else:
                new_y = Preprocessor.stretch (x)
                new_y = Preprocessor.amplify (new_y)
            result [i, :] = new_y
        return result

    @staticmethod
    def split_df(data):
        M = data.values
        X = M [:, :-1]
        y = M [:, -1].astype (int)
        return X, y

    @staticmethod
    def categorize(y):
        C0 = np.argwhere (y == 0).flatten ()
        C1 = np.argwhere (y == 1).flatten ()
        C2 = np.argwhere (y == 2).flatten ()
        C3 = np.argwhere (y == 3).flatten ()
        C4 = np.argwhere (y == 4).flatten ()
        return C0, C1, C2, C3, C4

    @staticmethod
    def add_augmented(X, y, category):
        result = np.apply_along_axis (Preprocessor.augment, axis = 1, arr = X [category]).reshape (-1, 187)
        classe = np.ones (shape = (result.shape [0],), dtype = int) * 3
        X = np.vstack ([X, result])
        y = np.hstack ([y, classe])
        return X, y

    @staticmethod
    def random_subsets(n, *args):
        subsets = []
        for subset in args:
            subsets.append (np.random.choice (subset, n))
        return subsets

    @staticmethod
    def construct_from_subsets(X, *args):
        constructed = np.ndarray ()  # TODO fix
        for category in args:
            constructed = np.vstack ([constructed, X [category]])
        return constructed

    @staticmethod
    def separate_train_val(X, y):

        pass

    @staticmethod
    def load_mitbih(directory_path):
        df_train = pd.read_csv (directory_path + "mitbih_train2.csv", header = None) # , index_col = 0
        df_test = pd.read_csv (directory_path + "mitbih_test2.csv", header = None)
        return df_train, df_test

    @staticmethod
    def CNN_preprocessor(train_data, test_data, val_size, test_size):
        # Extract data from df into numpy array
        X, y = Preprocessor.split_df (train_data)
        X_test, y_test = Preprocessor.split_df (test_data)
        # Get subsets of different categories
        C0, C1, C2, C3, C4 = Preprocessor.categorize (y)
        C0_test, C1_test, C2_test, C3_test, C4_test = Preprocessor.categorize (y_test)
        # Augment data (now only for C3)
        X, y = Preprocessor.add_augmented (X, y, C3)
        X_test, y_test = Preprocessor.add_augmented (X_test, y_test, C3_test)
        # Get random subsets for further validation and testing
        subC0, subC1, subC2, subC3, subC4 = Preprocessor.random_subsets (val_size, C0, C1, C2, C3, C4)
        subC0_t, subC1_t, subC2_t, subC3_t, subC4_t = Preprocessor.random_subsets (test_size, C0_test, C1_test, C2_test,
                                                                                   C3_test,
                                                                                   C4_test)
        # Stacking subsets to create vaidation sets
        X_val = np.vstack ([X [subC0], X [subC1], X [subC2], X [subC3], X [subC4]])
        y_val = np.hstack ([y [subC0], y [subC1], y [subC2], y [subC3], y [subC4]])

        X_train = np.delete (X, [subC0, subC1, subC2, subC3, subC4], axis = 0)
        y_train = np.delete (y, [subC0, subC1, subC2, subC3, subC4], axis = 0)

        X_train, y_train = shuffle (X_train, y_train, random_state = 0)
        X_val, y_val = shuffle (X_val, y_val, random_state = 0)

        X_test = np.vstack ([X_test [subC0_t], X_test [subC1_t], X_test [subC2_t], X_test [subC3_t], X_test [subC4_t]])
        y_test = np.hstack ([y_test [subC0_t], y_test [subC1_t], y_test [subC2_t], y_test [subC3_t], y_test [subC4_t]])

        X_train = np.expand_dims (X_train, 2)
        X_val = np.expand_dims (X_val, 2)
        X_test = np.expand_dims (X_test, 2)

        ohe = OneHotEncoder ()
        y_train = ohe.fit_transform (y_train.reshape (-1, 1))
        y_val = ohe.transform (y_val.reshape (-1, 1))
        y_test = ohe.transform (y_test.reshape (-1, 1))

        return X_train, y_train, X_val, y_val, X_test, y_test
