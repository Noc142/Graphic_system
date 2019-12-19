from base import*
from line import*

class Curve(Primitive):
    def __init__(self, vertex, pno, alg, is_done, color):
        super().__init__(vertex, pno, color)
        self.alg = alg

    def rasterization(self):
        self.pixels = []
        if len(self.vertex) == 2:
            tmp_vertex = [[int(self.vertex[0][0]), int(self.vertex[0][1])],
                          [int(self.vertex[1][0]), int(self.vertex[1][1])]]
            temp = Line(tmp_vertex, 1, 1, 1)
            self.pixels = temp.get_pixels()
            # return temp.get_pixels()
            return
        if self.alg == 'Bezier':
            self.Bezier()
        elif self.alg == 'B-spline':
            self.Bspline()

    def Bezier(self):
        # print('Bezier')
        p = np.zeros((len(self.vertex), len(self.vertex), 2), dtype=np.float)
        for i in range(len(self.vertex)):
            p[i][0] = self.vertex[i]
        for i in range(len(self.vertex)-1, -1, -1):
            for j in range(1, len(self.vertex)-i):
                p[i][j][0] = 0.5 * p[i][j - 1][0] + 0.5 * p[i + 1][j - 1][0]
                p[i][j][1] = 0.5 * p[i][j - 1][1] + 0.5 * p[i + 1][j - 1][1]
        # print(p)
        q_vertex = p[0]
        r_vertex = [p[i][len(self.vertex)-i-1] for i in range(len(self.vertex))]
        if max([self.distance(point, [q_vertex[0], q_vertex[len(self.vertex)-1]]) for point in q_vertex]) <= 1:
            # print(int(q_vertex[0][0]))
            vertex = [[int(q_vertex[0][0]), int(q_vertex[0][1])],
                      [int(q_vertex[len(self.vertex)-1][0]), int(q_vertex[len(self.vertex)-1][1])]]
            temp = Line(vertex, 1, 1, 1)
            self.pixels.extend(temp.get_pixels())
        else:
            temp = Curve(q_vertex, 1, 'Bezier', 1, 1)
            self.pixels.extend(temp.get_pixels())
        if max([self.distance(point, [r_vertex[0], r_vertex[len(self.vertex)-1]]) for point in r_vertex]) <= 1:
            vertex = [[int(r_vertex[0][0]), int(r_vertex[0][1])],
                      [int(r_vertex[len(self.vertex) - 1][0]), int(r_vertex[len(self.vertex) - 1][1])]]
            temp = Line(vertex, 1, 1, 1)
            self.pixels.extend(temp.get_pixels())
        else:
            temp = Curve(r_vertex, 1, 'Bezier', 1, 1)
            self.pixels.extend(temp.get_pixels())

    @staticmethod
    def distance(p, l):
        if l[0][0]==l[1][0] and l[0][1]==l[1][1]:
            return math.sqrt((p[0]-l[0][0])*(p[0]-l[0][0]) + (p[1]-l[0][1])*(p[1]-l[0][1]))
        a = l[1][1] - l[0][1]
        b = l[0][0] - l[1][0]
        c = (l[1][0] - l[0][0])*l[0][1] - (l[1][1] - l[0][1])*l[0][0]
        return abs((a*p[0] + b*p[1] + c)/math.sqrt(a*a + b*b))

    def Bspline(self):
        # print('B-spline')
        # # 三次（四阶）均匀B样条
        # k = 4
        # if k >= len(self.vertex):
        #     k = len(self.vertex)
        # def p_matrix(u):
        #     p = np.zeros((len(self.vertex), k, 2), dtype=np.float)
        #     for i in range(len(self.vertex)):
        #         for r in range(k):
        #             if r == 0:
        #                 p[i][r] = self.vertex[i]
        #             else:
        #                 p[i][r][0] = ((u - i) / (k - r)) * p[i][r - 1][0] + (1 - (u - i) / (k - r)) * p[i - 1][r - 1][0]
        #                 p[i][r][1] = ((u - i) / (k - r)) * p[i][r - 1][1] + (1 - (u - i) / (k - r)) * p[i - 1][r - 1][1]
        #     return p
        # u_t = k-1
        # last_point = self.vertex[0]
        # while(u_t <= len(self.vertex)):
        #     p = p_matrix(u_t)
        #     j = int(u_t)
        #     point = p[j][k-1]
        #     tmp_line = Line([last_point, point], 0, 1, 1)
        #     self.pixels.extend(tmp_line.get_pixels())
        #     last_point = point
        #     u_t += 0.1
        k = 4
        u_t = k-1
        last_point = [-1, -1]
        # print(u_t)
        while (u_t < len(self.vertex)):
            j = int(u_t)
            U = np.array([pow(u_t-j, 3), pow(u_t-j, 2), u_t-j, 1])
            A = np.array([[-1, 3, -3, 1],
                          [3, -6, 3, 0],
                          [-3, 0, 3, 0],
                          [1, 4, 1, 0]])
            px = np.array([[self.vertex[j-k+1][0]], [self.vertex[j-k+2][0]], [self.vertex[j-k+3][0]],
                           [self.vertex[j-k+4][0]]])
            py = np.array([[self.vertex[j-k+1][1]], [self.vertex[j-k+2][1]], [self.vertex[j-k+3][1]],
                           [self.vertex[j-k+4][1]]])

            point = [np.matmul(np.matmul(U, A), px)/6, np.matmul(np.matmul(U, A), py)/6]
            # print(point)
            if last_point != [-1, -1]:
                tmp_line = Line([last_point, point], 0, 1, 1)
                self.pixels.extend(tmp_line.get_pixels())
            else:
                self.pixels.append([int(point[0]), int(point[1])])
            last_point = point
            u_t += 0.1
        # print(u_t)




    def updating(self, point):
        self.vertex[len(self.vertex)-1] = point
        self.rasterization()

    def begin_update(self, point):
        self.vertex.append(point)
        self.rasterization()

if __name__ == '__main__':
    a = [[5, 5], [5, 10], [10, 20], [30, 10]]
    c = Curve(a, 1, 'B-spline', 255, 1)
    c.get_pixels()
