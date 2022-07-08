import logging.config
import os
from sys import path

from ast_processor import AstProcessor
from basic_info_listener import BasicInfoListener


if __name__ == '__main__':
    logging_setting_path = '../resources/logging/utiltools_log.conf'
    logging.config.fileConfig(logging_setting_path)
    logger = logging.getLogger("logs_test")

    # target_file_path = '../code/test.java'

    fp = r"../code"  # 目标文件夹
    with os.scandir(fp) as it:
        for i in it:
            print(i.path)
            if i.is_file():
                print("**** analysing " + i.path)
                ast_info = AstProcessor(logging, BasicInfoListener()).execute(i.path, None)
            if i.is_dir():
                print("**** folder " + i.name)
                fq = r"../code/" + i.name
                with os.scandir(fq) as jt:
                    for j in jt:
                        print("**** analysing " + j.path)
                        ast_info = AstProcessor(logging, BasicInfoListener()).execute(j.path, i.name)

    # ast_info = AstProcessor(logging, BasicInfoListener()).execute(target_file_path)