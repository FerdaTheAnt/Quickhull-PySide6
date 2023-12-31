import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

import quickhull

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.GeoArea = GeoArea()
        self.setCentralWidget(self.GeoArea)
        self.toolBar = QtWidgets.QToolBar()
        self.createActions()
        self.addToolBar(self.toolBar)

    def randomAct(self):
        self.GeoArea.randomSet()

    def quickHullAct(self):
        self.GeoArea.quickHull()

    def clearAct(self):
        self.GeoArea.clear()

    def createActions(self):
        randomAction = QtGui.QAction("Random set", self)
        randomAction.triggered.connect(self.randomAct)
        self.toolBar.addAction(randomAction)

        quickHullAction = QtGui.QAction("QuickHull", self)
        quickHullAction.triggered.connect(self.quickHullAct)
        self.toolBar.addAction(quickHullAction)

        clearAction = QtGui.QAction("Clear", self)
        clearAction.triggered.connect(self.clearAct)
        self.toolBar.addAction(clearAction)

class GeoArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.points = set()
        self.lastPoint = None
        self.pointCounter = 0
        self.MAX_POINTS = 200
        self.pen = QtGui.QPen(QtGui.QColor("green"), 5)
        self.brush = QtGui.QBrush(QtGui.QColor("green"), QtCore.Qt.SolidPattern)
        self.image = QtGui.QImage()

    def paintEvent(self, pe):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0,self.image)
    
    def mousePressEvent(self, event):
        if(event.button() == QtCore.Qt.LeftButton):
            pos = event.position()
            self.createPoint(pos.x(), pos.y())

    def resizeEvent(self, re):
        if(self.width() > self.image.width() or self.height() > self.image.height()):
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, QtCore.QSize(newWidth, newHeight))
            self.update()

    def createPoint(self, x, y):
        if(not self.image.isNull() and self.pointCounter < self.MAX_POINTS):
            self.pointCounter += 1
            self.lastPoint = (x,y)
            self.points.add((x,y))

            painter = QtGui.QPainter(self.image)
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.drawEllipse(x, y, 2, 2)

            self.update()

    def randomSet(self):
        self.clear()
        for _ in range(self.MAX_POINTS):
            temp_x = random.gauss(0, 1)*(self.width())%(self.width()-100) + 50
            temp_y = random.gauss(0, 1)*(self.height())%(self.height()-100) + 50
            # temp_x = random.uniform(10, self.height()-10)
            # temp_y = random.uniform(10, self.height()-10)
            self.createPoint(temp_x, temp_y)

    def resizeImage(self, oldImage, newSize):
        if (self.image.size() == newSize):
            return
        
        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.QColor("white"))
        painter = QtGui.QPainter(newImage)
        
        painter.drawImage(0, 0, oldImage)
        self.image = newImage

    def quickHull(self):
        hull = quickhull.beginQuickHull(self.points)
        #prototype
        if(hull):
            self.clear()
            for point in hull:
                self.createPoint(point[0], point[1])

    def clear(self):
        self.points.clear()
        self.pointCounter = 0
        self.image.fill(QtGui.QColor("white"))
        self.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())