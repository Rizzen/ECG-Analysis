import csv
import glob
import os
import matplotlib.pyplot as plt
from scipy import interpolate


def read_floats(array):
    res = []
    for a in array:
        res.append(float(a))
    return res


def interpolate_vals(val_left, val_right):
    return (val_left + val_right) / 2


def show_seq(x, y):
    plt.plot(x, y)
    plt.show()


def show_seq_dots(x, y, title=""):
    plt.plot(x, y, '.')
    plt.title(title)
    plt.show()


def read_csv_data(filepath: str) -> ([], []):
    x = []
    y = []
    with open(filepath, newline='') as csv_file:
        data = list(csv.reader(csv_file))
        for d in data:
            xd = float(d[0])
            yd = float(d[1])
            x.append(xd)
            y.append(yd)
    return x, y


def read_csv_mit_bih(filepath: str) -> [[]]:
    with open(filepath, newline='') as csv_file:
        data = list(csv.reader(csv_file))
        return data

def write_result_to_csv_file(filepath: str,  result:[[]]):
    with open(filepath, 'w') as result_file:
        wr = csv.writer(result_file)
        wr.writerows(result)


def discretize_x(x_arr: [], y_arr: [], frequency: int, t_max: float) -> ([], []):
    x_max = max(x_arr)
    modifier = x_max / t_max

    curr = min(y_arr)
    delta = 1 / frequency
    iter_count = int(t_max / delta)

    x_new = []

    for i in range(0, iter_count):
        curr = curr + delta
        scaled = curr * modifier
        x_new.append(scaled)

    f = interpolate.interp1d(x_arr, y_arr, bounds_error=False, fill_value='extrapolate', kind='slinear')
    y_new = f(x_new)

    return x_new, y_new


def split_to_full_arrays(array: [], array_size: int) -> [[float]]:
    res = []
    chunks_num = int(len(array) / array_size)

    for i in range(0, chunks_num):
        arr = list(array[(i * array_size):(i * array_size + array_size)])
        res.append(arr)
    return res


def slice_and_categorize(array: [], array_size: int, category: int) -> [[]]:
    split = split_to_full_arrays(array, array_size)
    for s in split:
        s.append(category)
    return split


def shift_slice(array: [], array_size: int, shift: int) -> [[float]]:
    res = []
    chunks_num = int ((len(array) - array_size) / shift)
    for i in range(0, chunks_num):
        arr = list(array[(i * shift):(i * shift + array_size)])
        res.append(arr)
    return res


def shift_slice_and_categorize(array: [], array_size: int, shift: int, category: int) -> [[]]:
    split = shift_slice(array, array_size, shift)
    for s in split:
        s.append(category)
    return split


def process_directory(directory: str, frequency: int, sample_len: float, target_sample_size: int, category: int) \
        -> [[float]]:
    os.chdir(directory)
    files = glob.glob("*.csv")

    res = []
    for file in files:
        x_data, y_data = read_csv_data(file)
        x_new, y_new = discretize_x(x_data, y_data, frequency, sample_len)
        v = shift_slice_and_categorize(y_new, target_sample_size, int(frequency / 2), category)
        for arr in v:
            res.append(arr)

    return res


def train_test_split(array: []) -> ([], []):
    anchor = len(array) - int(len(array) / 4)
    train = array[:anchor]
    test = array[anchor:]
    return train, test


def just_classify(lst: [(str, int)]) -> ([], []):
    train = []
    test = []
    for i in lst:
        os.chdir(i[0])
        files = glob.glob("*.csv")
        dir_res = []
        for file in files:
            arr = read_csv_mit_bih(file)
            arr[0].append(i[1])
            dir_res.append(arr[0])
        trn, tst = train_test_split(dir_res)
        train.extend(trn)
        test.extend(tst)
    return train, test

#  ['N': 0, 'S': 1, 'V': 2, 'F': 3, 'Q': 4]
# наджелудочковая - S = 1
# желудочковая - V = 2

dir_cat_list = [
    ("/Users/mark.tkachenko/Projects/OSS/ECG-Data/raw/наджелудочковая", 1),
    ("/Users/mark.tkachenko/Projects/OSS/ECG-Data/raw/желудочковая", 2),
    ("/Users/mark.tkachenko/Projects/OSS/ECG-Data/raw/норма", 0)
]

classify_list = [
    ("/Users/mark.tkachenko/Projects/OSS/ECG-Data/by-elikov/N", 0),
    ("/Users/mark.tkachenko/Projects/OSS/ECG-Data/by-elikov/S", 1),
    ("/Users/mark.tkachenko/Projects/OSS/ECG-Data/by-elikov/F", 3)
]

out_train_file = "/Users/mark.tkachenko/Projects/OSS/ECG-Data/mit-bih-format/ecg-data-train.csv"
out_test_file = "/Users/mark.tkachenko/Projects/OSS/ECG-Data/mit-bih-format/ecg-data-test.csv"
frequency = 125
sample_length = 9.2  # seconds
target_sample_size = 187  # items


train = []
test = []
for dir_cat in dir_cat_list:
    proc_res = process_directory(dir_cat[0], frequency, sample_length, target_sample_size, dir_cat[1])
    one_train, one_test = train_test_split(proc_res)
    train.extend(one_train)
    test.extend(one_test)

trn, tst = just_classify(classify_list)
train.extend(trn)
test.extend(tst)

write_result_to_csv_file(out_train_file, train)
write_result_to_csv_file(out_test_file, test)
