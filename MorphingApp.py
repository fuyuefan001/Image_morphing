import sys
import os
from copy import deepcopy
from multiprocessing import Process,Pool
from PyQt5.QtCore import QSize, QTimer, Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, \
    QGraphicsSceneEvent, QGraphicsItem
from MorphingGUI import Ui_Dialog
from Morphing import *
from enum import Enum
import  PyQt5.QtGui
import imageio



class state(Enum):
    INIT=1
    LOADED=2



class MorphingApp(QMainWindow, Ui_Dialog):
    img1=None
    img2=None
    def __init__(self, parent=None):

        super(MorphingApp, self).__init__(parent)
        self.setupUi(self)
        self.slidervalue=0
        # self.loadimg1()
        self.load_start.clicked.connect(self.loadimg1)
        self.load_end.clicked.connect(self.loadimg2)
        self.alpha.setMaximum(100)
        self.alpha.setMinimum(0)
        self.alpha.setSingleStep(5)
        slidervalue=self.alpha.value()/100.0
        self.alpha_value.setText('%.2f'%slidervalue)
        self.alpha.valueChanged.connect(self.valChangeHandler)
        self.start_image.mousePressEvent=self.image1ClickHandler
        self.end_image.mousePressEvent=self.image2ClickHandler
        self.blending.clicked.connect(self.blendingBtnHandler)
        self.show_triangles.toggled.connect(self.checkboxChangeHandler)
        self.MarkLeft=1
        self.numPoints=0
        self.comfirmedLen=0
        self.fromfileLen=0
        self.leftPoints=[]
        self.rightPoints = []
        self.qp= QPainter()
        self.keyPressEvent=self.backspaceHandler
        self.leftPath=''
        self.rightPath=''
        self.allowbland=0
        self.itemArr=[]
        self.previndex=0
    def checkboxChangeHandler(self):
        try:
            self.draw1()
            self.draw2()
        except Exception as e:
            pass
    def mousePressEvent(self,event):
        if self.img1 == None or self.img2 == None:
            # self.leftPoints = []
            self.MarkLeft = 233
            return
        self.comfirmedLen=min(len(self.rightPoints),len(self.leftPoints))
        self.writePoints()
        try:
            self.draw1()
            self.draw2()
        except Exception as e:
            pass
    def image1ClickHandler(self,event):
        print('%d %d' % (self.fromfileLen, self.comfirmedLen))
        if os.path.exists(self.leftPath + '.png.txt') and os.path.exists(
                self.rightPath + '.png.txt') and self.img1 != None and self.img2 != None:
            self.allowbland = 1
        self.comfirmedLen = len(self.leftPoints)
        if self.MarkLeft==1:
            # save point info
            print('click detect1')
            print(event.localPos())
            print(self.img1)
            if self.img1==None or self.img2 ==None:
                self.leftPoints=[]
                self.MarkLeft = 233
                return
            self.leftPoints.append(event.localPos())
            self.MarkLeft=0
            self.writePoints()
            try:
                self.draw1()
                self.draw2()
            except Exception as e:
                pass

        else:
            pass

    def image2ClickHandler(self,event):
        print('%d %d' % (self.fromfileLen,self.comfirmedLen))
        if os.path.exists(self.leftPath + '.png.txt') and os.path.exists(
                self.rightPath + '.png.txt') and self.img1 != None and self.img2 != None:
            self.allowbland = 1
        self.comfirmedLen=max(len(self.rightPoints),len(self.leftPoints))-1
        if self.MarkLeft ==0:
            print('click detect2')
            print(event.localPos())
            if self.img1==None or self.img2 ==None:
                self.rightPoints=[]
                self.MarkLeft = 233
                return
            self.rightPoints.append(event.localPos())
            self.MarkLeft=1
            self.writePoints()
            try:
                self.draw1()
                self.draw2()
            except Exception as e:
                pass
        else:
            pass
    def backspaceHandler(self,event):
        if self.img1 == None or self.img2 == None:
            return
        print('%d %d'%(len(self.leftPoints),len(self.rightPoints)))
        if not event.key() ==Qt.Key_Backspace:
            return
        print('backspace pressed')
        if self.comfirmedLen==max(len(self.rightPoints),len(self.leftPoints)):
            return
        if len(self.leftPoints)==len(self.rightPoints):
            self.rightPoints=self.rightPoints[0:len(self.rightPoints)-1]
            self.draw2()
            self.MarkLeft=0
            return
        if len(self.leftPoints)>len(self.rightPoints):
            self.leftPoints=self.leftPoints[0:len(self.leftPoints)-1]
            self.draw1()
            self.MarkLeft = 1
            return
    def valChangeHandler(self):
        self.slidervalue=self.alpha.value()/100.0
        index=int(self.slidervalue/0.05)
        if index==self.previndex:
            return

        self.alpha_value.setText('%.2f'%self.slidervalue)
        if len(self.itemArr)!=21:
            return
        self.qp.eraseRect(QRectF(QPointF(0, 0), QPointF(480, 360)))
        newImg=self.itemArr[index]
        # print(index)
        self.imabland = QImage.fromData(newImg)
        self.imabland= QImage(newImg.data, newImg.shape[1], newImg.shape[0], newImg.strides[0], QImage.Format_RGB888);
        self.imabland=self.imabland.scaledToWidth(480-2)
        self.imabland=self.imabland.scaledToHeight(360-2)
        self.imabland=QPixmap.fromImage(self.imabland)
        self.MarkLeft=1
        self.blend_image.scene = QGraphicsScene()  # ???????????
        item = QGraphicsPixmapItem(self.imabland)  # ????????????????
        self.blend_image.scene.addItem(item)  # ??????????scene??
        self.blend_image.setScene(self.blend_image.scene)
    def loadimg1(self):
        self.image1 = QPixmap()
        sz = QSize(720, 540)
        path, _ = QFileDialog.getOpenFileName(self, 'choose image', None, 'Image files(*.jpg *.gif *.png)')
        self.leftPath=path[0:len(path)-4]
        # leftImage = imageio.imread(self.leftPath + '.png')
        # print(leftImage)
        print(self.leftPath)
        with open(path,'rb') as fp:
            img=fp.read()
        self.imageee1 = QImage.fromData(img)
        self.imageee1=self.imageee1.scaledToWidth(480-2)
        self.imageee1=self.imageee1.scaledToHeight(360-2)
        self.img1=self.imageee1

        self.image1=QPixmap.fromImage(self.imageee1)
        self.MarkLeft=1
        self.start_image.scene = QGraphicsScene()  # ???????????
        item = QGraphicsPixmapItem(self.image1)  # ????????????????
        self.start_image.scene.addItem(item)  # ??????????scene??
        self.start_image.setScene(self.start_image.scene)
        if self.img1!=None and self.img2!=None:
            self.loadPoints()


    def loadimg2(self):
        self.image2 = QPixmap()
        path, _ = QFileDialog.getOpenFileName(self, 'choose image', None, 'Image files(*.jpg *.gif *.png)')
        self.rightPath=path[0:len(path)-4]
        with open(path,'rb') as fp:
            img=fp.read()
        self.imageee2 = QImage.fromData(img)
        self.imageee2=self.imageee2.scaledToWidth(480-2)
        self.imageee2=self.imageee2.scaledToHeight(360-2)
        self.img2 = self.imageee2

        self.image2=QPixmap.fromImage(self.imageee2)
        self.end_image.scene = QGraphicsScene()  # ???????????
        item = QGraphicsPixmapItem(self.image2)  # ????????????????
        self.end_image.scene.addItem(item)  # ??????????scene??
        self.MarkLeft=1
        self.end_image.setScene(self.end_image.scene)
        if self.img1!=None and self.img2!=None:
            self.loadPoints()
    # def operatePointsFile(self):
    #     self.numPoints=min(len(self.rightPoints),len(self.leftPoints))
    #     if os.path.exists(self.leftPath+'.txt') and os.path.exists(self.rightPath+'.txt'):
    #         # tris=loadTriangles(self.leftPath+'.txt',self.rightPath+'.txt')
    #         pointL = np.loadtxt(self.leftPath+'.txt', dtype=np.float64)
    #         pointR = np.loadtxt(self.rightPath+'.txt', dtype=np.float64)
    #         self.rightPoints=[]
    #         self.leftPoints=[]
    #         for lp in pointL:
    #             self.leftPoints.append(QPointF(lp[0]/3,lp[1]/3))
    #         for rp in pointR:
    #             self.rightPoints.append(QPointF(rp[0]/3,rp[1]/3))
    #         self.draw1()
    #         self.draw2()
    #         print(self.numPoints)
    #         print(self.rightPoints)
    #     else:
    #         self.writePoints()

    def draw1(self):
        self.qp.eraseRect(QRectF(QPointF(0, 0), QPointF(480, 360)))
        with open(self.leftPath+'.png', 'rb') as fp:
            img = fp.read()
        self.imageee1 = QImage.fromData(img)
        self.imageee1=self.imageee1.scaledToWidth(480-2)
        self.imageee1=self.imageee1.scaledToHeight(360-2)
        self.img1=self.imageee1

        self.qp.begin(self.img1)
        self.qp.setPen(Qt.red)
        # self.qp.eraseRect(QRectF(QPointF(0, 0), QPointF(480, 360)))
        for i in range(0,len(self.leftPoints)):
            if i<self.fromfileLen:
                self.qp.setPen(Qt.red)
            elif i < self.comfirmedLen:
                self.qp.setPen(Qt.blue)
            else:
                self.qp.setPen(Qt.green)
            self.qp.drawEllipse(self.leftPoints[i], 2, 2)
            # self.qp.drawPoint(point)
        if self.show_triangles.isChecked()==True:
            self.qp.setPen(Qt.yellow)
            try:
                tris=loadTrianglesResize(self.leftPath+'.png.txt', self.rightPath+'.png.txt')
            except Exception as e:
                return
            print(len(tris[0]))
            print(self.comfirmedLen)
            for tri in tris[0]:
                tri=tri.vertices
            # print(tri)
                self.qp.drawLine(tri[0][0],tri[0][1],tri[1][0],tri[1][1])
                self.qp.drawLine(tri[0][0], tri[0][1], tri[2][0], tri[2][1])
                self.qp.drawLine(tri[1][0], tri[1][1], tri[2][0], tri[2][1])
        self.qp.end()
        item = QGraphicsPixmapItem(self.image1)  # ????????????????
        self.start_image.scene.addItem(item)  # ??????????scene??
        self.start_image.scene.addPixmap(QPixmap.fromImage(self.img1))
        self.start_image.setScene(self.start_image.scene)
        self.update()
        if os.path.exists(self.leftPath + '.png.txt') and os.path.exists(
                self.rightPath + '.png.txt') and self.img1 != None and self.img2 != None:
            self.allowbland = 1
        # QGraphicsScene.removeItem()
    def draw2(self):
        with open(self.rightPath + '.png', 'rb') as fp:
            img = fp.read()
        self.imageee2 = QImage.fromData(img)
        self.imageee2 = self.imageee2.scaledToWidth(480 - 2)
        self.imageee2 = self.imageee2.scaledToHeight(360 - 2)


        self.img2=self.imageee2

        self.qp.begin(self.img2)
        self.qp.setPen(Qt.green)
        for i in range(0,len(self.rightPoints)):
            if i<self.fromfileLen:
                self.qp.setPen(Qt.red)
            elif i < self.comfirmedLen:
                self.qp.setPen(Qt.blue)
            else:
                self.qp.setPen(Qt.green)
            self.qp.drawEllipse(self.rightPoints[i], 2, 2)
        if self.show_triangles.isChecked() == True:
            self.qp.setPen(Qt.yellow)
            try:
                tris = loadTrianglesResize(self.leftPath + '.png.txt', self.rightPath + '.png.txt')
            except Exception as e:
                return
            for tri in tris[1]:
                tri = tri.vertices
                # print(tri)
                self.qp.drawLine(tri[0][0], tri[0][1], tri[1][0], tri[1][1])
                self.qp.drawLine(tri[0][0], tri[0][1], tri[2][0], tri[2][1])
                self.qp.drawLine(tri[1][0], tri[1][1], tri[2][0], tri[2][1])
        self.qp.end()
        item = QGraphicsPixmapItem(self.image2)  # ????????????????
        self.end_image.scene.addItem(item)  # ??????????scene??
        self.end_image.scene.addPixmap(QPixmap.fromImage(self.img2))
        self.end_image.setScene(self.end_image.scene)
        self.update()
        if os.path.exists(self.leftPath + '.png.txt') and os.path.exists(
                self.rightPath + '.png.txt') and self.img1 != None and self.img2 != None:
            self.allowbland = 1
    def loadPoints(self):
        self.fromfileLen=0
        if os.path.exists(self.leftPath+'.png.txt') and os.path.exists(self.rightPath+'.png.txt'):
            # tris=loadTriangles(self.leftPath+'.txt',self.rightPath+'.txt')
            pointL = np.loadtxt(self.leftPath+'.png.txt', dtype=np.float64)
            pointR = np.loadtxt(self.rightPath+'.png.txt', dtype=np.float64)
            self.rightPoints=[]
            self.leftPoints=[]
            for lp in pointL:
                self.leftPoints.append(QPointF(lp[0]/3,lp[1]/3))
                self.fromfileLen+=1
            for rp in pointR:
                self.rightPoints.append(QPointF(rp[0]/3,rp[1]/3))
            self.comfirmedLen=self.fromfileLen
            print(self.leftPoints)
            print(self.fromfileLen)
            try:
                self.draw1()
                self.draw2()
            except Exception as e:
                pass

            # print(self.numPoints)
            # print(self.rightPoints)
    def writePoints(self):
        self.numPoints=min(len(self.leftPoints),len(self.rightPoints))
        fp1=open(self.leftPath+'.png.txt','w')
        fp2=open(self.rightPath+'.png.txt','w')
        # fp1=open('temp1.txt','w')
        # fp2=open('temp2.txt','w')
        for i in range(0,self.comfirmedLen):
            fp1.write('%.1f %.1f\n'%(self.leftPoints[i].x()*3,self.leftPoints[i].y()*3))
            fp2.write('%.1f %.1f\n' % (self.rightPoints[i].x()*3, self.rightPoints[i].y()*3))
        fp1.close()
        fp2.close()

    def blendingBtnHandler(self):

        t1=time.time()
        # for i in range(5):
        #     p.apply_async(long_time_task, args=(i,))
        # print('Waiting for all subprocesses done...')
        # p.close()
        # p.join()
        print('All subprocesses done.')
        # if os.path.exists(self.leftPath+'.png.txt') and os.path.exists(self.rightPath+'.png.txt') and self.img1!=None and self.img2!=None:
        #     self.allowbland=1
        if self.allowbland==0:
            return
        self.allowbland = 0
        # self.operatePointsFile()
        processPoll = Pool(8)
        resultlist=[]
        self.itemArr=[]
        path1=self.leftPath
        path2=self.rightPath
        for i in range (0,101,5):
            res=processPoll.apply_async(MorphImgxx,args=(path1,path2,i/100.0,))
            # res=self.MorphImg(alpha=i/100.0)
            resultlist.append(res)
            # print(i)
        processPoll.close()
        # print('xxx')
        processPoll.join()
        # print('yyy')
        self.allowbland=0
        for r in resultlist:
            # print(type(r))
            # print(r.get())
            self.itemArr.append(r.get())
        t2=time.time()
        print(t2-t1)
        self.previndex=-1
        self.valChangeHandler()
        # self.MorphImg(alpha=self.slidervalue)
    # def showTriangle(self):

    def MorphImg(self,alpha):
        # self.leftPath='TestData/LeftColor'
        # self.rightPath='TestData/RightColor'
        t1 = time.time()
        out = loadTrianglesResize(self.leftPath+'.png.txt', self.rightPath+'.png.txt')
        t3 = time.time()
        # out = loadTrianglesResize('temp1.txt','temp2.txt')
        # leftImage = imageio.imread(self.leftPath+'.png')
        leftImage = Image.open(self.leftPath + '.png')
        leftImage=leftImage.resize([480,360])
        # leftImage.show()
        leftImage=np.array(leftImage.getdata()).reshape(leftImage.size[1], leftImage.size[0], 3)

        rightImage = Image.open(self.rightPath+'.png')
        rightImage=rightImage.resize([480,360])
        # rightImage.show()
        rightImage=np.array(rightImage.getdata()).reshape(rightImage.size[1], rightImage.size[0], 3)

        morpher = MyMorpher(leftImage, out[0], rightImage, out[1])
        newImg=morpher.getImageAtAlpha(alpha)

        # self.imabland = QImage.fromData(newImg)
        # self.imabland= QImage(newImg.data, newImg.shape[1], newImg.shape[0], newImg.strides[0], QImage.Format_RGB888);
        # self.imabland=self.imabland.scaledToWidth(480-2)
        # self.imabland=self.imabland.scaledToHeight(360-2)
        # self.imabland=QPixmap.fromImage(self.imabland)
        # self.MarkLeft=1
        # self.blend_image.scene = QGraphicsScene()  # ???????????
        # item = QGraphicsPixmapItem(self.imabland)  # ????????????????
        # self.blend_image.scene.addItem(item)  # ??????????scene??
        # self.blend_image.setScene(self.blend_image.scene)

        t2 = time.time()
        print(t2-t1)
        return newImg
        # itemcpy=deepcopy(item)
        # print(item==itemcpy)
        # return itemcpy

        # print(t2 - t1)
