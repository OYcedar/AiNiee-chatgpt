
from PyQt5.QtGui import QBrush, QColor, QDesktopServices, QFont, QImage, QPainter, QPixmap#需要安装库 pip3 install PyQt5
from PyQt5.QtCore import  QObject,  QRect,  QUrl,  Qt, pyqtSignal 
from PyQt5.QtWidgets import QAbstractItemView,QHeaderView,QApplication, QTableWidgetItem, QFrame, QGridLayout, QGroupBox, QLabel,QFileDialog, QStackedWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets.components import Dialog  # 需要安装库 pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/
from qfluentwidgets import ProgressRing, SegmentedWidget, TableWidget,CheckBox, DoubleSpinBox, HyperlinkButton,InfoBar, InfoBarPosition, NavigationWidget, Slider, SpinBox, ComboBox, LineEdit, PrimaryPushButton, PushButton ,StateToolTip, SwitchButton, TextEdit, Theme,  setTheme ,isDarkTheme,qrouter,NavigationInterface,NavigationItemPosition, EditableComboBox
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar



class Widget_SakuraLLM(QFrame):#  Sakura基础界面
    def __init__(self, text: str, parent=None,configurator=None,user_interface_prompter=None,background_executor=None):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))
        self.configurator = configurator
        self.user_interface_prompter = user_interface_prompter
        self.background_executor = background_executor
        #设置各个控件-----------------------------------------------------------------------------------------

        # -----创建第1个组，添加多个组件-----
        box_address = QGroupBox()
        box_address.setStyleSheet(""" QGroupBox {border: 1px solid lightgray; border-radius: 8px;}""")#分别设置了边框大小，边框颜色，边框圆角
        layout_address = QHBoxLayout()

        #设置“请求地址”标签
        self.labelA = QLabel( flags=Qt.WindowFlags())  #parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.labelA.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")#设置字体，大小，颜色
        self.labelA.setText("请求地址")

        #设置微调距离用的空白标签
        self.labelB = QLabel()  
        self.labelB.setText("                      ")

        #设置“请求地址”的输入框
        self.LineEdit_address = LineEdit()
        self.LineEdit_address.setText("http://127.0.0.1:8080")
        #LineEdit1.setFixedSize(300, 30)


        layout_address.addWidget(self.labelA)
        layout_address.addWidget(self.labelB)
        layout_address.addWidget(self.LineEdit_address)
        box_address.setLayout(layout_address)


        # -----创建第1个组，添加多个组件-----
        box_model = QGroupBox()
        box_model.setStyleSheet(""" QGroupBox {border: 1px solid lightgray; border-radius: 8px;}""")#分别设置了边框大小，边框颜色，边框圆角
        layout_model = QGridLayout()

        #设置“模型选择”标签
        self.labelx = QLabel(flags=Qt.WindowFlags())  #parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.labelx.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")#设置字体，大小，颜色
        self.labelx.setText("模型选择")


        #设置“模型类型”下拉选择框
        self.comboBox_model = ComboBox() #以demo为父类
        self.comboBox_model.addItems(['Sakura-v0.9','Sakura-v1.0'])
        self.comboBox_model.setCurrentIndex(1) #设置下拉框控件（ComboBox）的当前选中项的索引为0，也就是默认选中第一个选项
        self.comboBox_model.setFixedSize(250, 35)

        


        layout_model.addWidget(self.labelx, 0, 0)
        layout_model.addWidget(self.comboBox_model, 0, 1)
        box_model.setLayout(layout_model)



        # -----创建第3个组，添加多个组件-----
        box_proxy_port = QGroupBox()
        box_proxy_port.setStyleSheet(""" QGroupBox {border: 1px solid lightgray; border-radius: 8px;}""")#分别设置了边框大小，边框颜色，边框圆角
        layout_proxy_port = QHBoxLayout()

        #设置“代理地址”标签
        self.label_proxy_port = QLabel( flags=Qt.WindowFlags())  #parent参数表示父控件，如果没有父控件，可以将其设置为None；flags参数表示控件的标志，可以不传入
        self.label_proxy_port.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 17px;")#设置字体，大小，颜色
        self.label_proxy_port.setText("系统代理")

        #设置微调距离用的空白标签
        self.labelx = QLabel()  
        self.labelx.setText("                      ")

        #设置“代理地址”的输入框
        self.LineEdit_proxy_port = LineEdit()
        #LineEdit1.setFixedSize(300, 30)


        layout_proxy_port.addWidget(self.label_proxy_port)
        layout_proxy_port.addWidget(self.labelx)
        layout_proxy_port.addWidget(self.LineEdit_proxy_port)
        box_proxy_port.setLayout(layout_proxy_port)



        # -----创建第4个组，添加多个组件-----
        box_test = QGroupBox()
        box_test.setStyleSheet(""" QGroupBox {border: 0px solid lightgray; border-radius: 8px;}""")#分别设置了边框大小，边框颜色，边框圆角
        layout_test = QHBoxLayout()


        #设置“测试请求”的按钮
        primaryButton_test = PrimaryPushButton('测试请求', self, FIF.SEND)
        primaryButton_test.clicked.connect(self.test_request) #按钮绑定槽函数

        #设置“保存配置”的按钮
        primaryButton_save = PushButton('保存配置', self, FIF.SAVE)
        primaryButton_save.clicked.connect(self.saveconfig) #按钮绑定槽函数


        layout_test.addStretch(1)  # 添加伸缩项
        layout_test.addWidget(primaryButton_test)
        layout_test.addStretch(1)  # 添加伸缩项
        layout_test.addWidget(primaryButton_save)
        layout_test.addStretch(1)  # 添加伸缩项
        box_test.setLayout(layout_test)



        # -----最外层容器设置垂直布局-----
        container = QVBoxLayout()

        # 设置窗口显示的内容是最外层容器
        self.setLayout(container)
        container.setSpacing(28) # 设置布局内控件的间距为28
        container.setContentsMargins(50, 70, 50, 30) # 设置布局的边距, 也就是外边框距离，分别为左、上、右、下

        # 把各个组添加到容器中
        container.addStretch(1)  # 添加伸缩项
        container.addWidget(box_address)
        container.addWidget(box_model)
        container.addWidget(box_proxy_port)
        container.addWidget(box_test)
        container.addStretch(1)  # 添加伸缩项


    def saveconfig(self):
        self.user_interface_prompter.read_write_config("write",self.configurator.resource_dir)
        self.user_interface_prompter.createSuccessInfoBar("已成功保存配置")

    def test_request(self):

        if self.background_executor.Request_test_switch(self):
            Base_url = self.LineEdit_address.text()
            Model_Type =  self.comboBox_model.currentText()      #获取模型类型下拉框当前选中选项的值
            API_key_str = ""
            Proxy_port = self.LineEdit_proxy_port.text()            #获取代理端口

            #创建子线程
            thread = self.background_executor("接口测试","","","Sakura",Base_url,Model_Type,API_key_str,Proxy_port)
            thread.start()

