#!/usr/bin/env python3
# coding=utf-8
# Author: fyq
'''
写日志单元
'''
import logging
import os
import time
import datetime

LEVELS={'debug':logging.DEBUG,\
        'info':logging.INFO,\
        'warning':logging.WARNING,\
        'error':logging.ERROR,\
        'critical':logging.CRITICAL,}

logger=logging.getLogger()
level='default'

def createFile(filename):
    path=filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename,mode='w')
        fd.close()

def getHandler():

    timenow = datetime.datetime.now().strftime("%Y%m%d")
    log_filename = './log/' + timenow + '.log'
    createFile(log_filename)
    # err_filename='./log/错误日志/'+ timenow+'.log'
    logger.setLevel(LEVELS.get(level, logging.NOTSET))

    # createFile(err_filename)

    # 注意文件内容写入时编码格式指定

    ahandler = logging.FileHandler(log_filename, encoding='utf-8')
    return ahandler

def setHandler(level,handler):
    # if level=='error':
    #    logger.addHandler(MyLog.errhandler)
    # handler=logging.FileHandler(log_filename)
    #把logger添加上handler
    logger.addHandler(handler)

def removerhandler(level,handler):
   # if level=='error':
   #     logger.removeHandler(MyLog.errhandler)
   logger.removeHandler(handler)

def getCurrentTime():
    dateformat = '%Y-%m-%d %H:%M:%S'
    return time.strftime(dateformat,time.localtime(time.time()))

class MyLog:

   # errhandler=logging.FileHandler(err_filename,encoding='utf-8')
    @staticmethod
    def info(log_message,type='info'):
        inhandler = getHandler()
        setHandler(type,inhandler)
        logger.info(getCurrentTime()+"--->"+log_message)
        removerhandler(type,inhandler)

# logger可以看做是一个记录日志的人，对于记录的每个日志，他需要有一套规则，比如记录的格式（formatter），
# 等级（level）等等，这个规则就是handler。使用logger.addHandler(handler)添加多个规则，
# 就可以让一个logger记录多个日志。



# if __name__=="__main__":
#     # MyLog.debug("This is debug message")
#     for i in range(1,200):
#         MyLog.info("This is info message")
#     # MyLog.warning("This is warning message")
#     # MyLog.error("This is error message")
#     # MyLog.critical("This is critical message")