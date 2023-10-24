# user interface for steganography

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import steganography as steg



class PhotoLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drag & Drop \n Image Here \n\n')
        self.setStyleSheet('''
        QLabel {
            border: 4px dashed #aaa;
        }''')

    def setPixmap(self, *args, **kwargs):
        super().setPixmap(*args, **kwargs)
        self.setStyleSheet('''
        QLabel {
            border: none;
        }''')

class Template(QWidget):

    photo_path = ''
    message = ''

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Steganography')

        self.photo = PhotoLabel()

        # encode, decode, and submit buttons
        self.options_txt = QLabel('Options:')
        self.e_btn = QRadioButton('Encode')
        self.d_btn = QRadioButton('Decode')
        self.submit_btn = QPushButton('Apply')
        self.submit_btn.clicked.connect(self.run_steg)
        self.browse_btn = QPushButton('Browse')
        self.browse_btn.clicked.connect(self.open_image)




        # image preview, browse button, options, and message input
        layout = QGridLayout(self)
        layout.addWidget(self.photo, 0, 0)
        layout.addWidget(self.browse_btn, 1, 0, Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.resize(300, 200)
        layout.addWidget(self.options_txt)
        layout.addWidget(self.e_btn)
        layout.addWidget(self.d_btn)
        layout.addWidget(QLabel('Message:'))
        self.message_box = QLineEdit(self)
        layout.addWidget(self.message_box)
        layout.addWidget(self.submit_btn, 7, 0, Qt.AlignCenter)


    def run_steg(self):
        self.pop = QMessageBox()

        if(self.e_btn.isChecked()):
            msg = steg.messageToBin(self.message_box.text() + steg.encode_key) # add key to msg and convert to bin
            steg.encodeImage(msg, Template.photo_path)
            self.pop.setWindowTitle('Encoded!')
            self.pop.setText('Message has been encoded. New image saved in program directory.')
            self.pop.setIcon(QMessageBox.Information)
            self.pop.exec_()


        if(self.d_btn.isChecked()):
            msg = steg.decodeImage(Template.photo_path)
            self.pop.setWindowTitle('Decoded!')
            self.pop.setText('Message: ' + msg)
            self.pop.setIcon(QMessageBox.Information)
            self.pop.exec_()

        self.pop.buttonClicked.connect(self.pop_clicked())


    # terminates program once operation completed
    def pop_clicked(self, btn):
        Template.close()



    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            filename = event.mimeData().urls()[0].toLocalFile()
            event.accept()
            self.open_image(filename)
        else:
            event.ignore()

    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg *.jpeg)')
            if not filename:
                return
        self.photo.setPixmap(QPixmap(filename))
        Template.photo_path = filename




if __name__ =='__main__':
    app = QApplication(sys.argv)
    gui = Template()
    gui.show()
    sys.exit(app.exec_())