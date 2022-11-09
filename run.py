# 楼棋建筑交通网络化 by Louis翔
from tkinter import *
import tkinter.filedialog
import plot
import Astar
import model

'''函数'''
filename0 = ''
width, height = 0, 0
data_file = ''


def openfile():
    # 图纸地址字符串，图纸展示
    global filename0, width, height, img_label
    filename0 = tkinter.filedialog.askopenfilename()    # 原始图纸路径
    filename = plot.cut_show(filename0, 0)[0]  # 展示图纸路径
    filename0, width, height = plot.cut_draw(filename0)       # 绘制图纸路径
    img = PhotoImage(file=filename)
    img_label.config(image=img)


def load_data():
    global data_file, filename0, width, height, img_label
    data_file = tkinter.filedialog.askopenfilename()
    plot.load(filename0, data_file)
    filename = plot.cut_show(filename0, 1)[0]
    img = PhotoImage(file=filename)
    img_label.config(image=img)


def draw(point_type: str, color: tuple):
    global filename0
    x = -1
    for i in filename0[::-1]:
        if i == '_':
            break
        x -= 1
    plotTool.draw(filename0, point_type, color, x)    # 生成数据和对应图纸
    filename0 = f'{filename0[:x:]}_{point_type}.png'   # 图源换为_area
    filename = plot.cut_show(filename0, x)[0]   # 重做_S
    img = PhotoImage(file=filename)
    img_label.config(image=img)


def first_model():
    print('开始建模')
    file = 'data/sj_barrier.csv'
    model.model(height, width, file)
    print('已构建栅格地图, 可以开始路径规划')


def astar():
    start, goal = plotTool.choose(filename0)
    file = 'data/sj_barrier.csv'
    way = Astar.astar_search(height, width, start, goal, file)
    print(way)
    plot.draw_path(way)


'''新建窗口'''
root = Tk()
root.title('楼棋——建模系统')
root.geometry('1280x640')
'''建立分区和预览图纸'''
frame1 = Frame(root, width=640, height=640)
frame1.place(relx=0, rely=0)
frame2 = Frame(root, width=640, height=640)
frame2.place(relx=0.5, rely=0)
img0 = PhotoImage(file='logo/Logo_S.png')
img_label = Label(frame1, image=img0)
img_label.pack()
'''开始标点'''
btn0 = Button(frame2, text='选择图纸', command=openfile)
btn0.pack()
plotTool = plot.plotTool()
btn1 = Button(frame2, text='加载数据', command=load_data)
btn1.pack()
btn2 = Button(frame2, text='绘制障碍区域', command=lambda: draw('barrier', (0, 0, 255)))
btn2.pack()
btn3 = Button(frame2, text='标注出入口', command=lambda: draw('passageway', (0, 255, 0)))
btn3.pack()
btn4 = Button(frame2, text='楼梯及坡道', command=lambda: draw('stair', (255, 0, 0)))
btn4.pack()
btn5 = Button(frame2, text='初次运行请建模', command=first_model)
btn5.pack()
btn6 = Button(frame2, text='选择起点和终点进行路径规划', command=astar)
btn6.pack()

root.mainloop()
