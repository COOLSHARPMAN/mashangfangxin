import winreg
import chardet
from datetime import datetime
import os
import configparser
import random
import re


def readreg(key,value_name):
    """读取注册表中指定键的值（默认值用空字符串）"""
    try:

        return winreg.QueryValueEx(key, value_name)[0]
    except FileNotFoundError:
        print(f"键不存在: ")
        return None
    except PermissionError:
        print(f"无权限访问: （可能需要管理员权限）")
        return None
    except Exception as e:
        print( f"错误: {str(e)}")
        return None

def convert_to_utf8(file_path, original_encoding=None):
    """
    将文件编码转换为UTF-8

    参数:
        file_path: 配置文件路径
        original_encoding: 原始编码，如果为None则自动检测
    """
    try:
        # 读取文件内容
        with open(file_path, 'rb') as f:
            content = f.read()

        # 检测文件编码
        if not original_encoding:
            result = chardet.detect(content)
            original_encoding = result['encoding']
            confidence = result['confidence']
            print(f"检测到文件编码: {original_encoding} (可信度: {confidence:.2f})")

        # 如果已经是UTF-8则不需要转换
        if original_encoding and original_encoding.lower() in ['utf-8', 'utf8']:
            print(f"文件 {file_path} 已经是UTF-8编码")
            return True

        # 解码并重新编码为UTF-8
        try:
            # 解码原始内容
            text = content.decode(original_encoding)

            # 创建备份文件
            backup_path = f"{file_path}.bak"
            if not os.path.exists(backup_path):
                with open(backup_path, 'wb') as f:
                    f.write(content)
                print(f"已创建备份文件: {backup_path}")

            # 以UTF-8编码写入
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)

            print(f"文件 {file_path} 已成功转换为UTF-8编码")
            return True

        except UnicodeDecodeError:
            print(f"错误: 无法用 {original_encoding} 编码解码文件 {file_path}")
            return False

    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return False

def get_current_time_ms():
    # 利用strftime获取基本时间，再补充毫秒部分
    now = datetime.now()
    # %f 表示微秒，取前3位即为毫秒
    return now.strftime("%Y%m%d%H%M%S") + now.strftime("%f")[:3]


def extract_hospital_name(full_name):
    # 去除开头的数字和字母
    pattern1 = r'^[0-9a-zA-Z]+'
    name = re.sub(pattern1, '', full_name)

    # 新增：去除头部中文括号及其内容
    # 匹配以"（"开头，中间包含任意字符，以"）"结束的内容
    pattern3 = r'^[（][^）]*[）]'
    name = re.sub(pattern3, '', name)

    # 去除最后一个括号及其内容
    pattern2 = r'[（(][^）)]*[)）]$'
    name = re.sub(pattern2, '', name)

    return name.strip()


def get_int(start,end,os=0,float=False):
    if float:
        return random.uniform(start, end)
    elif os==2:
        return random.randrange(start,end,2)
    elif os==0:
        return random.randint(start,end)

def convert_date_format(date_str):
    # 假设date_str是一个有效的8位日期字符串
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date

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