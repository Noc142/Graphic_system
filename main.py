
"""
    v1.1.0update 2019/10/26
    添加了基础功能：读取命令行文件
    实现了重置画布/保存画布/设置画笔颜色/画线段/画椭圆/画多边形的命令

    v1.0.4update 2019/10/21
    实现了通过获取鼠标事件绘制多边形

    v1.0.3update 2019/10/20
    添加了获取鼠标事件来调用DDA算法、Bresenham算法以及中点椭圆算法的功能
    运行效率还说得过去

    v1.0.2update 2019/10/19
    修改了画图逻辑：每次出现新的图元或者有图元修改时
    使用GUI.update函数对图片进行刷新，刷新过程中遍历所有图元的所有点
    这样在删除/修改某个图元后。原先被盖住的像素可以还原
    经测试，图元数量为80个以下时，刷新时间能够控制在100ms以下

    v1.0.1 update  2019/10/15
    将直接在tkinter.canvas上画线以代替点的画图方式修改为用PIL画图然后粘贴到canvas上
    这样可以对单个像素进行操作而不是直接在tkinter.Canvas上画线曲线救国，一定程度提高了效率

    v1.0.0
    完成了初步框架
"""

# TODO:
#       调整按钮布局
#       读取鼠标数据：右键等更多功能
#       关闭有的时候要点两次 不知道为啥 ：关闭的command改成了destroy, 以后行不行有待检验
#       做一下反走样？
#       输入框为空的时候 处理一下 弹出一个messagebox
#       双击结束
#       纯命令行
#       回退： 存操作&存对象
#       鼠标事件转成命令行操作
#       图元文件的保存和读取
#       鲁棒性：命令行错误 弹窗提示 e.g.裁剪非直线
#       缩放的误差 手动时特别明显
#       椭圆旋转有错误

from base import*
from line import*
from circle import*
from polygon import*
from curve import*

