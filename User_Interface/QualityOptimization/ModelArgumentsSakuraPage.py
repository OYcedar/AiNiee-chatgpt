
import os
import json

from rich import print
from PyQt5.Qt import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QVBoxLayout

from qfluentwidgets import HyperlinkLabel

from Widget.SpinCard import SpinCard
from Widget.SliderCard import SliderCard
from Widget.ComboBoxCard import ComboBoxCard
from Widget.SwitchButtonCard import SwitchButtonCard

class ModelArgumentsSakuraPage(QFrame):

    DEFAULT = {
        "Sakura_parameter_adjustment": False,
        "Sakura_top_p": 3,
        "Sakura_Temperature": 1,
        "Sakura_frequency_penalty": 0,
    }

    def __init__(self, text: str, parent = None, configurator = None):
        super().__init__(parent = parent)

        self.setObjectName(text.replace(" ", "-"))
        self.configurator = configurator

        # 载入配置文件
        config = self.load_config()
        config = self.save_config(config)

        # 设置主容器
        self.container = QVBoxLayout(self)
        self.container.setSpacing(8)
        self.container.setContentsMargins(24, 24, 24, 24) # 左、上、右、下

        # 添加控件
        self.add_widget_01(self.container, config)
        self.add_widget_02(self.container, config)
        self.add_widget_03(self.container, config)
        self.add_widget_04(self.container, config)
        self.add_widget_05(self.container, config)

        # 填充
        self.container.addStretch(1)

    # 载入配置文件
    def load_config(self) -> dict[str]:
        config = {}

        if os.path.exists(os.path.join(self.configurator.resource_dir, "config.json")):
            with open(os.path.join(self.configurator.resource_dir, "config.json"), "r", encoding = "utf-8") as reader:
                config = json.load(reader)
        
        return config

    # 保存配置文件
    def save_config(self, new: dict) -> None:
        path = os.path.join(self.configurator.resource_dir, "config.json")
        
        # 读取配置文件
        if os.path.exists(path):
            with open(path, "r", encoding = "utf-8") as reader:
                old = json.load(reader)
        else:
            old = {}

        # 修改配置文件中的条目：如果条目存在，这更新值，如果不存在，则设置默认值
        for k, v in self.DEFAULT.items():
            if not k in new.keys():
                old[k] = v
            else:
                old[k] = new[k]

        # 写入配置文件
        with open(path, "w", encoding = "utf-8") as writer:
            writer.write(json.dumps(old, indent = 4, ensure_ascii = False))

        return old

    # 启动自定义参数
    def add_widget_01(self, parent, config):
        def widget_init(widget):
            widget.setChecked(config.get("Sakura_parameter_adjustment"))
            
        def widget_callback(widget, checked: bool):
            config["Sakura_parameter_adjustment"] = checked
            self.save_config(config)

        parent.addWidget(
            SwitchButtonCard(
                "启动自定义参数", 
                "启用此功能后，将使用本页中设置的参数向模型发送请求",
                widget_init,
                widget_callback,
            )
        )

    # 启动自定义参数
    def add_widget_02(self, parent, config):
        def widget_init(widget, label):
            value = config.get("Sakura_top_p")
            
            widget.setRange(0, 10)
            label.setText(str(value / 10))
            widget.setValue(int(value))
            
        def widget_callback(widget, label, value: int):
            label.setText(str(value / 10))
            config["Sakura_top_p"] = value
            self.save_config(config)

        parent.addWidget(
            SliderCard(
                "top_p", 
                "官方默认值为 0.3",
                widget_init,
                widget_callback,
            )
        )

    # 启动自定义参数
    def add_widget_03(self, parent, config):
        def widget_init(widget, label):
            value = config.get("Sakura_Temperature")
            
            widget.setRange(0, 10)
            label.setText(str(value / 10))
            widget.setValue(int(value))
            
        def widget_callback(widget, label, value: int):
            label.setText(str(value / 10))
            config["Sakura_Temperature"] = value
            self.save_config(config)

        parent.addWidget(
            SliderCard(
                "temperature", 
                "官方默认值为 0.1",
                widget_init,
                widget_callback,
            )
        )
        
    # 启动自定义参数
    def add_widget_04(self, parent, config):
        def widget_init(widget, label):
            value = config.get("Sakura_frequency_penalty")
            
            widget.setRange(-10, 10)
            label.setText(str(value / 10))
            widget.setValue(int(value))
            
        def widget_callback(widget, label, value: int):
            label.setText(str(value / 10))
            config["Sakura_frequency_penalty"] = value
            self.save_config(config)

        parent.addWidget(
            SliderCard(
                "frequency_penalty", 
                "官方默认值为 0.0",
                widget_init,
                widget_callback,
            )
        )
        
    # 添加连接
    def add_widget_05(self, parent, config):
        spacer = QFrame()
        spacer.setFixedHeight(8)
        
        hyper_link_label = HyperlinkLabel(QUrl("https://github.com/SakuraLLM/SakuraLLM#%E6%8E%A8%E7%90%86"), "点击查看官方文档")
        hyper_link_label.setUnderlineVisible(True)
        
        parent.addWidget(spacer, alignment = Qt.AlignHCenter)
        parent.addWidget(hyper_link_label, alignment = Qt.AlignHCenter)