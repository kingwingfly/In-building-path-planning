import numpy as np
import pandas as pd


def is_in(point, points):
    """射线法判断某个点是否在points围成的封闭图形中
    射线法原理：
    对于一段封闭曲线，判断一个点是否在封闭图形内，首先过该点做一条平行于x轴，射向x轴正方向的射线
    若该线段和封闭曲线有偶数个交点，则在封闭区域外；奇数个交点，则在封闭区域内

    Args:
        point (tuple[int, int]): 某个待判断的点
        points (np.array[int]): 封闭图形的顶点们

    Returns:
        _type_: _description_
    """
    flag = False
    for i in range(len(points)):  # 遍历障碍物区域的所有顶点
        pointA = points[i][::-1]  # A点（倒序是为了转坐标轴，让射线法用着更方便）
        pointB = points[(i + 1) % len(points)][
            ::-1
        ]  # B点；为什么求余？答：若A为最后一个点，则B点取第一个点，这样才能封闭
        x, y, x1, y1, x2, y2 = (
            point[0],
            point[1],
            pointA[0],
            pointA[1],
            pointB[0],
            pointB[1],
        )  # 将点的横纵坐标赋值，提高可读性
        '''
        下面步骤的思路
        首先，flag初始值为False，表示0个交点，在封闭区域外
        两条直线最多有一个交点
        每多一个交点，flag就取一次反
        '''
        if y1 == y2:
            continue
        elif y > max([y1, y2]):
            continue
        elif y <= y1 and y <= y2:
            continue
        # 此时 y 在 y1 y2 之间
        elif x > max([x1, x2]):
            continue
        elif y == max([y1, y2]):  # 这里有一个射线经过边界的特殊情况，我也说不清楚，可以注释掉试试看看后果
            flag = not flag
            continue
        x0 = (x2 - x1) * (y - y1) / (y2 - y1) + x1  # 求解射线所在直线与边线交点的横坐标
        if x < x0:  # 如果交点在射线端点的右边，说明射线与边线有交点，此时flag取反
            flag = not flag
    # 遍历结束后，返回flag即可
    return flag


def model(height: int, weight: int, file: str):
    """根据文件中描述的有关障碍物的线段生成矩阵

    Args:
        height (int): The row number of the array
        weight (int): The column number of the array
        file (str): Path of the file describing the barriers
    """
    data = pd.read_csv(file)  # 打开文件
    a, b = data['start'], data['end']  # 读取开始点与结束点
    points, barriers = [], []
    for start, end in zip(a, b):
        points.append(start)  # 遍历开始点和结束点：先将开始点存起来，当结束点出现在开始点列表中时，说明这个图形封闭了
        if end in points:  # 封闭后
            points = np.array(
                list(map(eval, points))
            )  # 就可以将points转化为array（因为points中的元素为字符串，所以需要eval一下）
            barriers.append(points)  # 将这个array加入到barriers列表中
            points = []  # 重置point
    '''
    至此, 文件中的所有封闭的线段都被分开并存储在了barrier这个列表中
    '''
    # print(barriers)
    dd = float('inf')  # 将无穷大的数赋值给dd，方便使用
    cost_map = np.ones([height, weight], float)  # 初始化一个没有任何障碍物的map矩阵
    for points in barriers:  # 对某个封闭的障碍物
        for i in range(height):
            for j in range(weight):  # 对map中的每个点(i, j)
                if cost_map[i, j] != dd:  # 如果通过该点的代价还不是无穷大（如果被认定为障碍物就不用在做判断了）
                    if is_in((i, j), points):  # 如果该点在这个障碍物中
                        cost_map[i, j] = dd  # 则通过该点的代价为无穷大

    # 这里就是把一个列表储存为可以直接通过eval方法转成列表的字符串，总觉得有更好的方法，我也不知道为啥我会这么写，太抽象了，可恶（直接将列表写入文件多半不行）
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
