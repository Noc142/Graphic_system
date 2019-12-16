from base import*
from line import*

class Polygon(Primitive):
    def __init__(self, vertex, pno, method, is_done, color):  # is_done:命令行直接完成，图形界面要等待完成
        super().__init__(vertex, pno, color)
        self.method = method
        self.is_done = is_done
        self.lines = []
        self.last_point = vertex[0]
        self.is_updating = 0
        self.new_point = [0, 0]
        if is_done:
            # 直接光栅化完成
            self.rasterization()
            # for i in range(1, len(vertex)):
            #    print(i)
            #    self.update_rasterization(vertex[i])
            #    self.last_point = vertex[i]
            # self.done()
        # 第一个点就在vertex[0]里面

    def rasterization(self):
        self.pixels = []
        self.lines = []
        self.last_point = self.vertex[0]
        for i in range(1, len(self.vertex)):
            # print(i)
            self.update_rasterization_done(self.vertex[i])
            self.last_point = self.vertex[i]
        self.done()

    def update_rasterization(self, point):
        tmp_line = Line([self.last_point, point], 0, self.method, self.color)
        self.vertex.append(point)
        self.last_point = point
        self.pixels.extend(tmp_line.rasterization())
        self.is_updating = 0

    def update_rasterization_done(self, point):
        tmp_line = Line([self.last_point, point], 0, self.method, self.color)
        # self.vertex.append(point)
        self.last_point = point
        self.pixels.extend(tmp_line.rasterization())
        self.is_updating = 0

    def done(self):
        tmp_line = Line([self.last_point, self.vertex[0]], 0, self.method, self.color)
        tmp_pix = tmp_line.get_pixels()
        self.pixels.extend(tmp_pix)

    def get_pixels(self):
        if self.is_updating == 1:
            res = self.pixels
            tmp_line = Line([self.last_point, self.new_point], 0, self.method, self.color)
            tmp_pix = tmp_line.get_pixels()
            return res + tmp_pix
        else:
            return self.pixels

    def updating(self, point):
        self.new_point = point
        self.is_updating = 1

