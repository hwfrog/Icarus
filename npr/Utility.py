import numpy as np
import operator
from skimage import io
from skimage.color import rgb2hsv,hsv2rgb
def com(n,k):
    #return the combination number
    if k!=0:
         return  reduce(operator.mul, range(n - k + 1, n + 1)) /reduce(operator.mul, range(1, k +1))
    else:
        return 1

def rgb2gray(im):
    #im is the a rgb image matrix
    #return the corresponding matrix in the greyscale
    height=im.shape[0]
    width=im.shape[1]
    gray=np.ndarray(shape=(height,width), dtype=float)
    for row in range(height):
        for col in range(width):
            r,g,b=im[row][col]
            gray[row][col]=0.299*r + 0.587*g + 0.114*b
    return gray


def neighbour(row,col,height,width):
    #row,col is the coordinate of the pixel, while height,width is the dimension of the image
    #return the coordinates of the neighboring pixels
    neighbour=[(i,j) for i in range(row-1,row+2) for j in range(col-1,col+2)]
    neighbour=filter(lambda x:x[0]>=0 and x[0]<height and x[1]>=0 and x[1]<width, neighbour)
    neighbour.remove((row,col))
    return neighbour

def merge(c1,c2,a1,a2):
    c=c1*a1+c2*a2*(1-a1)
    a=a1+a2*(1-a1)
    return c/a

class Neighbourscanner:
    direction=[(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    def __init__(self):
        self.mode=True#true for clockwise, false for unclockwise

    def neighbour(self,row,col,tag):
        result=[]
        if(self.mode):
            for i,dir in enumerate(self.direction):
                nb=np.array((row,col))+np.array(self.direction[i])
                if(tag(nb)):
                   #if(i>=4): self.mode=False
                   no=[(i+x)%8 for x in range(2)]
                   no=map(int,no)
                   result=[np.array(self.direction[noo])+np.array([row,col]) for noo in no]
                   result=[(x[0],x[1]) for x in result]
            return  result
        else:
            for i,dir in enumerate(self.direction[7::-1]):
                nb=np.array((row,col))+np.array(dir)
                if(tag(nb)):
                   if(i>3): self.mode=True
                   no=(7-i+np.arange(0,-4,-1))%8
                   no=map(int,no)
                   result=[np.array(self.direction[noo])+np.array([row,col]) for noo in no]
                   result=[(x[0],x[1]) for x in result]
                   return  result

if __name__=='__main__':
    img=np.ndarray(shape=(400,600,3))
    c1=np.array((1.0,0.0,0.0))
    c2=np.array((0.0,1.0,0.0))
    a1=0.9
    a2=0.9
    print merge(c1,c2,a1,a2)
    for i in range(400):
        for j in range(600):
            if(j<200):
                img[i][j]=c1*a1
            elif(j<400):
                img[i][j]=merge(c2,c1,a2,a1)
            else:
                img[i][j]=c2*a2
    io.imshow(img)
    io.show()