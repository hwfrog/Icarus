#-*- coding:utf-8 -*-
import numpy as np
from Segmentation import *
from Rendering_Layers import *
from transformation import *
from Render_segment_layers import *
from Canvas import *
import math

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


class painter:
    def __init__(self,Seg=None,Canvas=None):
        self.Segmentation = Seg
        self.Subsegs = []
        self.layers = None
        self.Canvas =  Canvas
        
              

    def set_Segmentation(self, segs):
        self.Segmentation = segs

    def set_Subsegs(self):
        for s in self.Segmentation.objects:
            for b in s.subsegment:
                bb=[b]
                self.Subsegs.extend(bb)

    def assigncolor(self):
        self.layers=Layers()
        self.layers.set_segs(self.Subsegs)
        self.layers.rendering()

    def set_canvas(self,canvas):
        self.Canvas = canvas

    def set_canvascolor(self):
        for color in self.layers.pc:
            self.Canvas.set_palettecolor(color)

    def hsv(self):
        for seg in self.Subsegs:
            for key in seg.pix:
                h,s,v=rgb2hsv(seg.pix[key][0],seg.pix[key][1],seg.pix[key][2])
                seg.pix[key]=[h,s,v]

    def paint(self):
        self.set_Subsegs()
        self.hsv()
        self.assigncolor()
        self.set_canvascolor()
        
        for seg in self.layers.segs:
            slayer=Seg_layer(seg.edge,seg.pix,self.Canvas)
            slayer.render()
        

if __name__ == '__main__':
    sg=Segmentation()
    sg.imread('input.jpg')
    #sg.set_no(1)
    sg.segment()
    canvas=Canvas()
    canvas.set_canvas(600,400)
    canvas.set_paper('paper.jpg')
    pt=painter(sg,canvas)
    pt.paint()























        
        

    
