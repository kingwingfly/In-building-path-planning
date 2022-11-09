import cv2
import pandas as pd
from PIL import Image


class plotTool:
    def __init__(self):
        self.img = None
        self.a, self.b = [], []
        self.x1, self.x2, self.y1, self.y2, self.x0, self.y0 = 0, 0, 0, 0, 0, 0
        self.x1y1, self.x2y2 = '', ''
        self.start = True
        self.end = False
        self.point = []

    def mouse_event(self, event, x, y, flags, param):
        img, color = param
        if event == cv2.EVENT_LBUTTONDOWN and self.start:
            self.x1, self.y1 = x, y
            self.x1y1 = '%d,%d' % (x, y)
            self.x0, self.y0 = x, y
            cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
            cv2.putText(img, self.x1y1, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=1)
            self.start = False

        elif event == cv2.EVENT_LBUTTONDOWN:
            self.x2, self.y2 = x, y
            self.x2y2 = '%d,%d' % (x, y)
            self.a.append((self.x1, self.y1))
            self.b.append((self.x2, self.y2))
            cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
            cv2.putText(img, self.x2y2, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=1)
            cv2.line(img, (self.x1, self.y1), (self.x2, self.y2), color=color, thickness=3)
            self.x1, self.y1 = self.x2, self.y2

    def mouse_event1(self, event, x, y, flags, param):
        img, file = param
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.point) < 1:
                # print(self.point)
                self.point.append((x, y))
                xy = 'Start: %d,%d' % (x, y)
                cv2.circle(img, (x, y), 3, (255, 0, 0), thickness=5)
                cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2)
            else:
                self.img = cv2.imread(file)
                self.point.append((x, y))
                self.point = self.point[-2::]
                print(self.point)
                for i in range(2):
                    x, y = self.point[i]
                    if i == 0:
                        xy = 'Start: %d,%d' % (x, y)
                    else:
                        xy = 'End: %d,%d' % (x, y)
                    print(xy)
                    cv2.circle(self.img, (x, y), 3, (255, 0, 0), thickness=5)
                    cv2.putText(self.img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2)

    def choose(self, file: str):
        self.img = cv2.imread(file)
        cv2.namedWindow('image')
        while True:
            cv2.imshow('image', self.img)
            cv2.setMouseCallback('image', self.mouse_event1, (self.img, file))
            k = cv2.waitKey(10)
            if k == 13:     # 回车
                return self.point[0][::-1], self.point[1][::-1]
            if k == 27:
                break
            if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) <= 0:
                break
        cv2.destroyWindow('image')
        return self.point[0][::-1], self.point[1][::-1]

    def draw(self, file: str, point_type: str, color: tuple, x: int):
        assert isinstance(file, str)
        self.__init__()
        img = cv2.imread(file)
        cv2.namedWindow('image')
        while True:
            cv2.imshow('image', img)
            cv2.setMouseCallback('image', self.mouse_event, (img, color))
            k = cv2.waitKey(10)
            if k == 32:     # 空格打断
                self.start = not self.start
            elif k == 99:   # c闭合
                self.end = not self.end
                if self.end:
                    self.a.append((self.x1, self.y1))
                    self.b.append((self.x0, self.y0))
                    cv2.line(img, (self.x1, self.y1), (self.x0, self.y0), color=color, thickness=3)
                    self.end, self.start = not self.end, not self.start
            elif k == 117:   # u撤回
                img = cv2.imread(file)
                self.a, self.b = self.a[:-1:], self.b[:-1:]
                for i in range(len(self.a)):
                    (self.x1, self.y1), (self.x2, self.y2) = self.a[i], self.b[i]
                    self.x1y1, self.x2y2 = '%d,%d' % (self.x1, self.y1), '%d,%d' % (self.x2, self.y2)
                    cv2.putText(img, self.x1y1, (self.x1, self.y1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=1)
                    cv2.line(img, (self.x1, self.y1), (self.x2, self.y2), color=color, thickness=3)
                self.x1, self.y1 = self.x2, self.y2
                cv2.putText(img, self.x2y2, (self.x2, self.y2), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=1)
                if self.start:
                    self.start = not self.start
            if k == 27:
                break
            if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) <= 0:
                break
        cv2.destroyWindow('image')
        data = {'start': self.a, 'end': self.b}
        data = pd.DataFrame(data)
        data.to_csv(f'data/sj_{point_type}.csv')
        cv2.imwrite(f'{file[:x:]}_{point_type}.png', img)
        print(data)
        print(f'数据已保存到data/sj_{point_type}.csv，图纸已保存到pic/{file[:x:]}_{point_type}.png')


def draw_path(way):
    img = cv2.imread('pic/1_D.png')
    for i in range(len(way)-1):
        start, end = way[i][::-1], way[i+1][::-1]
        cv2.line(img, start, end, color=(0, 255, 0), thickness=2)
    cv2.namedWindow('image')
    while True:
        cv2.imshow('image', img)
        k = cv2.waitKey(10)
        if k == 27:
            break
        if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) <= 0:
            break
    cv2.destroyWindow('image')


def cut_show(filename, mode):
    img = Image.open(filename)
    img_size = img.size
    t = 640 / max(img_size)
    img_size2 = (int(img_size[0] * t), int(img_size[1] * t))
    img2 = img.resize(img_size2)
    if mode == 0:
        img2.save(filename[:-4:] + '_S.png')
        return filename[:-4:] + '_S.png', img_size2[0], img_size2[1]
    elif mode == 1:
        img2.save(filename[:-6:] + '_S.png')
        return filename[:-6:] + '_S.png', img_size2[0], img_size2[1]
    else:
        x = -1
        for i in filename[::-1]:
            if i == '_':
                break
            x -= 1
        img2.save(filename[:x:] + '_S.png')
        print('展示图片已保存到' + filename[:x:] + '_S.png')
        return filename[:x:] + '_S.png', img_size2[0], img_size2[1]


def cut_draw(filename):
    img = Image.open(filename)
    img_size = img.size
    t = 1280 / max(img_size)
    img_size2 = (int(img_size[0] * t), int(img_size[1] * t))
    img2 = img.resize(img_size2)
    img2.save(filename[:-4:] + '_D.png')
    return filename[:-4:] + '_D.png', img_size2[0], img_size2[1]


def load(file, data_file):
    # 数据加载到_D中
    img = cv2.imread(file)
    data = pd.read_csv(data_file, encoding='utf-8')
    a, b = data['start'], data['end']
    for start, end in zip(a, b):
        (x1, y1), (x2, y2) = eval(start), eval(end)
        x1y1, x2y2 = '%d,%d' % (x1, y1), '%d,%d' % (x2, y2)
        cv2.putText(img, x1y1, (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=1)
        cv2.line(img, (x1, y1), (x2, y2), color=(255, 0, 0), thickness=3)
    x2, y2 = eval(b[len(data['start'])-1])
    x2y2 = '%d,%d' % (x2, y2)
    cv2.putText(img, x2y2, (x2, y2), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=1)
    cv2.imwrite(file, img)


# plotTool = plotTool()
# plotTool.draw("pic/1_D.png", 'test')
