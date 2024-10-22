import os
import sys
import json
import time
import subprocess

from PyQt5.Qt import Qt
from PyQt5.Qt import QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFileDialog

from qfluentwidgets import PushButton
from qfluentwidgets import FluentIcon
from qfluentwidgets import MessageBox
from qfluentwidgets import SingleDirectionScrollArea

from Base.AiNieeBase import AiNieeBase
from Widget.EmptyCard import EmptyCard
from Widget.SwitchButtonCard import SwitchButtonCard

class AppSettingsPage(QWidget, AiNieeBase):

    DEFAULT = {
        "font_hinting": True,
    }

    def __init__(self, text: str, window):
        super().__init__(window)
        self.setObjectName(text.replace(" ", "-"))

        # 载入配置文件
        config = self.load_config()

        # 设置主容器
        self.container = QVBoxLayout(self)
        self.container.setContentsMargins(0, 0, 0, 0)

        # 设置滚动容器
        self.scroller = SingleDirectionScrollArea(self, orient = Qt.Vertical)
        self.scroller.setWidgetResizable(True)
        self.scroller.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.container.addWidget(self.scroller)

        # 设置容器
        self.vbox_parent = QWidget(self)
        self.vbox_parent.setStyleSheet("QWidget { background: transparent; }")
        self.vbox = QVBoxLayout(self.vbox_parent)
        self.vbox.setSpacing(8)
        self.vbox.setContentsMargins(24, 24, 24, 24) # 左、上、右、下
        self.scroller.setWidget(self.vbox_parent)

        # 添加控件
        self.add_widget_font_hinting(self.vbox, config)
        self.add_widget_app_profile(self.vbox, config, window)

        # 填充
        self.vbox.addStretch(1)

    # 应用字体优化
    def add_widget_font_hinting(self, parent, config):
        def init(widget):
            widget.set_checked(config.get("font_hinting"))
            
        def checked_changed(widget, checked: bool):
            config = self.load_config()
            config["font_hinting"] = checked
            self.save_config(config)

        parent.addWidget(
            SwitchButtonCard(
                "应用字体优化", 
                "启用此功能后，应用内字体会更加圆润，但是边缘会稍显模糊（切换将在应用重启后生效）",
                init = init,
                checked_changed = checked_changed,
            )
        )
    
    # 应用配置切换
    def add_widget_app_profile(self, parent, config, window):

        # 重启应用
        def restart_app():
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit(0)

        # 导入配置文件
        def import_profile_file(path):
            profile = {}

            if os.path.exists(path):
                with open(path, "r", encoding = "utf-8") as reader:
                    profile = json.load(reader)
            else:
                self.error_toast("", "配置文件不存在！")
                return

            if len(profile) == 0 or "target_platform" not in profile:
                self.error_toast("", "配置文件内容未通过校验！")
                return

            # 确认框
            message_box = MessageBox("警告", "是否确认导入选中的配置文件，导入后应用将自动重启 ...", window)
            message_box.yesButton.setText("确认")
            message_box.cancelButton.setText("取消")
            if message_box.exec():
                self.success_toast("", "配置文件导入成功，应用即将自动重启！")
            else:
                return

            # 保存配置文件
            config = self.load_config()
            for k, v in profile.items():
                if k != "platforms":
                    config[k] = v
            self.save_config(config)

            # 重启应用
            QTimer.singleShot(1000, restart_app)

        # 导出配置文件
        def export_profile_file(path):
            config = self.load_config()
            del config["platforms"]

            with open(f"{path}/ainiee_profile.json", "w", encoding = "utf-8") as writer:
                writer.write(json.dumps(config, indent = 4, ensure_ascii = False))
                
            self.success_toast("", "配置已导出为 \"ainiee_profile.json\" ...")

        # 导入按钮点击事件
        def on_improt_button_clicked():
            path, _ = QFileDialog.getOpenFileName(None, "选择文件", "", "json files (*.json)")

            if path == None or path == "":
                return
            
            import_profile_file(path)
        # 导出按钮点击事件
        def on_exprot_button_clicked():
            path = QFileDialog.getExistingDirectory(None, "选择文件夹", "")

            if path == None or path == "":
                return
            
            export_profile_file(path)

        def init(widget):
            improt_button = PushButton("导入", self)
            improt_button.setIcon(FluentIcon.DOWNLOAD)
            improt_button.setContentsMargins(4, 0, 4, 0)
            improt_button.clicked.connect(on_improt_button_clicked)

            export_button = PushButton("导出", self)
            export_button.setIcon(FluentIcon.SHARE)
            export_button.setContentsMargins(4, 0, 4, 0)
            export_button.clicked.connect(on_exprot_button_clicked)

            widget.add_widget(improt_button)
            widget.add_spacing(16)
            widget.add_widget(export_button)

        parent.addWidget(
            EmptyCard(
                "应用配置切换", 
                "可以将当前应用的除接口信息以外的所有设置导出为配置文件，以方便根据不同项目切换配置（导入配置后应用将自动重启）",
                init = init,
            )
        )