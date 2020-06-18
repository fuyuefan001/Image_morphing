import os

import imageio
import matplotlib
import numpy as np
import scipy
from scipy.spatial import Delaunay
import scipy.interpolate
import matplotlib.pyplot as plt


from PIL import Image
import threading
import time
def loadTriangles(leftPointFilePath, rightPointFilePath):
    list1=[]
    list2=[]
    pointL = np.loadtxt(leftPointFilePath,dtype=np.float64)
    pointR = np.loadtxt(rightPointFilePath, dtype=np.float64)
    indexs = Delaunay(np.array(pointL)).simplices
    for i in indexs:
        list1.append(Triangle(pointL[i]))
        list2.append(Triangle(pointR[i]))
    return(list1,list2)


class Triangle():
    vertices=None
    def __init__(self,vt):
        for i in vt:
            for j in i:
                if type(j) != np.float64:
                    raise ValueError
        if len(vt)==3 and len(vt[0])==2:
            self.vertices=vt
        else:
            raise ValueError
    def isInside(self,point):
        vct1=self.vertices[1]-self.vertices[0]
        vct2 = self.vertices[2] - self.vertices[0]
        vctpoint=point-self.vertices[0]
        coef=(np.linalg.inv(np.array([vct1,vct2])))
        ab=coef * vctpoint
        a=ab[0][0]
        b=ab[1][1]
        if a>=0 and b>=0 and a+b<=1:
            return True
        else:
            return False

    def getPoints(self):
        indexlist=[]
        vt = self.vertices
        minx=min(vt[0][0],vt[1][0],vt[2][0])
        miny = min(vt[0][1], vt[1][1], vt[2][1])
        maxx=max(vt[0][0],vt[1][0],vt[2][0])
        maxy = max(vt[0][1], vt[1][1], vt[2][1])

        for x in range(int(minx),int(maxx)+1):
            for y in range(int(miny), int(maxy)+1):
                index=[x,y]
                indexlist.append(index)
        indexlist = np.array(indexlist, dtype=np.float64)
        point = matplotlib.path.Path(self.vertices)
        pt = point.contains_points(indexlist)
        res = indexlist[pt]
        return res



class Morpher:
    leftImage=None
    rightImage=None
    leftTriangles=None
    rightTriangles = None
    def __init__(self,li,lt,ri,rt):
        for i in lt:
            if not isinstance(i, Triangle):
                raise TypeError
        for j in rt:
            if not isinstance(j, Triangle):
                raise TypeError
        if not isinstance(li, np.ndarray):
            raise TypeError
        if not  isinstance(ri, np.ndarray):
            raise TypeError
        self.leftImage=li
        self.leftTriangles=lt
        self.rightImage=ri
        self.rightTriangles=rt


    def getImageAtAlpha(self,alpha):
        li=self.leftImage
        ri=self.rightImage
        shp=self.leftImage.shape

        shp=[shp[0],shp[1]]
        res = np.zeros(self.leftImage.shape)
        for i in range (0,len(self.leftTriangles)):
            vtmid=(1-alpha)* (self.leftTriangles[i].vertices) + alpha* (self.rightTriangles[i].vertices)

            midtri = Triangle(vtmid)

            vt1=self.leftTriangles[i].vertices
            vt2=self.rightTriangles[i].vertices
            h_mid2left=getH(vt1,vtmid)
            h_mid2right=getH(vt2,vtmid)
            midpoints=midtri.getPoints()
            midpoints= np.insert(midpoints, 2, 1, axis=1).T
            # print(len(midpoints[0]))
            indexleft=(h_mid2left).dot(midpoints).astype(int)
            indexright =(h_mid2right).dot(midpoints).astype(int)
            midpoints=midpoints.astype(int)
            for i in range(0,len(midpoints[0])):
                leftval = li[indexleft[1][i]][indexleft[0][i]]
                rightval = ri[indexright[1][i]][indexright[0][i]]
                color=np.array( (alpha*rightval + (1-alpha)*leftval).astype(int))
                res[midpoints[1][i]][midpoints[0][i]]=color
        return res.astype(np.uint8)

    def saveVideo(self,targetFilePath,frameCount,frameRate,includeReversed):
        writer=imageio.get_writer(targetFilePath,fps=frameRate)
        for i in range(0,frameCount):
            temp=self.getImageAtAlpha(i/(frameCount))
            writer.append_data(temp)
            print(i)
        if includeReversed==True:
            for i in range(0, frameCount):
                temp = self.getImageAtAlpha((frameCount-i) / (frameCount))
                writer.append_data(temp)
                print(i)
        writer.close()

