from base import*

class Line(Primitive):
    def __init__(self, vertex, pno, method, color):
        super().__init__(vertex, pno, color)
        self.vertical = 0  # 是否存在斜率
        self.slope = 0
        self.method = method
        # print("slope:", self.slope)

    def rasterization(self):  # method: 1 for DDA, 2 for Bresenham
        # if self.pixels.__len__() != 0:  # 若已经光栅化过， 直接返回
            # print(self.pixels.__len__())
            # return self.pixels
        # print("rasterization")
        if self.vertex.__len__() == 1:
            self.vertex.append(self.vertex[0])
        self.slope = 10000
        self.vertical = 0
        # print(self.vertex)
        # print(self.vertex)
        if self.vertex[1][0] == self.vertex[0][0]:
            self.vertical = 1  # 垂直 不存在斜率
            # print("vertical!")
        if self.vertical == 0:
            self.slope = (self.vertex[1][1]-self.vertex[0][1])/(self.vertex[1][0]-self.vertex[0][0])
        self.pixels = []
        x = 0
        y = 1
        tmp_slope = self.slope

        if abs(self.slope) >= 1:  # 斜率绝对值大于1， x y互换
            x = 1
            y = 0
            if tmp_slope != 0:
                tmp_slope = 1 / tmp_slope
                # print("changed")
        if (self.vertex[0][x] == self.vertex[1][x]) or (self.vertex[0][y] == self.vertex[1][y]):
            # 水平或垂直,此时就不需要DDA或Bresenham了
            # print("No!")
            # print(x)
            return self.ver_or_hor(x, y)
        if self.vertex[0][x] > self.vertex[1][x]:  # 第一个点是"横坐标"较小的
            temp = self.vertex[0]
            self.vertex[0] = self.vertex[1]
            self.vertex[1] = temp
        # print("vertex:", self.vertex)
        if self.method == 1:
            return self.DDA(x, y, tmp_slope)
        elif self.method == 2:
            return self.Bresenham(x, y)
            # print("Bresenham")

    def ver_or_hor(self, x, y):
        if self.vertex[0][x] > self.vertex[1][x]:  # 第一个点是"横坐标"较小的
            temp = self.vertex[0]
            self.vertex[0] = self.vertex[1]
            self.vertex[1] = temp
        for i in range(self.vertex[0][x], self.vertex[1][x] + 1):
            point = [0, 0]
            point[y] = self.vertex[0][y]
            point[x] = i
            # print(point)
            self.pixels.append(point)
        return self.pixels

    def DDA(self, x, y, tmp_slope):
        point = [self.vertex[0][0], self.vertex[0][1]]
        self.pixels.append(point)
        yk = self.vertex[0][y]
        for i in range(self.vertex[0][x] + 1, self.vertex[1][x] + 1):
            point = [0, 0]
            point[x] = i
            yk = yk + tmp_slope
            # yk = (math.ceil(yk1) if math.ceil(yk1)-yk1 <= yk1-int(yk1) else int(yk1))
            point[y] = (math.ceil(yk) if math.ceil(yk) - yk < yk - int(yk) else int(yk))
            self.pixels.append(point)
            # print("inserted", point, "pixels is", self.pixels)
        # print("DDA")
        # print(tmp_slope, self.vertex)
        return self.pixels

    def Bresenham(self, x, y):
        point = [self.vertex[0][0], self.vertex[0][1]]
        self.pixels.append(point)
        # print(self.pixels)
        deltax = self.vertex[1][x] - self.vertex[0][x]
        deltay = self.vertex[1][y] - self.vertex[0][y]
        assert deltax >= 0, "delta x < 0"
        pk = 2 * deltay - deltax
        y_negative = 0
        if deltay < 0:  # 如果delta y 小于0， 则整体要向下, pk也要修改
            y_negative = 1
            pk += 2 * deltax
        xk = self.vertex[0][x]
        yk = self.vertex[0][y]
        for k in range(deltax):
            point_a = [0, 0]
            if pk < 0:
                # point = [self.vertex[k+1][x], yk]
                point_a[x] = xk + 1  # self.vertex[k + 1][x]
                point_a[y] = yk - y_negative
                yk = yk - y_negative
                pk = pk + 2 * deltay
            else:
                # point = [self.vertex[k+1][x], yk+1]
                point_a[x] = xk + 1  # self.vertex[k + 1][x]
                point_a[y] = yk + 1 - y_negative
                yk = yk + 1 - y_negative
                pk = pk + 2 * deltay - 2 * deltax
            if y_negative == 1:
                pk = pk + 2 * deltax
            xk = xk + 1
            self.pixels.append(point_a)
            # print("inserted", point_a, "pixels is", self.pixels)  # ???why????
        # print("Bresenham")
        return self.pixels

    def clip(self, x1, y1, x2, y2, alg):
        # print('clip line')
        if alg == 'Cohen-Sutherland':
            code = self.encode(x1, y1, x2, y2)
            if code[0]==0 and code[1] == 0:
                return  # 啥也不做
            elif code[0]&code[1] != 0:
                self.is_deleted = 1
            else:
                if code[1]==0:
                    code[1] = code[0]
                    code[0] = 0
                    temp = self.vertex[0]
                    self.vertex[0] = self.vertex[1]
                    self.vertex[1] = temp
                if code[0]==0:
                    cross_points = [self.vertex[0]]
                    res = []
                    if code[1]&8==8:
                        # print("x min")
                        res.extend(self.node(x1, y1, x2, y2, 1))
                    elif code[1]&4==4:
                        # print("x max")
                        res.extend(self.node(x1, y1, x2, y2, 2))
                    if code[1]&2==2:
                        # print("y min")
                        res.extend(self.node(x1, y1, x2, y2, 3))
                    elif code[1]&1==1:
                        # print("y max")
                        res.extend(self.node(x1, y1, x2, y2, 4))
                    if len(res) != 0:
                        cross_points.append(res)
                    self.vertex = cross_points
                    self.rasterization()
                else:
                    cross_points = []
                    cross = code[0] | code[1]
                    res = []
                    if cross & 8 == 8:
                        # print("x min")
                        res = self.node(x1, y1, x2, y2, 1)
                        if len(res) != 0:
                            cross_points.append(res)
                    if cross & 4 == 4:
                        # print("x max")
                        res = self.node(x1, y1, x2, y2, 2)
                        if len(res) != 0:
                            cross_points.append(res)
                    if cross & 2 == 2:
                        # print("y min")
                        res = self.node(x1, y1, x2, y2, 3)
                        if len(res) != 0 and res not in cross_points:
                            cross_points.append(res)
                    if cross & 1 == 1:
                        # print("y max")
                        res = self.node(x1, y1, x2, y2, 4)
                        if len(res) != 0 and res not in cross_points:
                            cross_points.append(res)
                    if len(cross_points)==0:
                        self.is_deleted = 1
                    else:
                        self.vertex = cross_points
                        self.rasterization()
        elif alg == 'Liang-Barsky':
            print('Liang-Barsky')
            u1 = 0
            u2 = 1
            xmax = max(x1, x2)
            xmin = min(x1, x2)
            ymax = max(y1, y2)
            ymin = min(y1, y2)
            p = [0, 0, 0, 0]
            q = [0, 0, 0, 0]
            p[0] = -self.vertex[1][0] + self.vertex[0][0]
            p[1] = -p[0]
            p[2] = -self.vertex[1][1] + self.vertex[0][1]
            p[3] = -p[2]
            q[0] = self.vertex[0][0] - xmin
            q[1] = xmax - self.vertex[0][0]
            q[2] = self.vertex[0][1] - ymin
            q[3] = ymax - self.vertex[0][1]
            r = 0.0
            flag = 0
            for i in range(4):
                if p[i]<0:
                    r = q[i] / p[i]
                    u1 = max(u1, r)
                    if u1 > u2:
                        flag = 1
                        break
                if p[i] > 0:
                    r = q[i] / p[i]
                    u2 = min(u2, r)
                    if u1 > u2:
                        flag = 1
                        break
                if p[i]==0 and q[i] < 0:
                    flag = 1
                    break
            if flag == 1:
                self.is_deleted = 1
                return
            else:
                point1_x = int(self.vertex[0][0] + u1*(self.vertex[1][0] - self.vertex[0][0]))
                point1_y = int(self.vertex[0][1] + u1 * (self.vertex[1][1] - self.vertex[0][1]))
                point2_x = int(self.vertex[0][0] + u2 * (self.vertex[1][0] - self.vertex[0][0]))
                point2_y = int(self.vertex[0][1] + u2 * (self.vertex[1][1] - self.vertex[0][1]))
                self.vertex = [[point1_x, point1_y], [point2_x, point2_y]]
                self.rasterization()

    def node(self, x1, y1, x2, y2, pos):
        xmax = max(x1, x2)
        xmin = min(x1, x2)
        ymax = max(y1, y2)
        ymin = min(y1, y2)
        x1 = self.vertex[0][0]
        x2 = self.vertex[1][0]
        y1 = self.vertex[0][1]
        y2 = self.vertex[1][1]
        res = [0, 0]
        if pos==1:  # xmin
            y = (y2-y1)/(x2-x1)*(xmin-x1) + y1
            y = int(y)
            res = [xmin, y]
        if pos == 2:  # xmax
            y = (y2 - y1) / (x2 - x1) * (xmax - x1) + y1
            y = int(y)
            res = [xmax, y]
        if pos==3:  # ymin
            x = (x2-x1)/(y2-y1)*(ymin-y1) + x1
            x = int(x)
            res = [x, ymin]
        if pos==4:  # ymax
            x = (x2-x1)/(y2-y1)*(ymax-y1) + x1
            x = int(x)
            res = [x, ymax]
        if (res[0]>=xmin) and (res[0]<=xmax) and (res[1]>=ymin) and (res[1]<=ymax):
            return res
        else:
            return []

    def encode(self, x1, y1, x2, y2):
        xmax = max(x1, x2)
        xmin = min(x1, x2)
        ymax = max(y1, y2)
        ymin = min(y1, y2)
        code = [0, 0]
        if self.vertex[0][0] < xmin:
            code[0] = code[0] | 8
        elif self.vertex[0][0] > xmax:
            code[0] = code[0] | 4
        if self.vertex[0][1] < ymin:
            code[0] = code[0] | 2
        elif self.vertex[0][1] > ymax:
            code[0] = code[0] | 1
        if self.vertex[1][0] < xmin:
            code[1] = code[1] | 8
        elif self.vertex[1][0] > xmax:
            code[1] = code[1] | 4
        if self.vertex[1][1] < ymin:
            code[1] = code[1] | 2
        elif self.vertex[1][1] > ymax:
            code[1] = code[1] | 1
        return code

    def get_method(self):
        return self.method