def MorphImgxx(path1,path2,alpha):
    # self.leftPath='TestData/LeftColor'
    # self.rightPath='TestData/RightColor'
    t1 = time.time()
    out = loadTrianglesResize(path1+'.png.txt',path2+'.png.txt')
    t3 = time.time()
    # out = loadTrianglesResize('temp1.txt','temp2.txt')
    # leftImage = imageio.imread(self.leftPath+'.png')
    leftImage = Image.open(path1 + '.png')
    leftImage=leftImage.resize([480,360])
    if leftImage.mode=='L':
        chan=1
    else:
        chan=3
    # print(chan)
    # leftImage.show()
    leftImage=np.array(leftImage.getdata()).reshape(leftImage.size[1], leftImage.size[0], chan)
    rightImage = Image.open(path2+'.png')
    rightImage=rightImage.resize([480,360])
    # rightImage.show()
    rightImage=np.array(rightImage.getdata()).reshape(rightImage.size[1], rightImage.size[0], chan)

    # leftImage=Image.fromarray(leftImage,mode='RGB')
    # leftImage=np.array(leftImage.getdata()).reshape(leftImage.size[1], leftImage.size[0], 3)
    # rightImage=Image.fromarray(rightImage,mode='RGB')
    # rightImage = np.array(rightImage.getdata()).reshape(rightImage.size[1], rightImage.size[0], 3)
    # print(leftImage.shape)
    # print(rightImage.shape)
    morpher = MyMorpher(leftImage, out[0], rightImage, out[1])
    newImg=morpher.getImageAtAlpha(alpha)
    # self.imabland = QImage.fromData(newImg)
        # self.imabland= QImage(newImg.data, newImg.shape[1], newImg.shape[0], newImg.strides[0], QImage.Format_RGB888);
        # self.imabland=self.imabland.scaledToWidth(480-2)
        # self.imabland=self.imabland.scaledToHeight(360-2)
        # self.imabland=QPixmap.fromImage(self.imabland)
        # self.MarkLeft=1
        # self.blend_image.scene = QGraphicsScene()  # ???????????
        # item = QGraphicsPixmapItem(self.imabland)  # ????????????????
        # self.blend_image.scene.addItem(item)  # ??????????scene??
        # self.blend_image.setScene(self.blend_image.scene)

    t2 = time.time()
    # print(t2-t1)
    return newImg
