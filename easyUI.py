from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.baseDataDirButton = QtWidgets.QPushButton(self)
        self.baseDataDirButton.setGeometry(QtCore.QRect(18, 40, 101, 25))
        self.baseDataDirButton.setObjectName("baseDataDirButton")
        self.successDataDirButton = QtWidgets.QPushButton(self)
        self.successDataDirButton.setGeometry(QtCore.QRect(18, 160, 101, 25))
        self.successDataDirButton.setObjectName("successDataDirButton")
        self.testDataDirButton = QtWidgets.QPushButton(self)
        self.testDataDirButton.setGeometry(QtCore.QRect(18, 100, 101, 25))
        self.testDataDirButton.setObjectName("testDataDirButton")
        self.runProcess = QtWidgets.QPushButton(self)
        self.runProcess.setGeometry(QtCore.QRect(18, 220, 101, 25))
        self.runProcess.setObjectName("runProcess")

        self.baseDataLable = QtWidgets.QLabel(self)
        self.baseDataLable.setGeometry(QtCore.QRect(140, 38, 800, 31))
        self.baseDataLable.setObjectName("baseDataLable")
        self.testDataLable = QtWidgets.QLabel(self)
        self.testDataLable.setGeometry(QtCore.QRect(140, 98, 800, 31))
        self.testDataLable.setObjectName("testDataLable")
        self.successDataLable = QtWidgets.QLabel(self)
        self.successDataLable.setGeometry(QtCore.QRect(140, 158, 800, 31))
        self.successDataLable.setObjectName("successDataLable")
        self.timeLable = QtWidgets.QLabel(self)
        self.timeLable.setGeometry(QtCore.QRect(140, 218, 800, 31))
        self.timeLable.setObjectName("timeLable")

        self.baseDataDirButton.setText("基础数据路径")
        self.successDataDirButton.setText("文件保存路径")
        self.testDataDirButton.setText("测试数据路径")
        self.runProcess.setText("运行")
        self.baseDataLable.setText("无")
        self.testDataLable.setText("无")
        self.successDataLable.setText("无")
        self.timeLable.setText("总耗时为： 0s, 预处理时间： 0s, \n"
                               "查找总时间： 0s, 加载耗时：0s, 查找用时：0s")

        # # 绑定事件
        self.baseDataDirButton.clicked.connect(self.base_data_message)
        self.testDataDirButton.clicked.connect(self.test_data_message)
        self.successDataDirButton.clicked.connect(self.success_data_message)
        self.runProcess.clicked.connect(self.run_process)

    def base_data_message(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件夹")  # 起始路径
        self.baseDataLable.setText(fileName)
        self.base_data_fileName = fileName

    def test_data_message(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件夹")  # 起始路径
        self.testDataLable.setText(fileName)
        self.test_data_fileName = fileName

    def success_data_message(self):
        directory3 = QFileDialog.getExistingDirectory(self, "选取文件夹")  # 起始路径
        self.successDataLable.setText(directory3)
        self.success_data_dir = directory3

    def run_process(self):
        from mainfile.run import run_process
        """
        处理数据开始
        :return:
        """
        print("开始运行")
        run_time = run_process(self.base_data_fileName, self.test_data_fileName, self.success_data_dir)
        self.timeLable.setText(
            "总耗时为： {times}s, 预处理时间： {processing}s, \n"
            "查找总时间： {look_up}s, 加载耗时： {load}s, 查找用时： {search}s"
            .format(times=run_time["times"],
                    processing=run_time["processing"],
                    look_up=run_time["look_up"],
                    load=run_time["load"],
                    search=run_time["search"]
                    ))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.move(600, 200)
    myshow.show()
    sys.exit(app.exec_())
