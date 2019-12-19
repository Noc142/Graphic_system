# TODO:
#       回退： 存操作&存对象
#       鼠标事件转成命令行操作
#       鲁棒性：命令行错误 弹窗提示 e.g.裁剪非直线
#       GUI裁剪
#       按钮提示
#       曲线控制点, canvas的显示
#       鼠标按下

from base import*
from line import*
from circle import*
from polygon import*
from curve import*

class GUI:
    def __init__(self):
        # 初始化
        self.init_basic()
        # 初始化GUI框架
        self.init_GUI()
        # 图像显示相关
        self.init_papers()
        # 鼠标事件相关
        self.init_mouse()
        # 基础按钮等
        self.init_buttons_basic()
        # 鼠标图元变换相关
        self.init_change()
        # 命令行等其他的按键
        self.init_buttons_files()
        # 菜单栏：
        self.menubar = Menu(self.top)
        self.init_menubar()
        # 曲线的控制点显示和拖拽
        self.init_curve_drawing()
        # pack
        self.pack_n_run()

    def init_basic(self):
        self.color_r = 0
        self.color_g = 0
        self.color_b = 0
        self.size_x = 500
        self.size_y = 500
        self.primitives = []  # 已经创建的图元 用于撤销等操作
        self.save_name = "temp.bmp"  # 要保存的文件名
        self.image = Image.new("RGB", (self.size_x, self.size_y), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def init_GUI(self):
        self.top = Tk()
        self.top.title("Painting_v2.4.0")
        self.top.geometry("1000x600+200+0")

    def init_papers(self):
        self.is_image_scaling = 0  # 1 for left, 2 for down, 3 for both
        self.photo = ImageTk.PhotoImage(self.image)
        self.paper = Canvas(self.top, width=1000, height=600, bg="gray")
        self.paper.create_image(2, 2, image=self.photo, anchor=NW)

    def init_buttons_basic(self):
        self.tmp_icon0 = self.getIcon(0)
        self.line_DDA = Button(self.top, command=lambda: self.set_type(self.line_type), text="直线", image=self.tmp_icon0)
        # self.line_Bre = Button(self.top, command=lambda: self.set_type(1), text="Bresenham直线")
        self.tmp_icon1 = self.getIcon(1)
        self.owl = Button(self.top, command=lambda: self.set_type(2), text="椭圆", image=self.tmp_icon1)
        self.tmp_icon2 = self.getIcon(2)   # next line: 3 for dda 4 for bresenham
        self.polygon = Button(self.top, command=lambda: self.set_type(3), text="多边形", image=self.tmp_icon2)
        self.tmp_icon3 = self.getIcon(3)
        self.curve = Button(self.top, command=lambda: self.set_type(4), text="曲线", image=self.tmp_icon3)
        self.tmp_icon4 = self.getIcon(4)
        self.translate = Button(self.top, command=lambda: self.set_type(5), text="平移", image=self.tmp_icon4)
        self.tmp_icon5 = self.getIcon(5)
        self.rotate = Button(self.top, command=lambda: self.set_type(6), text="旋转", image=self.tmp_icon5)
        self.tmp_icon6 = self.getIcon(6)
        self.scale = Button(self.top, command=lambda: self.set_type(7), text="缩放", image=self.tmp_icon6)
        # self.tmp_icon12 = self.getIcon(12)
        self.clip = Button(self.top, command=lambda: self.set_type(8), text="裁剪")  #, image=self.tmp_icon12)
        # self.save_but = Button(self.top, command=self.save_canvas, text="保存")
        self.is_polygon_painting = 0
        self.is_curve_painting = 0
        self.polygon_last_point = [0, 0]
        self.map = np.full((self.size_x, self.size_y), -1)

    def init_buttons_files(self):
        self.tmp_icon8 = self.getIcon(8)
        self.cl = Button(self.top, command=self.cmd_line_window, text="打开文件", image=self.tmp_icon8)
        self.tmp_icon7 = self.getIcon(7)
        self.colorboard = Button(self.top, command=self.color_board_window, text='调色板', image=self.tmp_icon7)

        # 基础按键设置
        # self.draw_line = Button(self.top, command=self.draw_line_window, text="画直线")
        # self.draw_circle = Button(self.top, command=self.draw_circle_window, text="画椭圆")
        self.tmp_icon9 = self.getIcon(9)
        self.clean = Button(self.top, command=self.clean_pic, text="清除画布", image=self.tmp_icon9)
        self.tmp_icon10 = self.getIcon(10)
        self.close = Button(self.top, command=self.top.destroy, text="关闭", image=self.tmp_icon10)

    def init_change(self):
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
        # self.primitive_clipping = -1
        self.is_clipping = 0
        self.clip_point = [-1, -1]
        self.clip_alg = ''
        self.clipped = 0

        # self.

    def init_mouse(self):
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

    def init_menubar(self):
        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='文件', menu=filemenu)
        filemenu.add_cascade(label='打开命令行文件', command=self.cmd_line_window)
        filemenu.add_command(label='清除画布', command=self.clean_pic)
        filemenu.add_command(label='保存', command=self.save_by_mouse)
        filemenu.add_command(label='退出', command=self.top.destroy)

        drawmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="绘图", menu=drawmenu)

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

    def init_curve_drawing(self):
        self.display_ctrl_point = 0
        self.ctrl_point_check = Checkbutton(self.top, text="显示控制点", command=self.change_dis_ctrl_point)
        self.map_ctrl_point = np.full((self.size_x, self.size_y, 2), -1)
        self.is_curve_modifying = 0
        self.curve_modify_num = [-1, -1]

    def change_dis_ctrl_point(self):
        self.display_ctrl_point = 1 if self.display_ctrl_point==0 else 0
        self.refresh()

    def pack_dis_ctrl_point(self, p):
        if p==1:
            self.ctrl_point_check.grid(row=0, column=20)
        else:
            self.ctrl_point_check.grid_forget()

    def pack_n_run(self):
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
        self.clip.grid(row=0, column=7)
        self.colorboard.grid(row=0, column=8)

        # self.paper.grid(row=1, column=5)
        self.paper.place(x=0, y=30)
        self.cl.grid(row=0, column=9)
        self.clean.grid(row=0, column=10)
        self.close.grid(row=0, column=11)
        self.pack_dis_ctrl_point(1)
        self.pack_dis_ctrl_point(0)
        # self.draw_line.grid(row=3, column=0)
        # self.draw_circle.grid(row=3, column=1)
        self.top.config(menu=self.menubar)

        os.remove("tmp.ico")

        self.top.mainloop()

    @staticmethod
    def getIcon(s):
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(imgs.icons[s]))
        tmp.close()
        return PhotoImage(file='tmp.ico')

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
        tmp = colorchooser.askcolor(parent=self.top, title='选择画笔颜色', color='blue')
        if tmp != (None, None):
            color_t =tmp
            self.color_r = int(color_t[0][0])
            self.color_g = int(color_t[0][1])
            self.color_b = int(color_t[0][2])
            print(self.color_r, self.color_g, self.color_b, color_t)

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
        # if self.display_ctrl_point==1:
        #     print(1111)
        # else:
        #     print("0000")
        self.paper.delete(ALL)
        self.image = Image.new("RGB", (self.size_x, self.size_y), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.map = np.full((self.size_x, self.size_y), -1)
        i = 0
        for primitive in self.primitives:
            pixels = primitive.get_pixels()
            for point in pixels:
                if (point[0] >= 0) and (point[1] >= 0) and (point[0] <= self.size_x-1) and (point[1] <= self.size_y-1):
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
        if self.type>=4 and self.display_ctrl_point==1:  # 绘制曲线控制点和虚线
            self.map_ctrl_point = np.full((self.size_x, self.size_y, 2), -1)
            for i in range(self.primitives.__len__()):
                if self.primitives[i].__class__.__name__ == 'Curve':
                    vertex = self.primitives[i].get_vertexes()
                    for j in range(vertex.__len__()):
                        self.paper.create_oval(vertex[j][0]-2, vertex[j][1]-2, vertex[j][0]+2, vertex[j][1]+2)
                        if 0<=vertex[j][0]<=self.size_x-1 and 0<=vertex[j][1]<=self.size_y-1:
                            self.map_ctrl_point[vertex[j][0]][vertex[j][1]] = [i, j]
                        if j >= 1:
                            self.paper.create_line(vertex[j-1][0], vertex[j-1][1], vertex[j][0], vertex[j][1],
                                                   fill='red', dash=(4, 4))

        # t2 = int(round(time.time() * 1000))
        # print("timecost:", t2-t1)

    def leftdown(self, event):
        self.cur = self.primitives.__len__()
        self.start_x = event.x
        self.start_y = event.y
        def find(point, map_t):
            res = -1
            for i in range(point[0] - 5, point[0] + 5):
                for j in range(point[1] - 5, point[1] + 5):
                    if (i >= 0) and (i <= self.size_x-1) and (j > 0) and (j <= self.size_y-1):
                        if map_t[i][j] >= 0:
                            if res == -1:
                                res = map_t[i][j]
                            elif map_t[i][j] != res:
                                res = -1
                                return res
            # print("select ", res)
            return res
        def find_curve(point, map_t):
            res = [-1, -1]
            for i in range(point[0] - 5, point[0] + 5):
                for j in range(point[1] - 5, point[1] + 5):
                    if (i >= 0) and (i <= self.size_x-1) and (j > 0) and (j <= self.size_y-1):
                        if map_t[i][j][0] >=0:
                            if res == [-1, -1]:
                                res = map_t[i][j]
                            elif map_t[i][j][0] != res[0]:
                                res = [-1, -1]
                                return res
            # print("select ", res)
            return res
        color = [self.color_r, self.color_g, self.color_b]
        if self.size_x-5 <= event.x <= self.size_x+5 and self.size_y-5 <= event.y <= self.size_y+5:
            self.is_image_scaling = 3
        elif self.size_x-5 <= event.x <= self.size_x+5:
            self.is_image_scaling = 1
        elif self.size_y-5 <= event.y <= self.size_y+5:
            self.is_image_scaling = 2
        # elif 0 <= event.x <=self.size_x and 0 <= event.y <= self.size_y:
        elif self.type == 0 or self.type == 1:
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
            tmp = [-1, -1]
            if self.display_ctrl_point == 1:
                tmp = find_curve([event.x, event.y], self.map_ctrl_point)
            if tmp[0] != -1:
                self.is_curve_modifying = 1
                self.curve_modify_num = tmp
                # print(tmp)
                self.is_curve_painting = 0
            elif self.is_curve_painting == 0:
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
            self.primitive_changing = find([event.x, event.y], self.map)
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
                self.primitive_changing = find([event.x, event.y], self.map)
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
                self.primitive_changing = find([event.x, event.y], self.map)
                self.primitives[self.primitive_changing].change(1)
                if self.primitive_changing >= 0:
                    print('a')
                    self.start_distance = math.sqrt(pow(event.x - self.scale_point[0], 2) +
                                                    pow(event.y - self.scale_point[1], 2))
        elif self.type == 8:
            if self.is_clipping == 1:
                self.last_point = [event.x, event.y]
            else:
                self.primitive_changing = find([event.x, event.y], self.map)
                if self.primitive_changing >= 0 and self.primitives[self.primitive_changing].__class__.__name__=='Line':
                    self.is_clipping = 1




        # print("press", event.x, event.y)

    def leftmove(self, event):
        x = event.x
        y = event.y
        # print("pass", x, y)
        # temp_list = []
        if self.is_image_scaling > 0:
            self.cur -= 1
            if self.is_image_scaling == 1:
                self.size_x = 1000 if x>=1000 else x
            elif self.is_image_scaling == 2:
                self.size_y = 600 if y>=600 else y
            else:
                self.size_x = 1000 if x>=1000 else x
                self.size_y = 600 if y>=600 else y
            self.set_type(self.type)
        elif self.type == 0 or self.type == 1:
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
            if self.is_curve_modifying == 1:
                self.primitives[self.curve_modify_num[0]].modify(self.curve_modify_num[1], [x, y])
            else:
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
        elif self.type == 8 and self.primitive_changing != -1 and self.is_clipping==1:
            self.clip_point = [x, y]
            self.clip_alg = 'Cohen-Sutherland'
            tmp_line = self.primitives[self.primitive_changing]

            tmp_line.clip(self.last_point[0], self.last_point[1],
                                                          self.clip_point[0], self.clip_point[1],
                                                          self.clip_alg)
            self.clipped = 1
            # 类的赋值有问题
            # 得到像素画出来
            #TODO: 算法选择， 直线和裁剪框的标识
        self.refresh()
        # print("refreshed")

    def leftrelease(self, event):
        if self.is_image_scaling >0:
            self.is_image_scaling = 0
        elif self.type==0 or self.type == 1 or self.type == 2:
            self.cur = self.primitives.__len__()
        elif self.type == 3:
            self.primitives[self.cur].update_rasterization([event.x, event.y])
            self.polygon_last_point = [event.x, event.y]
            self.refresh()
        elif self.type == 4:
            if self.is_curve_modifying == 1:
                self.primitives[self.curve_modify_num[0]].modify(self.curve_modify_num[1], [event.x, event.y])
                self.is_curve_modifying = 0
            else:
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
        elif self.type == 8 and self.clipped == 1:
            self.primitives[self.primitive_changing].clip(self.last_point[0], self.last_point[1],
                                                          self.clip_point[0], self.clip_point[1],
                                                          self.clip_alg)
            self.clipped = 0
            self.is_clipping = 0
            self.primitive_changing = -1
        # print("release")

    def double_left_click(self, event):
        print("double!")
        if self.type == 3 and self.is_polygon_painting == 1:
            self.primitives[self.cur].update_rasterization([event.x, event.y])
            self.polygon_last_point = [event.x, event.y]
            self.refresh()

    def set_type(self, type_t):  # 设置鼠标画图的类型
        self.type = type_t
        if type_t>=4:
            self.pack_dis_ctrl_point(1)
        else:
            self.pack_dis_ctrl_point(0)
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
        self.refresh()
        # self.primitive_changing = -1

if __name__ == '__main__':
    gui = GUI()