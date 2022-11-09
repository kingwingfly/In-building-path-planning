import cv2
import pandas as pd
import numpy as np
from PIL import Image
# data_file = 'data/sj_test.csv'
# data = pd.read_csv(data_file, encoding='utf-8')
# # a, b = data['start'], data['end']
# # print(a, b)
# print(len(data['start']))
# # for i in range(len(data['start'])):
# #     # print(type(data['start'][i]))
# #     a, b = eval(data['start'][i])
# #     print(a, b)
# print(data["start"][len(data['start'])-1])
# a, b = ['(6, 9)', '(0, 0)', '(9, 2)'], ['(0, 0)', '(9, 2)', '(6, 9)']
# for x, y in zip(a, b):
#     print(x, y)
# print(np.random.rand(36,2))
# file = 'data/sj_test.csv'
# data = pd.read_csv(file)


# def area(points):
#     x = points[:, 0]
#     y = points[:, 1]
#     return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
#
#
# points = np.array([[0, 0], [0, 2], [0, 3], [2, 4]])
# print(area(points))

with open('data/cost_map.txt', 'r', encoding='utf-8') as f:
    t = f.read()
    # print(t)
    lst = []
    for i in t[1:-1:]:
        if i == '[':
            lst.append([])
        elif i == '1':
            lst[-1].append(1)
        elif i == 'i':
            lst[-1].append(float('inf'))
    lst = np.array(lst)

print(type(lst))
print(lst)


img = Image.fromarray(lst)

import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()


