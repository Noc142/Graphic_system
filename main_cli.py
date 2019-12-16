from base import*
from line import*
from circle import*
from polygon import*
from curve import*
import sys

class CLI:
    def __init__(self, input, save):
        # 初始化
        self.color_r = 0
        self.color_g = 0
        self.color_b = 0
        self.size_x = 500
        self.size_y = 500
        self.primitives = []  # 已经创建的图元 用于撤销等操作
        self.save_name = "temp.bmp"  # 要保存的文件名
        self.image = Image.new("RGB", (self.size_x, self.size_y), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.cmd_line_act(input, save)




    def open_file(self, path):
        name = tkfl.askopenfilename(filetypes=[("文本文档", ".txt")])
        print(name)
        path.set(name)

    def select_dir(self, path):
        name = tkfl.askdirectory()
        print(name)
        path.set(name)


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

    def cmd_line_act(self, file_name, save_path):  # 这里 文件名是字符串了
        file = file_name
        if file=='':
            file = 'input.txt'
        path = save_path
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
                    if path[len(path)-1] !='/':
                        self.save_name = path + "/" + words[1] + ".bmp"
                    else:
                        self.save_name = path + words[1] + ".bmp"
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
                # tkinter.messagebox.showinfo("提示", notification)
                print(notification)
                break

    def clean_pic(self):
        self.primitives = []
        self.refresh()


    def save_canvas(self):
        # file_name = "temp.bmp"
        self.image.save(self.save_name)

    def refresh(self):
        # t1 = int(round(time.time() * 1000))
        # self.image.show()
        # print("refresh!")
        self.image = Image.new("RGB", (self.size_x, self.size_y), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        i = 0
        for primitive in self.primitives:
            pixels = primitive.get_pixels()
            for point in pixels:
                if (point[0] >= 0) and (point[1] >= 0) and (point[0] <= self.size_x-1) and (point[1] <= self.size_y-1):
                    # self.draw.point((point[0], point[1]), fill=self.color_r + self.color_g*256 + self.color_b*256*256)
                    self.draw.point((point[0], point[1]), fill=primitive.get_color())
            i = i + 1

if __name__ == '__main__':
    print("input file: " + sys.argv[1] + "\noutput path: " +sys.argv[2])
    cli = CLI(sys.argv[1], sys.argv[2])

