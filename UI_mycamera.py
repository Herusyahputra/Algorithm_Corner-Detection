import sys
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from OpencvQt import Capture, Converter


config = {
    "DURATION_INT": 5
}

def send_email(user, pwd, recipient, subject, body, image_payload):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')

    part.set_payload(image_payload)
    encoders.encode_base64(part)
    filename = QtCore.QDateTime.currentDateTime().toString()+ '.png'
    part.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(part)
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, pwd)
    server.sendmail(user, recipient, text)
    server.quit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        lay = QtWidgets.QVBoxLayout(central_widget)
        self.view = QtWidgets.QLabel()
        self.btn_start = QtWidgets.QPushButton("Start")
        self.btn_stop = QtWidgets.QPushButton("Stop")
        self.btn_send = QtWidgets.QPushButton("Send Email")
        self.label_time = QtWidgets.QLabel()
        lay.addWidget(self.view, alignment=QtCore.Qt.AlignCenter)
        lay.addWidget(self.btn_start)
        lay.addWidget(self.btn_stop)
        lay.addWidget(self.btn_send)
        lay.addWidget(self.label_time, alignment=QtCore.Qt.AlignCenter)
        self.view.setFixedSize(640, 400)
        self.show()
        self.init_camera()
        self.init_email()

    def init_camera(self):
        self.capture = Capture()
        self.converter = Converter()
        captureThread = QtCore.QThread(self)
        converterThread = QtCore.QThread(self)
        self.converter.setProcessAll(False)
        captureThread.start()
        converterThread.start()
        self.capture.moveToThread(captureThread)
        self.converter.moveToThread(converterThread)
        self.capture.frameReady.connect(self.converter.processFrame)
        self.converter.imageReady.connect(self.setImage)
        self.capture.started.connect(lambda: print("started"))
        self.btn_start.clicked.connect(self.capture.start)
        self.btn_stop.clicked.connect(self.capture.stop)

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        self.view.setPixmap(QtGui.QPixmap.fromImage(image))

    def init_email(self):
        timeline = QtCore.QTimeLine(config["DURATION_INT"]*1000, self)
        timeline.frameChanged.connect(self.onFrameChanged)
        timeline.setFrameRange(0, config["DURATION_INT"])
        timeline.setDirection(QtCore.QTimeLine.Backward)
        self.btn_send.clicked.connect(timeline.start)

        d = EmailDialog(self)
        if d.exec_() == EmailDialog.Accepted:
            self._info = d.get_data()

    def onFrameChanged(self, frame):
        if frame !=0:
            self.label_time.setNum(frame)
        else:
            self.label_time.setText("Smile...!")
            QtWidgets.QApplication.beep()
            image = QtGui.QImage(self.converter.image)
            ba = QtCore.QByteArray()
            buff = QtCore.QBuffer(ba)
            image.save(buff, "PNG")
            th = threading.Thread(target=send_email, args=(*self._info, ba))
            th.start()

    def closeEvent(self, event):
        self.capture.stop()
        super(MainWindow, self).closeEvent(event)


class EmailDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EmailDialog, self).__init__(parent)
        lay = QtWidgets.QFormLayout(self)
        self.from_le = QtWidgets.QLineEdit()
        self.pass_le = QtWidgets.QLineEdit(echoMode=QtWidgets.QLineEdit.Password)
        self.to_le = QtWidgets.QLineEdit()
        self.subject_le = QtWidgets.QLineEdit()
        self.body_te = QtWidgets.QTextEdit()

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        lay.addRow("From: ", self.from_le)
        lay.addRow("Password: ", self.pass_le)
        lay.addRow("To: ", self.to_le)
        lay.addRow("Subject: ", self.subject_le)
        lay.addRow("Body: ", self.body_te)
        lay.addRow(self.buttonBox)

        self.from_le.textChanged.connect(self.enable_button)
        self.pass_le.textChanged.connect(self.enable_button)
        self.to_le.textChanged.connect(self.enable_button)
        self.enable_button()

    def enable_button(self):
        disabled = self.from_le.text() == "" or self.pass_le.text() == "" or self.to_le.text() == ""
        self.buttonBox.setDisabled(disabled)

    def get_data(self):
        return self.from_le.text(), self.pass_le.text(), self.to_le.text(), self.subject_le.text(), self.body_te.toPlainText()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())