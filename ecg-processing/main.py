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


#  ['N': 0, 'S': 1, 'V': 2, 'F': 3, 'Q': 4]
# наджелудочковая - S = 1
# желудочковая - V = 2
in_directory_one = "/Users/mark.tkachenko/Projects/OSS/ECG-Data/raw/наджелудочковая"
in_directory_two = "/Users/mark.tkachenko/Projects/OSS/ECG-Data/raw/желудочковая"
in_directory_three = "/Users/mark.tkachenko/Projects/OSS/ECG-Data/raw/норма"

out_file = "/Users/mark.tkachenko/Projects/OSS/ECG-Data/mit-bih-format/ecg-data.csv"
frequency = 125
sample_length = 9.2  # seconds
target_sample_size = 187  # items

cat_one = process_directory(in_directory_one, frequency, sample_length, target_sample_size, 1)
cat_two = process_directory(in_directory_two, frequency, sample_length, target_sample_size, 2)
cat_three = process_directory(in_directory_three, frequency, sample_length, target_sample_size, 0)

cat_one.extend(cat_two)
cat_one.extend(cat_three)

write_result_to_csv_file(out_file, cat_one)
