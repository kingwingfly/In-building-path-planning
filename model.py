import numpy as np
import pandas as pd


def is_in(point, points):
    flag = False
    for i in range(len(points)):
        pointA = points[i][::-1]
        pointB = points[(i + 1) % len(points)][::-1]
        x, y, x1, y1, x2, y2 = point[0], point[1], pointA[0], pointA[1], pointB[0], pointB[1]
        if y1 == y2:
            continue
        elif y > max([y1, y2]):
            continue
        elif y <= y1 and y <= y2:
            continue
        elif x > max([x1, x2]):
            continue
        elif y == max([y1, y2]):
            flag = not flag
            continue
        x0 = (x2 - x1) * (y - y1) / (y2 - y1) + x1
        if x < x0:
            flag = not flag
    return flag


def model(height, weight, file):
    data = pd.read_csv(file)
    a, b = data['start'], data['end']
    points, barriers = [], []
    for start, end in zip(a, b):
        points.append(start)
        if end in points:
            points = np.array(list(map(eval, points)))
            barriers.append(points)
            points = []
    # print(barriers)
    dd = float('inf')
    cost_map = np.ones([height, weight], float)
    for points in barriers:
        for i in range(height):
            for j in range(weight):
                if cost_map[i, j] != dd:
                    if is_in((i, j), points):
                        cost_map[i, j] = dd
    with open('data/cost_map.txt', 'w+', encoding='utf-8') as f:
        f.write('[')
        lst = list(cost_map)
        for i in lst[:-1:]:
            f.write('[')
            for j in i[:-1:]:
                f.write(str(j) + ',')
            f.write(str(i[-1]))
            f.write('],')
        f.write('[')
        for j in lst[-1][:-1:]:
            f.write(str(j) + ',')
        f.write(str(lst[-1][-1]))
        f.write(']]')


if __name__ == '__main__':
    print(model(100, 100, 'data/sj_test.csv'))
