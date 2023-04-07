import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint


class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        # self.setGeometry(0, 0, 800, 800)
        self.adjustSize()
        self.setFixedSize(800, 600)
        self.setWindowTitle("Paint!")
        menu_bar = self.menuBar()

        self.image = QImage(self.size(), QImage.Format_RGB32 )
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_size = 2
        self.brush_color = Qt.black
        self.last_point = QPoint()
        
        file_menu = menu_bar.addMenu("File")
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        save_action.triggered.connect(self.save_picture)
        
        clear_action = QAction("Clear", self)
        clear_action.setShortcut("Ctrl+C")
        file_menu.addAction(clear_action)
        clear_action.triggered.connect(self.clear_picture)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
    
    def mouseMoveEvent(self, event):
         
        if (event.buttons() and Qt.LeftButton) and self.drawing:
             
            painter = QPainter(self.image)
             
            painter.setPen(QPen(self.brush_color, self.brush_size,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
             
            painter.drawLine(self.lastPoint, event.pos())
             
            self.lastPoint = event.pos()
            self.update()
 
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
 
    def paintEvent(self, _):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
    
    def save_picture(self) -> None:
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image",
                                                  os.path.expanduser("~/Desktop/untitled.png"),
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath:
            self.image.save(filePath)
    
    def clear_picture(self) -> None:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.Yes)
        msg_box.setWindowTitle("Continue?")
        msg_box.setText("Do you really want to continue?")
        res = msg_box.exec_()
        if res == QMessageBox.No: return
        self.image.fill(Qt.white)
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
