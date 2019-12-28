from base import*

class Circle(Primitive):  # 其实应该是椭圆
    def __init__(self, vertex, pno, color):
        super().__init__(vertex, pno, color)  # vertex第一个点是圆心 第二个点的第一个元素是x半轴，第二个元素是y半轴
        self.rx = vertex[1][0]
        self.ry = vertex[1][1]

    def rasterization(self):
        # if self.pixels.__len__() != 0:  # 若已经光栅化过， 直接返回
            # return self.pixels
        # splt_x = int(math.sqrt(self.ry/(2*self.rx)+self.ry))  # 分割点横坐标
        # splt_y = int(math.sqrt(self.rx/(2*self.ry)+self.rx))  # 分割点纵坐标
        # 不用上面这么麻烦的
        self.rx = self.vertex[1][0]
        self.ry = self.vertex[1][1]
        if self.vertex[1][0] == 0 or self.vertex[1][1] == 0:
            return self.pixels
        self.pixels = []
        # print(self.vertex)
        rx = self.rx
        ry = self.ry
        # 区域1
        self.pixels.append([0, ry])
        x = 0
        y = ry
        p1k = ry * ry - rx * rx * ry + rx * rx /4   # P one K  not PLK
        while 2 * ry * ry * x <= 2 * rx * rx * y:
            if p1k < 0:
                p1k = p1k + 2 * ry * ry * x + 3 * ry * ry
                x = x + 1
            else:
                p1k = p1k + 2 * ry * ry * x + 3 * ry * ry - 2 * rx * rx * y + 2 * rx * rx
                x = x + 1
                y = y - 1
            self.pixels.append([x, y])
            # print([x, y])
        p2k = ry*ry*(x+0.5)*(x+0.5) + rx*rx*(y-1)*(y-1) - rx*rx*ry*ry
        while y >= 0:
            if p2k <= 0:
                # p2k = p2k - 2*rx*rx*y + 3*rx*rx
                p2k = p2k + 2*ry*ry*x + 2*ry*ry - 2*rx*rx*y + 3*rx*rx
                y = y - 1
                x = x + 1
            else:
                # p2k = p2k + 2*ry*ry*x - 2*rx*rx*y + 2*ry*ry + 3*rx*rx
                p2k = p2k - 2*rx*rx*y + 3*rx*rx
                y = y - 1
            self.pixels.append([x, y])
        # print("end?")
        len_1 = self.pixels.__len__()
        for i in range(len_1):  # y对称
            temp = [-self.pixels[i][0], self.pixels[i][1]]
            # temp.append(-self.pixels[i][0])
            # temp.append(self.pixels[i][1])
            # temp[0] = -temp[0]
            if temp[0] != 0:
                self.pixels.append(temp)

        len_2 = self.pixels.__len__()
        for i in range(len_2):  # x对称
            # temp = self.pixels[i]
            # temp[1] = -temp[1]
            temp = [self.pixels[i][0], -self.pixels[i][1]]
            if temp[1] != 0:
                self.pixels.append(temp)

        len_3 = self.pixels.__len__()
        for i in range(len_3):  # 平移
            self.pixels[i][0] += self.vertex[0][0]
            self.pixels[i][1] += self.vertex[0][1]
        return self.pixels

    def translate(self, x, y):
        self.vertex[0] = [self.vertex[0][0] + x, self.vertex[0][1] + y]
        self.rasterization()

    def rotate(self, x0, y0, r):
        if self.rx == self.ry or r % 90 == 0:
            super().rotate(x0, y0, r)
        else:  # 直接旋转像素
            for i in range(len(self.pixels)):
                x1 = self.pixels[i][0]
                y1 = self.pixels[i][1]
                self.pixels[i][0] = int(
                    x0 + (x1 - x0) * math.cos(r / 180 * math.pi) - (y1 - y0) * math.sin(r / 180 * math.pi))
                self.pixels[i][1] = int(
                    y0 + (x1 - x0) * math.sin(r / 180 * math.pi) + (y1 - y0) * math.cos(r / 180 * math.pi))
            # print(self.vertex)

    def scale(self, x0, y0, s):
        if self.rx == self.ry:
            self.rx = int(s * self.rx)
            self.ry = int(s * self.ry)
            x1 = self.vertex[0][0]
            y1 = self.vertex[0][1]
            self.vertex[0][0] = int((x1 - x0) * s + x0)
            self.vertex[0][1] = int((y1 - y0) * s + y0)
            self.vertex[1] = [self.rx, self.ry]
            self.rasterization()
        else:
            # points = [[self.vertex[0][0] - self.rx, self.vertex[0][1] - self.ry],
            #           [self.vertex[0][0] + self.rx, self.vertex[0][1] + self.ry]]
            # for i in range(len(points)):
            #     x1 = points[i][0]
            #     y1 = points[i][1]
            #     points[i][0] = int((x1 - x0) * s + x0)
            #     points[i][1] = int((y1 - y0) * s + y0)
            # self.vertex[0][0] = int((points[0][0] + points[1][0])/2)
            # self.vertex[0][1] = int((points[0][1] + points[1][1])/2)
            # self.vertex[1][0] = abs(int((points[0][0] - points[1][0])/2))
            # self.vertex[1][1] = abs(int((points[0][1] - points[1][1])/2))
            # self.rx = self.vertex[1][0]
            # self.ry = self.vertex[1][1]
            self.vertex[1] = [int(p*s) for p in self.vertex[1]]
            x1 = self.vertex[0][0]
            y1 = self.vertex[0][1]
            self.vertex[0][0] = int((x1 - x0) * s + x0)
            self.vertex[0][1] = int((y1 - y0) * s + y0)
            self.rasterization()




