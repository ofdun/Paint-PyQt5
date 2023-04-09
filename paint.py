import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction,\
    QFileDialog, QMessageBox, QSlider, QLabel, QColorDialog, QPushButton
from PyQt5.QtGui import QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QSize

class App(QMainWindow):
    def __init__(self, width: int = 800, height: int = 600) -> None:
        super().__init__()
        self.adjustSize()
        self.setFixedSize(width, height)
        self.setWindowTitle("Paint!")
        menu_bar = self.menuBar()

        self.image = QImage(QSize(width, height), QImage.Format_RGB32 )
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_color = Qt.black
        self.last_point = QPoint()
        
        self.toolbar = self.addToolBar("TOOLBAR")
        self.toolbar.setFixedHeight(self.percent(height, 7))
        
        # brush_picture = QPixmap('pictures/brush.png')
        brush_label = QLabel(self)
        self.brush_value_label = QLabel(self)
        
        # brush_label.setPixmap(brush_picture)
        # brush_label.resize(20, 20)
        brush_label.setText("Brush Size:")
        self.brush_value_label.setText("8")
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setFixedWidth(self.percent(width, 20))
        self.slider.setRange(2, 48)
        self.slider.setSliderPosition(8)
        self.brush_size = self.slider.value()
        self.slider.valueChanged[int].connect(self.changeBrushSize)
        
        self.color_choose_button = QPushButton("Color", self)
        self.color_choose_button.clicked.connect(self.changeColor)
        
        self.toolbar.addWidget(self.color_choose_button)
        self.toolbar.addWidget(brush_label)
        self.toolbar.addWidget(self.slider)
        self.toolbar.addWidget(self.brush_value_label)
        
        file_menu = menu_bar.addMenu("File")
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        save_action.triggered.connect(self.save_picture)
        
        clear_action = QAction("Clear", self)
        clear_action.setShortcut("Ctrl+C")
        file_menu.addAction(clear_action)
        clear_action.triggered.connect(self.clear_picture)
        
    def changeColor(self) -> None:
        color = QColorDialog.getColor(self.brush_color, self)
        self.brush_color = color
        
    def changeBrushSize(self, size: int) -> None:
        self.brush_size = size
        self.brush_value_label.setText( str( self.slider.value() ) )
    
    @staticmethod
    def percent(number: int, percent: int) -> int:
        return round(number * (percent/100))
        
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
    
    def mouseMoveEvent(self, event) -> None:
         
        if (event.buttons() & Qt.LeftButton) and self.drawing:
             
            painter = QPainter(self.image)
             
            painter.setPen(QPen(
                self.brush_color,
                self.brush_size, Qt.SolidLine,
                Qt.RoundCap, Qt.RoundJoin))
             
            painter.drawLine(self.lastPoint, event.pos() )
             
            self.lastPoint = event.pos()
            self.update()
 
    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.drawing = False
 
    def paintEvent(self, _) -> None:
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
