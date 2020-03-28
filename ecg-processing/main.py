import csv
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


def show_seq_dots(x, y):
    plt.plot(x, y, '.')
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


def discretize_x(x_arr: [], y_arr: [], frequency: int, t_max: float) -> ([], []):
    x_max = max(x_arr)
    modifier = x_max / t_max

    curr = min(y)
    delta = 1 / frequency
    iter_count = int(t_max / delta)

    x_new = []

    for i in range(0, iter_count):
        curr = curr + delta
        scaled = curr * modifier
        x_new.append(scaled)

    f = interpolate.interp1d(y, x, bounds_error=False, fill_value='extrapolate')
    y_new = f(x_new)

    return x_new, y_new


x, y = read_csv_data("data2.csv")
show_seq_dots(y, x)

x_new, y_new = discretize_x(y, x, 125, 9.2)

show_seq_dots(x_new, y_new)
show_seq(x_new, y_new)