# 通过分析文件的创建修改时间需要源文件镜像，比较难实现
# import time
# import os
#
# FileName = r"../resources/attack.py"
# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(FileName).st_ctime)))
# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(FileName).st_mtime)))
# print(time.localtime(os.stat(FileName).st_ctime).tm_year)
# print(time.localtime(os.stat(FileName).st_ctime).tm_zone)

# 所以此处需要分析的是注释的时间戳内容
# 首先分析日期的跨度

# GMT: 格林威治时间
# UTC：标准时间
# ISO： 标准时间
# CST：北京时间
# UTC+08:00、+08:
import re

match = []
code = "16:11:59+05:30  11:11:59 a.m. +05:30  11:11:59 PST"
print(type(code))
a = re.findall(r"(?<![\+|\-])(20|21|22|23|[0-1][0-9]):[0-5]\d[:[0-5]\d]*.*(a\.m\.)|(am)|(p\.m\.)|(pm)|(A\.M\.)|(AM)|(P\.M\.)|(PM)", code)
print(a)
# if a:
#     match.append(a)
# print(match)