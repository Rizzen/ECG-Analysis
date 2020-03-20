import csv
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def read_floats(array):
    res = []
    for a in array:
        res.append(float(a))
    return res

def interpolate_vals(val_left, val_right):
    return (val_left + val_right) / 2

def show_seq(seq):
    r = range(0, len(seq))
    plt.plot(r, seq, '.')

    plt.show()

with open('data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

    nums = read_floats(data[0])
    print(len(nums))

    res = []
    i = 1
    for a in nums:
        if i >= len(nums):
            break
        inter = interpolate_vals(a, nums[i])
        res.append(a)
        res.append(inter)
        i = i + 1
    res.append(nums[i - 1])

    show_seq(nums)
    show_seq(res)

print(nums)
print(res)