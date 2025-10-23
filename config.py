# coding=utf-8
import configparser

def read_config(config_path):
    """读取配置文件"""
    conf = configparser.ConfigParser()
    try:
        if conf.read(config_path, encoding='UTF-8-sig'):
            return conf
        return None
    except Exception as e:
        from mylog import MyLog
        MyLog.info(f'读取配置文件失败：{str(e)}')
        return None

def save_config(config_path, config_data):
    """保存配置文件
    :param config_data: 字典格式，如 {'section': {'key': 'value'}}
    """
    conf = configparser.ConfigParser()
    try:
        # 写入sections和keys
        for section, items in config_data.items():
            if not conf.has_section(section):
                conf.add_section(section)
            for key, value in items.items():
                conf.set(section, key, value)
        # 保存文件
        with open(config_path, 'w+', encoding='UTF-8-sig') as f:
            conf.write(f)
        return True
    except Exception as e:
        from mylog import MyLog
        MyLog.info(f'保存配置文件失败：{str(e)}')
        return False