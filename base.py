import math
from tkinter import *
import tkinter.messagebox
from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk
import os
from PIL import ImageGrab
# from pyscreenshot import grab
# import time
import tkinter.filedialog as tkfl
from tkinter import colorchooser
import numpy as np

import imgs
import base64

class Primitive:
    def __init__(self, vertex, pno, color):
        # self.vertex = vertex
        self.vertex = [[int(p[0]), int(p[1])] for p in vertex]
        self.pixels = []
        self.pno = pno
        self.color = color
        self.is_deleted = 0
        self.is_changed = 0
        self.vertex_float = []

    def rasterization(self):
        # self.pixels = []
        return self.pixels

    def get_pixels(self):
        if self.is_deleted == 1:
            res = []
            return res
        # print(self.pixels.__len__())
        if self.pixels.__len__() == 0:  # __len__() 要括号！
            self.rasterization()
            # print("here")
        return self.pixels

    def get_id(self):
        return self.pno

    def get_color(self):
        return self.color[0] + self.color[1]*256 + self.color[2]*256*256

    def translate(self, x, y):  # for line, polygon, curve
        self.vertex = [[p[0] + x, p[1] + y] for p in self.vertex]
        self.rasterization()

    def rotate(self, x0, y0, r):
        # self.vertex = [[p[0], p[1]] for p in self.vertex]
        if self.is_changed:
            for i in range(len(self.vertex_float)):
                x1 = self.vertex_float[i][0]
                y1 = self.vertex_float[i][1]
                self.vertex_float[i][0] = x0 + (x1 - x0) * math.cos(r/180*math.pi) - (y1 - y0) * math.sin(r/180*math.pi)
                self.vertex_float[i][1] = y0 + (x1 - x0) * math.sin(r/180*math.pi) + (y1 - y0) * math.cos(r/180*math.pi)
            # print(self.vertex)
            # print("rotate ", r/180*math.pi)
            self.vertex = [[int(p[0]), int(p[1])] for p in self.vertex_float]
        else:
            for i in range(len(self.vertex)):
                x1 = self.vertex[i][0]
                y1 = self.vertex[i][1]
                self.vertex[i][0] = int(x0 + (x1 - x0) * math.cos(r/180*math.pi) - (y1 - y0) * math.sin(r/180*math.pi))
                self.vertex[i][1] = int(y0 + (x1 - x0) * math.sin(r/180*math.pi) + (y1 - y0) * math.cos(r/180*math.pi))
        self.rasterization()

    def scale(self, x0, y0, s):
        if self.is_changed:
            for i in range(len(self.vertex_float)):
                x1 = self.vertex_float[i][0]
                y1 = self.vertex_float[i][1]
                self.vertex_float[i][0] = int((x1 - x0)*s + x0)
                self.vertex_float[i][1] = int((y1 - y0)*s + y0)
                self.vertex = [[int(p[0]), int(p[1])] for p in self.vertex_float]
        else:
            for i in range(len(self.vertex)):
                x1 = self.vertex[i][0]
                y1 = self.vertex[i][1]
                self.vertex[i][0] = int((x1 - x0)*s + x0)
                self.vertex[i][1] = int((y1 - y0)*s + y0)
        self.rasterization()

    def clip(self, x1, y1, x2, y2, alg):
        # print('a')
        print('Primitive {} is not line. You can\'t clip it'.format(self.pno))

    # def updating(self, point):
        # return 0

    # def update_rasterization(self, point):
        # return 0

    def change(self, i):  # 修改过之后的
        self.is_changed = i
        self.vertex_float = self.vertex
        if i == 0:
            self.vertex_float = []