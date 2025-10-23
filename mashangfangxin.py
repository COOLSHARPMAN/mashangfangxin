# coding=utf-8
# pyinstaller -F -w --paths D:\py_prj\ali_kufang --paths D:\py_prj\ali_kufang\topsdk --hidden-import=topsdk  --hidden-import=flask    --add-data "config.conf;." --add-data "ui/ui_untitled.py;ui"   mashangfangxin.py
# uv pip freeze > requirements.txt
# uv pip install -r requirements.txt
import sys
import os
import datetime
import threading
import socket
import logging
import multiprocessing
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
import winreg

# 第三方库
from flask import Flask, globals, Response

# 项目模块
from ui.ui_untitled import Ui_MainWindow
from mylog import MyLog
import upublic
from config import read_config, save_config  # 提取配置读写到config.py
from alibaba_api import (                   # 接口逻辑提取到alibaba_api.py
    get_name_ex,
    handle_interface_request
)

# Flask应用初始化
app = Flask(__name__)


# Flask接口路由
@app.route('/doZFB_KU', methods=['POST', 'GET'])
def doZFB_KU():
    try:
        # 读取配置
        confile = read_config('config.conf')
        if not confile:
            return "配置文件不存在或读取失败"

        # 校验核心配置
        appkey = confile.get('ZFB', 'appkey')
        appsecret = confile.get('ZFB', 'appsecret')
        if not appkey or not appsecret:
            MyLog.info('服务端支付宝appkey或者appsecret未配置，请配置好再使用')
            return '服务端支付宝appkey或者appsecret未配置，请配置好再使用'

        # 获取请求参数
        interface_id = globals.request.form.get('interface_id')
        if not interface_id:
            MyLog.info('接口ID为空')
            return '接口ID号为空'

        # 处理接口请求（核心逻辑移至alibaba_api.py）
        result = handle_interface_request(
            interface_id=interface_id,
            request=globals.request,
            confile=confile
        )
        return result

    except Exception as e:
        MyLog.info(f'接口处理异常：{str(e)}')
        return f'出现异常：{str(e)}'


