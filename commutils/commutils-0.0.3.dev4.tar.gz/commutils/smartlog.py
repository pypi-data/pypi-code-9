#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os,sys




def set_root_logger(level = logging.INFO, filename=None,filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s'):
    # filename=os.path.basename(__file__)+'.rootlog'
    logging.basicConfig( level = level, filename=None, filemode = filemode, format = format)

def clear_logger(logger):
    logger.handlers=[]

def get_logger(level = logging.WARNING,logname='mylog', console=True, filename=False,filemode='w'):
    # 创建一个logger

    if type(level) is str:
        level=level.upper()
        if level == 'DEBUG':
            level = logging.DEBUG
        elif level == 'INFO':
            level = logging.INFO
        elif level == 'WARNING':
            level = logging.WARNING
        elif level == 'ERROR':
            level = logging.ERROR
        elif level == 'CRITICAL':
            level = logging.CRITICAL

    logger = logging.getLogger(logname)
    logger.setLevel(level)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    formatter = logging.Formatter('%(levelname)s:[%(filename)s:%(lineno)s - %(funcName)20s() ]  %(message)s')

    if filename:
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(filename,mode=filemode)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if console:
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

if __name__ == '__main__':
    log=get_logger()
    # log=logging.getLogger('root')
    set_root_logger()
    log.debug("haha")