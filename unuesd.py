# def draw_line_primitive(self, x1, y1, x2, y2, method):   # 通用的 vertex是输入框的list的list 待添加更多参数以区分形状
#                                                         # method也可以用来区分是否为多边形传入的直线，这样就不用对直线创建新的图元了
#     vertex = [[int(x1.get()), int(y1.get())], [int(x2.get()), int(y2.get())]]
#     color = [self.color_r, self.color_g, self.color_b]
#     line_2b_drawn = Line(vertex, self.primitives.__len__(), method, color)
#     line_2b_drawn.rasterization()
#     self.primitives.append(line_2b_drawn)
#     # print(points)
#     # for i in points:
#     #     self.print_pixel(i[0], i[1])
#     self.refresh()
#     # self.image.show()
#
# def draw_circle_primitive(self, x, y, rx, ry):
#     vertex = [[int(x.get()), int(y.get())], [int(rx.get()), int(ry.get())]]
#     color = [self.color_r, self.color_g, self.color_b]
#     circle_2b_drawn = Circle(vertex, self.primitives.__len__(), color)
#     circle_2b_drawn.rasterization()
#     self.primitives.append(circle_2b_drawn)
#     # for i in points:
#     #     self.print_pixel(i[0], i[1])
#     self.refresh()
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