# coding=utf-8
import configparser
import os
import sys
from mylog import MyLog
import chardet

def read_config(file_name):
    if os.path.exists(file_name):

        with open(file_name, 'rb') as f:
            result = chardet.detect(f.read())
        file_encoding = result['encoding']
        confilemain = configparser.ConfigParser()
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding=file_encoding) as f:
                confilemain.read_file(f)
                return confilemain
    else:
        return {}

# def read_config(config_path):
#     """读取配置文件"""
#     conf = configparser.ConfigParser()
#     try:
#         if conf.read(config_path, encoding='UTF-8-sig'):
#             return conf
#         return None
#     except Exception as e:
#         from mylog import MyLog
#         MyLog.info(f'读取配置文件失败：{str(e)}')
#         return None

def get_config_path(config_filename):
    if getattr(sys, 'frozen', False):
        # 打包后，配置文件在exe同目录
        base_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境，在脚本所在目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, config_filename)

def save_config(config_filename, config_data):
    """保存配置文件，自动跳过DEFAULT section"""
    config_path = get_config_path(config_filename)
    try:
        # 确保目录存在
        config_dir = os.path.dirname(config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
            MyLog.info(f"创建配置文件目录: {config_dir}")

        # 创建一个新的配置对象，避免写入DEFAULT section
        new_conf = configparser.ConfigParser()
        # 只复制自定义section（排除DEFAULT）
        for section in config_data.sections():
            if section != 'DEFAULT':  # 跳过DEFAULT
                new_conf.add_section(section)
                for key, value in config_data.items(section):
                    new_conf.set(section, key, value)

        # 写入配置
        with open(config_path, 'w+', encoding='UTF-8-sig') as f:
            new_conf.write(f)
        MyLog.info(f"成功保存配置文件: {config_path}")
        return True
    except Exception as e:
        MyLog.info(f"保存配置文件失败: {str(e)}，路径: {config_path}")
        return False