def loadTrianglesResize(leftPointFilePath, rightPointFilePath):
    list1=[]
    list2=[]
    pointL = (np.loadtxt(leftPointFilePath,dtype=np.float64)/3).round(0)
    # print(pointL)
    pointR = (np.loadtxt(rightPointFilePath, dtype=np.float64)/3).round(0)
    indexs = Delaunay(np.array(pointL)).simplices
    for i in indexs:
        # print(pointL[i])
        list1.append(Triangle(pointL[i]))
        list2.append(Triangle(pointR[i]))
    return(list1,list2)

class MyMorpher(Morpher):
    def getImageAtAlpha(self, alpha):
        li = self.leftImage
        ri = self.rightImage
        shp = self.leftImage.shape

        # shp = [shp[0], shp[1]]
        # if li.shape[2]==3:
        res = np.zeros(self.leftImage.shape)
        # else:
        #     res = np.zeros(shp)
        # print(res.shape)
        for i in range(0, len(self.leftTriangles)):
            vtmid = (1 - alpha) * (self.leftTriangles[i].vertices) + alpha * (self.rightTriangles[i].vertices)

            midtri = Triangle(vtmid)

            vt1 = self.leftTriangles[i].vertices
            vt2 = self.rightTriangles[i].vertices
            h_mid2left = getH(vt1, vtmid)
            h_mid2right = getH(vt2, vtmid)
            midpoints = midtri.getPoints()
            midpoints = np.insert(midpoints, 2, 1, axis=1).T
            # print(len(midpoints[0]))
            indexleft = (h_mid2left).dot(midpoints).astype(int)
            indexright = (h_mid2right).dot(midpoints).astype(int)
            midpoints = midpoints.astype(int)
            # print(len(midpoints[0]))
            # print()

            for i in range(0, len(midpoints[0])):
                # print(indexleft[1][i])
                # print(indexleft[0][i])
                try:
                    leftval = li[indexleft[1][i]-1][indexleft[0][i]-1]
                    rightval = ri[indexright[1][i]-1][indexright[0][i]-1]
                    color = np.array((alpha * rightval + (1 - alpha) * leftval).astype(int))
                    res[midpoints[1][i]-1][midpoints[0][i]-1] = color
                except Exception:
                    res[midpoints[1][i] - 1][midpoints[0][i] - 1]=0
        return res.astype(np.uint8)
if __name__ == '__main__':
    # out = loadTriangles('alpha25.txt', 'alpha75.txt')
    # print(out[0])
    # print(out[1])
    currentApp = QApplication(sys.argv)
    currentForm = MorphingApp()
    # currentForm.MorphImg(0.5)
    # currentForm.loadimg1()
    # currentForm.loadimg2()
    # currentForm.blendingBtnHandler()
    # currentForm.loadPoints()
    currentForm.show()
    currentApp.exec_()
    # leftImage1 = Image.open('TestData/LeftGray' + '.png')
    # leftImage2 = Image.open('TestData/LeftColor' + '.png')
    # print(leftImage1)
    # print(leftImage2)
    # leftImage=leftImage.resize([480,360])