# 主窗口类
class MyWindows(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ser_port = 0
        self.init_ui()
        self.bind_events()

    def init_ui(self):
        """初始化UI，加载配置"""
        self.lbl_status.setStyleSheet("color:red;")
        # 加载配置文件
        confile = read_config('config.conf')
        if confile:
            self.edt_port.setText(str(confile.get('main', 'port', fallback='')))
            self.edt_key.setText(str(confile.get('ZFB', 'appkey', fallback='')))
            self.edt_secret.setText(str(confile.get('ZFB', 'appsecret', fallback='')))
            self.edt_name.setText(str(confile.get('ZFB', 'ent_name', fallback='')))
            self.edt_id.setText(str(confile.get('ZFB', 'ent_id', fallback='')))
            self.edt_ent.setText(str(confile.get('ZFB', 'ref_ent_id', fallback='')))
            self.edt_user.setText(str(confile.get('ZFB', 'ref_user_id', fallback='')))

        # 自动启动服务（如果配置完整）
        self.auto_start_service()

    def bind_events(self):
        """绑定按钮事件"""
        self.btn_start.clicked.connect(self.ser_start)  # 开始运行服务
        self.btn_get_config.clicked.connect(self.get_config)  # 获取配置

    def auto_start_service(self):
        """自动启动服务（配置完整时）"""
        if all([
            self.edt_port.text(),
            self.edt_key.text(),
            self.edt_secret.text(),
            self.edt_name.text()
        ]):
            self.ser_port = int(self.edt_port.text())
            self.start_service()

    def ser_start(self):
        """保存配置并启动服务"""
        # 校验必填项
        if not all([
            self.edt_port.text(),
            self.edt_key.text(),
            self.edt_secret.text(),
            self.edt_name.text()
        ]):
            QMessageBox.information(self, '提示', '请配置好端口号、医院名称、阿里巴巴appkey、appsecret后再操作')
            return

        # 保存配置
        config_data = {
            'main': {'port': self.edt_port.text()},
            'ZFB': {
                'appkey': self.edt_key.text(),
                'appsecret': self.edt_secret.text(),
                'ent_name': self.edt_name.text(),
                'ent_id': self.edt_id.text(),
                'ref_ent_id': self.edt_ent.text(),
                'ref_user_id': self.edt_user.text()
            }
        }
        save_config('config.conf', config_data)

        # 启动服务
        self.ser_port = int(self.edt_port.text())
        self.start_service()

    def get_config(self):
        """通过企业名获取配置（调用阿里巴巴接口）"""
        # 校验必填项
        if not all([
            self.edt_port.text(),
            self.edt_key.text(),
            self.edt_secret.text(),
            self.edt_name.text()
        ]):
            QMessageBox.information(self, '提示', '请配置好端口号、医院名称、阿里巴巴appkey、appsecret后再操作')
            return

        # 调用接口获取企业信息
        from alibaba_api import create_ability  # 延迟导入避免循环依赖
        client = create_ability(
            appkey=self.edt_key.text(),
            appsecret=self.edt_secret.text()
        )
        result = get_name_ex(self.edt_name.text(), client)
        if isinstance(result, tuple):
            from_name, third_ent_id, from_id, ref_ent_id = result
            self.edt_id.setText(str(third_ent_id))
            self.edt_ent.setText(str(ref_ent_id))
            self.edt_user.setText(str(third_ent_id))
            # 保存更新后的配置
            confile = read_config('config.conf')
            if confile:
                confile.set('ZFB', 'ent_id', str(third_ent_id))
                confile.set('ZFB', 'ref_ent_id', str(ref_ent_id))
                confile.set('ZFB', 'ref_user_id', str(third_ent_id))
                save_config('config.conf', confile)

    def start_service(self):
        """启动Flask服务（线程方式）"""
        # 设置开机启动
        file_path = os.path.realpath(sys.argv[0])
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run",
                             winreg.KEY_SET_VALUE,
                             winreg.KEY_ALL_ACCESS | winreg.KEY_WRITE | winreg.KEY_CREATE_SUB_KEY)  # By IvanHanloth
        if key:
            if upublic.readreg(key, '阿里巴巴库房') is not None:
                winreg.DeleteValue(key, '阿里巴巴库房')
            winreg.SetValueEx(key, '阿里巴巴库房', 0, winreg.REG_SZ, file_path)
            winreg.CloseKey(key)

        # 检查端口是否被占用
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            iret = s.connect_ex(('127.0.0.1', self.ser_port))
            if iret == 0:
                self.lbl_status.setText(f'{self.ser_port}端口已经被占用')
            else:
                # 启动Flask服务（后台线程）
                kwargs = {
                    'host': '0.0.0.0',
                    'port': self.ser_port,
                    'threaded': True,
                    'use_reloader': False,
                    'debug': False
                }
                threading.Thread(target=app.run, daemon=True, kwargs=kwargs).start()
                # 更新UI状态
                self.lbl_status.setText('服务正在运行中')
                self.lbl_status.setStyleSheet("color:blue;")
                self.btn_start.setText('正在运行')
                self.edt_log.appendPlainText(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:开始运行")
                self.edt_log.appendPlainText(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:端口号={self.ser_port}")
                self.edt_log.appendPlainText(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:日志在{os.getcwd()}\\log")
                self.btn_start.setEnabled(False)
                self.edt_port.setEnabled(False)
        finally:
            s.close()


# 程序入口
if __name__ == '__main__':
    # 初始化日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='sys_logs.log',
        filemode='w'
    )
    logging.debug('记录debug information')
    logging.info('记录info information')

    # 解决多进程打包问题
    multiprocessing.freeze_support()

    # 启动UI
    app_windows = QtWidgets.QApplication(sys.argv)
    my_window = MyWindows()
    my_window.show()
    sys.exit(app_windows.exec())