class ColorMorpher(Morpher):
    def __init__(self,li,lt,ri,rt):
        for i in lt:
            if not isinstance(i, Triangle):
                raise TypeError
        for j in rt:
            if not isinstance(j, Triangle):
                raise TypeError
        if not isinstance(li, np.ndarray):
            raise TypeError
        if not  isinstance(ri, np.ndarray):
            raise TypeError
        self.leftImage=li
        self.leftTriangles=lt
        self.rightImage=ri
        self.rightTriangles=rt


    def getImageAtAlpha(self,alpha):
        li=self.leftImage
        ri=self.rightImage
        shp=self.leftImage.shape

        shp=[shp[0],shp[1]]
        res = np.zeros(self.leftImage.shape)
        for i in range (0,len(self.leftTriangles)):
            vtmid=(1-alpha)* (self.leftTriangles[i].vertices) + alpha* (self.rightTriangles[i].vertices)

            midtri = Triangle(vtmid)

            vt1=self.leftTriangles[i].vertices
            vt2=self.rightTriangles[i].vertices
            h_mid2left=getH(vt1,vtmid)
            h_mid2right=getH(vt2,vtmid)
            midpoints=midtri.getPoints()
            midpoints= np.insert(midpoints, 2, 1, axis=1).T
            # print(len(midpoints[0]))
            indexleft=(h_mid2left).dot(midpoints).astype(int)
            indexright =(h_mid2right).dot(midpoints).astype(int)
            midpoints=midpoints.astype(int)
            # print(len(midpoints[0]))
            # print()
            for i in range(0,len(midpoints[0])):
                # print(indexleft[1][i])
                # print(indexleft[0][i])
                leftval = li[indexleft[1][i]][indexleft[0][i]]
                rightval = ri[indexright[1][i]][indexright[0][i]]
                color=np.array( (alpha*rightval + (1-alpha)*leftval).astype(int))
                res[midpoints[1][i]][midpoints[0][i]]=color
        return res.astype(np.uint8)


def getH(vt1,vtmid):
    matleft6x6 = [[vt1[0][0], vt1[0][1], 1, 0, 0, 0],
                  [0, 0, 0, vt1[0][0], vt1[0][1], 1],
                  [vt1[1][0], vt1[1][1], 1, 0, 0, 0],
                  [0, 0, 0, vt1[1][0], vt1[1][1], 1],
                  [vt1[2][0], vt1[2][1], 1, 0, 0, 0],
                  [0, 0, 0, vt1[2][0], vt1[2][1], 1]]
    matmid = [[vtmid[0][0]], [vtmid[0][1]], [vtmid[1][0]], [vtmid[1][1]], [vtmid[2][0]], [vtmid[2][1]]]
    hleft2mid = np.linalg.solve(matleft6x6, matmid)
    h_left_mat = np.array([[hleft2mid[0][0], hleft2mid[1][0], hleft2mid[2][0]],
                           [hleft2mid[3][0], hleft2mid[4][0], hleft2mid[5][0]],
                           [0, 0, 1]])
    # print(h_left_mat)
    h_mid2left = np.linalg.inv(h_left_mat)
    # print(h_mid2left)
    return h_mid2left


if __name__=='__main__':
    t1=time.time()
    out=loadTriangles('TestData/LeftColor.orig.txt','TestData/RightColor.orig.txt')
    tris = out[0]
    tri=out[0][100]
    tri2=out[1][100]
    leftImage = imageio.imread('TestData/LeftColor.png')
    rightImage = imageio.imread('TestData/RightColor.png')
    out = loadTriangles('TestData/LeftColor.orig.txt','TestData/RightColor.orig.txt')
    morpher = ColorMorpher(leftImage, out[0], rightImage, out[1])
    #morpher = ColorMorpher(leftImage, leftTriangles, rightImage, rightTriangles)
    imageio.imsave('alpha50.png',morpher.getImageAtAlpha(0.75))
    # morpher.saveVideo('xxx.mp4', 10, 5, True)
    t2=time.time()
    print(t2-t1)