class GUI:
    def __init__(self):
        self.top = Tk()
        self.top.title("Painting_v2.4.0")
        self.top.geometry("1000x750+300+0")
        self.color_r = 0
        self.color_g = 0
        self.color_b = 0
        self.size_x = 500
        self.size_y = 500
        self.primitives = []  # 已经创建的图元 用于撤销等操作
        self.save_name = "temp.bmp"  # 要保存的文件名

        # 图像显示相关
        self.image = Image.new("RGB", (self.size_x, self.size_y), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.paper = Canvas(self.top, width=800, height=600, bg="gray")
        self.paper.create_image(2, 2, image=self.photo, anchor=NW)

        # 鼠标事件相关
        self.cur = self.primitives.__len__()  # 当前正在绘制的图元的数组下标
        self.start_x = 0  # 图元初始坐标
        self.start_y = 0
        self.type = 1  # 种类 0 for DDA line, 1 for Bresenham Line
        self.paper.bind('<Button-1>', self.leftdown)
        self.paper.bind('<B1-Motion>', self.leftmove)
        self.paper.bind('<ButtonRelease-1>', self.leftrelease)
        self.paper.bind('<Double-Button-1> ', self.double_left_click)
        self.line_type = 1
        self.polygon_type = 1
        self.curve_type = 1

        # icon = Image.open('drawLine.png')
        # drawLineIcon = tkinter.PhotoImage(file='drawLine.png')
        # drawLineIcon = ImageTk.PhotoImage(icon.resize((20, 20), Image.ANTIALIAS))
        # def getIcon(s):
        #     tmp = open("tmp.ico", "wb+")
        #     tmp.write(base64.b64decode(imgs.drawLineicon))  # 写入到临时文件中
        #     tmp.close()
        #     return PhotoImage(file='tmp.ico')
        # tmp = open("tmp.ico", "wb+")
        # tmp.write(base64.b64decode(imgs.drawLineicon))  # 写入到临时文件中
        # tmp.close()
        # abc = PhotoImage(file='tmp.ico')

        tmp_icon0 = self.getIcon(0)
        self.line_DDA = Button(self.top, command=lambda: self.set_type(self.line_type), text="直线", image=tmp_icon0)
        # self.line_Bre = Button(self.top, command=lambda: self.set_type(1), text="Bresenham直线")
        tmp_icon1 = self.getIcon(1)
        self.owl = Button(self.top, command=lambda: self.set_type(2), text="椭圆", image=tmp_icon1)
        tmp_icon2 = self.getIcon(2)   # next line: 3 for dda 4 for bresenham
        self.polygon = Button(self.top, command=lambda: self.set_type(3), text="多边形", image=tmp_icon2)
        tmp_icon3 = self.getIcon(3)
        self.curve = Button(self.top, command=lambda: self.set_type(4), text="曲线", image=tmp_icon3)
        tmp_icon4 = self.getIcon(4)
        self.translate = Button(self.top, command=lambda: self.set_type(5), text="平移", image=tmp_icon4)
        tmp_icon5 = self.getIcon(5)
        self.rotate = Button(self.top, command=lambda: self.set_type(6), text="旋转", image=tmp_icon5)
        tmp_icon6 = self.getIcon(6)
        self.scale = Button(self.top, command=lambda: self.set_type(7), text="缩放", image=tmp_icon6)
        # self.save_but = Button(self.top, command=self.save_canvas, text="保存")
        self.is_polygon_painting = 0
        self.is_curve_painting = 0
        self.polygon_last_point = [0, 0]
        self.map = np.full((self.size_x, self.size_y), -1)

        # 图元变换相关
        self.primitive_changing = 0
        self.last_point = [-1, -1]
        self.is_translating = 0
        self.rotate_point = [-1, -1]
        self.is_rotating = 0
        # self.is_primitive_rotating = 0
        self.start_angle = 0  # 弧度
        self.scale_point = [-1, -1]
        self.is_scaling = 0
        self.start_distance = 0

        # 命令行的按键
        tmp_icon8 = self.getIcon(8)
        self.cl = Button(self.top, command=self.cmd_line_window, text="打开文件", image=tmp_icon8)
        tmp_icon7 = self.getIcon(7)
        self.colorboard = Button(self.top, command=self.color_board_window, text='调色板', image=tmp_icon7)

        # 基础按键设置
        # self.draw_line = Button(self.top, command=self.draw_line_window, text="画直线")
        # self.draw_circle = Button(self.top, command=self.draw_circle_window, text="画椭圆")
        tmp_icon9 = self.getIcon(9)
        self.clean = Button(self.top, command=self.clean_pic, text="清除画布", image=tmp_icon9)
        tmp_icon10 = self.getIcon(10)
        self.close = Button(self.top, command=self.top.destroy, text="关闭", image=tmp_icon10)

        # 菜单栏：
        menubar = Menu(self.top)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='文件', menu=filemenu)
        filemenu.add_cascade(label='打开命令行文件', command=self.cmd_line_window)
        filemenu.add_command(label='清除画布', command=self.clean_pic)
        filemenu.add_command(label='保存', command=self.save_by_mouse)
        filemenu.add_command(label='退出', command=self.top.destroy)

        drawmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="绘图", menu=drawmenu)

        def set_draw_type(pri, type_t):
            if pri=='line':
                self.line_type = type_t
            elif pri=='polygon':
                self.polygon_type = type_t
            elif pri=='curve':
                if self.curve_type != type_t:
                    self.is_curve_painting = 0
                self.curve_type = type_t
        sub_menu_line = Menu(drawmenu, tearoff=0)
        drawmenu.add_cascade(label="直线绘制算法", menu=sub_menu_line)
        sub_menu_line.add_radiobutton(label="DDA", command=lambda: set_draw_type('line', 1))  # command
        sub_menu_line.add_radiobutton(label="Bresenham", command=lambda: set_draw_type('line', 2))
        sub_menu_polygon = Menu(drawmenu, tearoff=0)
        drawmenu.add_cascade(label="多边形绘制算法", menu=sub_menu_polygon)
        sub_menu_polygon.add_radiobutton(label="DDA", command=lambda: set_draw_type('polygon', 1))  # command
        sub_menu_polygon.add_radiobutton(label="Bresenham", command=lambda: set_draw_type('polygon', 2))
        sub_menu_curve = Menu(drawmenu, tearoff=0)
        drawmenu.add_cascade(label="曲线绘制算法", menu=sub_menu_curve)
        sub_menu_curve.add_radiobutton(label="Bezier", command=lambda: set_draw_type('curve', 1))  # command
        sub_menu_curve.add_radiobutton(label="B-spline", command=lambda: set_draw_type('curve', 2))


        # pack， TODO：位置设置
        self.line_DDA.grid(row=0, column=0)
        # self.line_DDA.place(x=0, y=0)
        # self.line_Bre.grid(row=0, column=1)
        self.owl.grid(row=0, column=1)
        self.polygon.grid(row=0, column=2)
        self.curve.grid(row=0, column=3)
        self.translate.grid(row=0, column=4)
        self.rotate.grid(row=0, column=5)
        self.scale.grid(row=0, column=6)
        self.colorboard.grid(row=0, column=7)

        # self.paper.grid(row=1, column=5)
        self.paper.place(x=0, y=30)
        self.cl.grid(row=0, column=9)
        self.clean.grid(row=0, column=10)
        self.close.grid(row=0, column=11)
        # self.draw_line.grid(row=3, column=0)
        # self.draw_circle.grid(row=3, column=1)
        self.top.config(menu=menubar)

        os.remove("tmp.ico")

        self.top.mainloop()

    def getIcon(self, s):
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(imgs.icons[s]))
        tmp.close()
        return PhotoImage(file='tmp.ico')

    # def draw_line_window(self):
    #     in_put = Toplevel()
    #     in_put.title("画直线")
    #     in_put.geometry("600x100+605+300")
    #     Label(in_put, text="第一个点的横坐标：").grid(row=0, column=0)
    #     Label(in_put, text="第一个点的纵坐标：").grid(row=0, column=2)
    #     Label(in_put, text="第二个点的横坐标：").grid(row=1, column=0)
    #     Label(in_put, text="第二个点的纵坐标：").grid(row=1, column=2)
    #     x1 = Entry(in_put)
    #     y1 = Entry(in_put)
    #     x2 = Entry(in_put)
    #     y2 = Entry(in_put)
    #     x1.grid(row=0, column=1)
    #     y1.grid(row=0, column=3)
    #     x2.grid(row=1, column=1)
    #     y2.grid(row=1, column=3)
    #     draw_DDA = Button(in_put, command=lambda: self.draw_line_primitive(x1, y1, x2, y2, 1), text="DDA算法")
    #     draw_Bresenham = Button(in_put, command=lambda: self.draw_line_primitive(x1, y1, x2, y2, 2), text="Bresenham算法")
    #     close = Button(in_put, command=in_put.destroy, text="关闭")  # 子窗口关闭用destroy不用quit
    #     draw_DDA.grid(row=2, column=0)
    #     draw_Bresenham.grid(row=2, column=1)
    #     close.grid(row=2, column=3)
    #     # draw.pack()
    #     # close.pack()
    #     in_put.mainloop()
    #     print("done")
    #
    # def draw_circle_window(self):
    #     in_put = Toplevel()
    #     in_put.title("画椭圆")
    #     in_put.geometry("600x100+605+300")
    #     Label(in_put, text="圆心的横坐标：").grid(row=0, column=0)
    #     Label(in_put, text="圆心的纵坐标：").grid(row=0, column=2)
    #     Label(in_put, text="长半轴：").grid(row=1, column=0)
    #     Label(in_put, text="短半轴：").grid(row=1, column=2)
    #     x = Entry(in_put)
    #     y = Entry(in_put)
    #     rx = Entry(in_put)
    #     ry = Entry(in_put)
    #     x.grid(row=0, column=1)
    #     y.grid(row=0, column=3)
    #     rx.grid(row=1, column=1)
    #     ry.grid(row=1, column=3)
    #     draw = Button(in_put, command=lambda: self.draw_circle_primitive(x, y, rx, ry), text="开始")
    #     close = Button(in_put, command=in_put.destroy, text="关闭")
    #     draw.grid(row=2, column=0)
    #     close.grid(row=2, column=3)
    #     in_put.mainloop()

    def cmd_line_window(self):
        in_put = Toplevel()
        # in_put.wm_attributes('-topmost', 1)
        # in_put.withdraw()
        in_put.protocol('WM_DELETE_WINDOW', in_put.withdraw)
        in_put.title("打开文件")
        in_put.geometry("330x100+605+300")
        Label(in_put, text="文件名：").grid(row=0, column=0)
        Label(in_put, text="输出图元保存位置：").grid(row=1, column=0)
        file_name_path = StringVar()
        save_path_path = StringVar()
        file_name = Entry(in_put, textvariable=file_name_path)
        save_path = Entry(in_put, textvariable=save_path_path)
        file_name.grid(row=0, column=1)
        save_path.grid(row=1, column=1)
        open_file = Button(in_put, command=lambda: self.open_file(file_name_path), text="打开文件")
        chose = Button(in_put, command=lambda: self.select_dir(save_path_path), text="选择文件夹")
        begin = Button(in_put, command=lambda: self.cmd_line_act(file_name, save_path), text="开始")
        close = Button(in_put, command=in_put.destroy, text="关闭")
        open_file.grid(row=0, column=2)
        chose.grid(row=1, column=2)
        begin.grid(row=2, column=0)
        close.grid(row=2, column=1)
        in_put.mainloop()

    def open_file(self, path):
        name = tkfl.askopenfilename(filetypes=[("文本文档", ".txt")])
        print(name)
        path.set(name)

    def select_dir(self, path):
        name = tkfl.askdirectory()
        print(name)
        path.set(name)

    def save_by_mouse(self):
        path = StringVar()
        path = tkfl.asksaveasfilename(filetypes=[('bmp文件', '.bmp')])
        print(path)
        if path != '':
            self.save_name = path
            self.save_canvas()

    def color_board_window(self):
        color_t = colorchooser.askcolor(parent=self.top, title='选择画笔颜色', color='blue')
        self.color_r = int(color_t[0][0])
        self.color_g = int(color_t[0][1])
        self.color_b = int(color_t[0][2])
        print(self.color_r, self.color_g, self.color_b, color_t)

    def draw_line_primitive(self, x1, y1, x2, y2, method):   # 通用的 vertex是输入框的list的list 待添加更多参数以区分形状
                                                            # method也可以用来区分是否为多边形传入的直线，这样就不用对直线创建新的图元了
        vertex = [[int(x1.get()), int(y1.get())], [int(x2.get()), int(y2.get())]]
        color = [self.color_r, self.color_g, self.color_b]
        line_2b_drawn = Line(vertex, self.primitives.__len__(), method, color)
        line_2b_drawn.rasterization()
        self.primitives.append(line_2b_drawn)
        # print(points)
        # for i in points:
        #     self.print_pixel(i[0], i[1])
        self.refresh()
        # self.image.show()

    def draw_circle_primitive(self, x, y, rx, ry):
        vertex = [[int(x.get()), int(y.get())], [int(rx.get()), int(ry.get())]]
        color = [self.color_r, self.color_g, self.color_b]
        circle_2b_drawn = Circle(vertex, self.primitives.__len__(), color)
        circle_2b_drawn.rasterization()
        self.primitives.append(circle_2b_drawn)
        # for i in points:
        #     self.print_pixel(i[0], i[1])
        self.refresh()

    def cmd_line_act(self, file_name, save_path):
        file = file_name.get()
        if file=='':
            file = 'input.txt'
        path = save_path.get()
        # 保存时 修改self.save_name
        cmd_file = open(file, "r")
        lines = 0  # 跨行时的参数 下面三个也是
        line2_id = 0
        line2_n = 0
        line2_alg = ""
        for cmd in cmd_file.readlines():
            # 如果涉及到跨行， 即多边形和曲线， 设置一个多余的参数
            color = [self.color_r, self.color_g, self.color_b]
            words = cmd.split()
            if words[0] == "resetCanvas":
                print("reset")
                self.size_x = int(words[1])
                self.size_y = int(words[2])
                self.clean_pic()
            elif words[0] == "saveCanvas":
                print("save")
                if path != '':
                    self.save_name = path + "/" + words[1] + ".bmp"
                else:
                    self.save_name = words[1] + ".bmp"
                self.save_canvas()
            elif words[0] == "setColor":
                print("setColor")
                self.color_r = int(words[1])
                self.color_g = int(words[2])
                self.color_b = int(words[3])
            elif words[0] == "drawLine":
                print("Line")
                vertex = [[int(words[2]), int(words[3])], [int(words[4]), int(words[5])]]
                pid = int(words[1])
                alg = 1 if words[6]=="DDA" else 2
                line_2b_drawn = Line(vertex, pid, alg, color)
                self.primitives.append(line_2b_drawn)
                # print(self.primitives.__len__())
                self.refresh()
            elif words[0] == "drawPolygon":
                print("Polygon")
                lines = 1
                line2_id = int(words[1])
                line2_n = int(words[2])
                line2_alg = 1 if words[3]=="DDA" else 2
            elif words[0] == "drawEllipse":
                print("Ellipse")
                vertex = [[int(words[2]), int(words[3])], [int(words[4]), int(words[5])]]
                pid = int(words[1])
                circle_2b_drawn = Circle(vertex, pid, color)
                self.primitives.append(circle_2b_drawn)
                self.refresh()
            elif words[0] == "drawCurve":
                print("Curve")
                lines = 2
                line2_id = int(words[1])
                line2_n = int(words[2])
                # TODO: alg
                line2_alg = 1 if words[3] == "Bezier" else 2
            elif words[0] == "translate":
                print("translate")
                for i in range(len(self.primitives)):
                    if int(words[1]) == self.primitives[i].get_id():
                        # num = i
                        self.primitives[i].translate(int(words[2]), int(words[3]))
                        break
                self.refresh()
            elif words[0] == "rotate":
                print("rotate")
                for i in range(len(self.primitives)):
                    if int(words[1]) == self.primitives[i].get_id():
                        # num = i
                        self.primitives[i].rotate(int(words[2]), int(words[3]), int(words[4]))
                        break
                self.refresh()
            elif words[0] == "scale":
                print("scale")
                for i in range(len(self.primitives)):
                    if int(words[1]) == self.primitives[i].get_id():
                        self.primitives[i].scale(int(words[2]), int(words[3]), int(words[4]))
                        break
                self.refresh()
            elif words[0] == "clip":
                print("clip")
                for i in range(len(self.primitives)):
                    if int(words[1]) == self.primitives[i].get_id():
                        self.primitives[i].clip(int(words[2]), int(words[3]), int(words[4]), int(words[5]), words[6])
                        break
                self.refresh()
            elif lines == 1:  # polygon
                print("Polygon, 2nd line")
                vertex = []
                for i in range(line2_n):
                    point = [int(words[2*i]), int(words[2*i+1])]
                    vertex.append(point)
                polygon_2b_drawn = Polygon(vertex, line2_id, line2_alg, 1, color)
                self.primitives.append(polygon_2b_drawn)
                self.refresh()
                lines = 0
            elif lines == 2:  # curve
                print("Curve, 2nd line")
                vertex = []
                for i in range(line2_n):
                    point = [int(words[2 * i]), int(words[2 * i + 1])]
                    vertex.append(point)
                alg = 'Bezier' if line2_alg == 1 else 'B-spline'
                curve_2b_drawn = Curve(vertex, line2_id, alg, 1, color)
                self.primitives.append(curve_2b_drawn)
                self.refresh()
                lines = 0
            else:
                notification = "指令\""+words[0] + "\"解析失败"
                tkinter.messagebox.showinfo("提示", notification)
                break

    def clean_pic(self):
        self.paper.delete(ALL)
        self.primitives = []
        self.rotate_point = [-1, -1]
        self.scale_point = [-1, -1]
        self.refresh()
        self.is_curve_painting = 0
        self.is_polygon_painting = 0
        self.is_rotating = 0

        # self.image = Image.new("RGB", (self.size_x, self.size_y), (255, 255, 255))
        # self.draw = ImageDraw.Draw(self.image)
        # self.paper.create_image(0, 0, image=self.photo, anchor=NW)
        print("clean_pic")

    def save_canvas(self):
        # file_name = "temp.bmp"
        self.image.save(self.save_name)

    def refresh(self):
        # t1 = int(round(time.time() * 1000))
        # self.image.show()
        # print("refresh!")
        self.image = Image.new("RGB", (self.size_x, self.size_y), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.map = np.full((self.size_x, self.size_y), -1)
        i = 0
        for primitive in self.primitives:
            pixels = primitive.get_pixels()
            for point in pixels:
                if (point[0] >= 0) and (point[1] >= 0) and (point[0] <= 499) and (point[1] <= 499):
                    # self.draw.point((point[0], point[1]), fill=self.color_r + self.color_g*256 + self.color_b*256*256)
                    self.draw.point((point[0], point[1]), fill=primitive.get_color())
                    if self.map[point[0]][point[1]] == -1:
                        self.map[point[0]][point[1]] = i
                    else:
                        self.map[point[0]][point[1]] = -2
            i = i + 1
            # print("drawn", primitive.pno)
        self.photo = ImageTk.PhotoImage(self.image)
        self.paper.create_image(2, 2, image=self.photo, anchor=NW)
        if self.rotate_point != [-1, -1]:
            self.paper.create_oval(self.rotate_point[0]-2, self.rotate_point[1]-2,
                                   self.rotate_point[0]+2, self.rotate_point[1]+2,
                                   fill='red')
        if self.scale_point != [-1, -1]:
            self.paper.create_oval(self.scale_point[0]-2, self.scale_point[1]-2,
                                   self.scale_point[0]+2, self.scale_point[1]+2,
                                   fill='green')
        # t2 = int(round(time.time() * 1000))
        # print("timecost:", t2-t1)

    def leftdown(self, event):
        self.cur = self.primitives.__len__()
        self.start_x = event.x
        self.start_y = event.y
        color = [self.color_r, self.color_g, self.color_b]
        def find(point):
            res = -1
            for i in range(point[0] - 5, point[0] + 5):
                for j in range(point[1] - 5, point[1] + 5):
                    if (i >= 0) and (i <= 499) and (j > 0) and (j <= 499):
                        if self.map[i][j] >= 0:
                            if res == -1:
                                res = self.map[i][j]
                            elif self.map[i][j] != res:
                                res = -1
                                return res
            print("select ", res)
            return res
        if self.type == 0 or self.type == 1:
            temp_list = [[self.start_x, self.start_y], [self.start_x, self.start_y]]
            line_being_drawn = Line(temp_list, self.primitives.__len__(), self.line_type, color)
            self.primitives.append(line_being_drawn)
        elif self.type == 2:
            owl_being_drawn = Circle([[self.start_x, self.start_y], [0, 0]], self.primitives.__len__(), color)
            self.primitives.append(owl_being_drawn)
        elif self.type ==3:
            if self.is_polygon_painting == 0:
                polygon_being_drawn = Polygon([[self.start_x, self.start_y]], self.primitives.__len__(),
                                              self.polygon_type, 0, color)
                self.primitives.append(polygon_being_drawn)
                self.is_polygon_painting = 1
            else:
                self.cur -= 1
                self.primitives[self.cur].updating([event.x, event.y])
        elif self.type==4:  # curve
            if self.is_curve_painting == 0:
                curve_being_drawn = Curve([[self.start_x, self.start_y],[self.start_x, self.start_y]],
                                          self.primitives.__len__(),
                                          ('Bezier' if self.curve_type==1 else 'B-spline'), 0, color)
                self.primitives.append(curve_being_drawn)
                self.is_curve_painting = 1
            else:
                self.cur -= 1
                self.primitives[self.cur].begin_update([event.x, event.y])
            self.refresh()
        elif self.type ==5:
            # print(self.map[50])
            self.primitive_changing = find([event.x, event.y])
            if self.primitive_changing >= 0:
                self.is_translating = 1
                self.last_point = [event.x, event.y]
                print("found")
        elif self.type == 6:
            print("rotate")
            if self.is_rotating == 0:
                self.rotate_point = [event.x, event.y]
                self.is_rotating = 1
                self.refresh()
            else:
                self.primitive_changing = find([event.x, event.y])
                if self.primitive_changing >= 0:
                    # self.is_rotating = 1
                    self.primitives[self.primitive_changing].change(1)
                    if event.x == self.rotate_point[0]:
                        self.start_angle = math.pi/2 if event.y - self.rotate_point[1] > 0 else -math.pi/2
                    else:
                        self.start_angle = math.atan((event.y - self.rotate_point[1])/(event.x - self.rotate_point[0]))
                        if event.x - self.rotate_point[0] < 0:
                            self.start_angle = self.start_angle + math.pi
                    # self.last_point = [event.x, event.y]
        elif self.type == 7:
            if self.is_scaling == 0:
                self.scale_point = [event.x, event.y]
                self.is_scaling = 1
                self.refresh()
            else:
                self.primitive_changing = find([event.x, event.y])
                self.primitives[self.primitive_changing].change(1)
                if self.primitive_changing >= 0:
                    print('a')
                    self.start_distance = math.sqrt(pow(event.x - self.scale_point[0], 2) +
                                                    pow(event.y - self.scale_point[1], 2))

        print("press", event.x, event.y)

    def leftmove(self, event):
        x = event.x
        y = event.y
        # print("pass", x, y)
        # temp_list = []
        if self.type == 0 or self.type == 1:
            temp_list = [[self.start_x, self.start_y], [x, y]]
            self.primitives[self.cur].vertex = temp_list
            self.primitives[self.cur].rasterization()
        elif self.type == 2:
            x_mid = int((x + self.start_x) / 2)
            y_mid = int((y + self.start_y) / 2)
            rx = int((abs(x - self.start_x)) / 2)
            ry = int((abs(y - self.start_y)) / 2)
            temp_list = [[x_mid, y_mid], [rx, ry]]
            self.primitives[self.cur].vertex = temp_list
            self.primitives[self.cur].rasterization()
        elif self.type == 3:
            self.primitives[self.cur].updating([x, y])
            # self.refresh()
        elif self.type == 4:
            self.primitives[self.cur].updating([x, y])
        # print(self.primitives[self.cur].vertex)
        # print(self.primitives[self.cur].pixels)
        elif self.type == 5 and self.is_translating == 1:
            self.primitives[self.primitive_changing].translate(x - self.last_point[0], y - self.last_point[1])
            self.last_point = [x, y]
        elif self.type == 6 and self.primitive_changing != -1:
            if x == self.rotate_point[0]:
                angle = math.pi/2 if y - self.rotate_point[1] > 0 else -math.pi/2
            else:
                angle = math.atan((y - self.rotate_point[1])/(x - self.rotate_point[0]))
                if x - self.rotate_point[0] < 0:
                    angle = angle + math.pi

            self.primitives[self.primitive_changing].rotate(self.rotate_point[0], self.rotate_point[1],
                                                            (angle - self.start_angle)*180 / math.pi)
            self.start_angle = angle  # 这里不应该叫"start"而是"last"
        elif self.type == 7 and self.primitive_changing != -1:
            cur_dis = math.sqrt(pow(event.x - self.scale_point[0], 2) +
                                pow(event.y - self.scale_point[1], 2))
            self.primitives[self.primitive_changing].scale(self.scale_point[0], self.scale_point[1],
                                                           cur_dis/self.start_distance)
            self.start_distance = cur_dis
        self.refresh()
        # print("refreshed")

    def leftrelease(self, event):
        if self.type==0 or self.type == 1 or self.type == 2:
            self.cur = self.primitives.__len__()
        elif self.type == 3:
            self.primitives[self.cur].update_rasterization([event.x, event.y])
            self.polygon_last_point = [event.x, event.y]
            self.refresh()
        elif self.type == 4:
            self.primitives[self.cur].updating([event.x, event.y])
            self.refresh()
        elif self.type == 5:
            self.is_translating = 0
            self.primitive_changing = -1
        elif self.type == 6:
            self.primitive_changing = -1
            self.primitives[self.primitive_changing].change(0)
        elif self.type == 7:
            self.primitive_changing = -1
            self.primitives[self.primitive_changing].change(0)
        print("release")

    def double_left_click(self, event):
        print("double!")
        if self.type == 3 and self.is_polygon_painting == 1:
            self.primitives[self.cur].update_rasterization([event.x, event.y])
            self.polygon_last_point = [event.x, event.y]
            self.refresh()

    def set_type(self, type_t):  # 设置鼠标画图的类型
        self.type = type_t
        if self.is_polygon_painting == 1:  # 完成多边形的绘制
            self.is_polygon_painting = 0
            self.primitives[self.cur].done()
            self.refresh()
        if self.is_curve_painting == 1:
            self.is_curve_painting = 0
            self.refresh()
        if self.is_rotating:
            self.is_rotating = 0
            self.rotate_point = [-1, -1]
            self.refresh()
        if self.is_scaling:
            self.is_scaling = 0
            self.scale_point = [-1, -1]
            self.refresh()
        # self.primitive_changing = -1

if __name__ == '__main__':
    gui = GUI()