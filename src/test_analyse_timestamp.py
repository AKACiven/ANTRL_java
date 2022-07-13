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

# GMT: 格林威治时间
# UTC：标准时间
# ISO： 标准时间
# CST：北京时间
# UTC+08:00、+08:
import re

import numpy as np

# 为了实现更加精准的确认
def sigmoid(x, offset):
    return 1.0 / (1.0 + np.exp(-x+offset))

# 对活动时间进行分析 凌晨：23~7 上午：8~11 中午：12~14 下午：15~18 晚上：19~22
def analyse_mainworktime(list_t):
    # 用于统计
    tmplist = [0, 0, 0, 0, 0]
    timelist = ['凌晨', '上午', '中午', '下午', '晚上']
    for i in list_t:
        # 无标注 am pm
        if isinstance(i[0], str):
            hour = int(i[0])
            # print(hour)
            if 8 <= hour <= 11:
                tmplist[1] += 1
            if 12 <= hour <= 14:
                tmplist[2] += 1
            if 15 <= hour <= 18:
                tmplist[3] += 1
            if 19 <= hour <= 22:
                tmplist[4] += 1
            if 23 == hour or hour <= 7:
                tmplist[0] += 1
        # 有标注 am pm
        if isinstance(i[0], tuple):
            # 判断是否为PM
            hour = int(i[0][0])
            # print(hour)
            tmp = re.findall(r"(pm|PM|p\.m|P\.M)", i[0][1])
            if len(tmp):
                hour = hour + 12
            if 8 <= hour <= 11:
                tmplist[1] += 1
            if 12 <= hour <= 14:
                tmplist[2] += 1
            if 15 <= hour <= 18:
                tmplist[3] += 1
            if 19 <= hour <= 22:
                tmplist[4] += 1
            if 23 == hour or hour <= 7:
                tmplist[0] += 1
    print(tmplist)
    maxtime = max(tmplist)
    for i in [0, 1, 2, 3, 4]:
        # 若考虑到效率可以简化
        judge = 0.8
        if sigmoid(tmplist[i], 0.5 * maxtime) >= judge:
            match['main_worktime'].append(timelist[i])


match = {
    'timezone': [],
    'recordtime_hour': [],
    'main_worktime': []
}
rules_timezone = [
    r"(\+)(20|21|22|23|[0-1]*[0-9]):[0-5]*[0-9]",
    r"(\-)(20|21|22|23|[0-1]*[0-9]):[0-5]*[0-9]",
    r"(UTC\+|UTC\-)(11|10|[0-9])",
    r"(GMT\+|GMT\-)(20|21|22|23|[0-1]*[0-9])",
    r"([A-Z][A-Z][A-Z]+)", ]
rules_hour = [
    r"(20|21|22|23|[0-1]*[0-9]):[0-5]*[0-9]:[0-5]*[0-9] (am|pm|AM|PM|a\.m|p\.m|A\.M|P\.M)",
    r"(20|21|22|23|[0-1]*[0-9]):[0-5]*[0-9]:[0-5]*[0-9]\:",
    r"(20|21|22|23|[0-1]*[0-9]):[0-5]*[0-9]:[0-5]*[0-9]\.",
    r"(20|21|22|23|[0-1]*[0-9]):[0-5]*[0-9]:[0-5]*[0-9]",
    r"(20|21|22|23|[0-1]*[0-9]):[0-5]*[0-9] (am|pm|AM|PM|a\.m|p\.m|A\.M|P\.M)",
    r"(20|21|22|23|[0-1]*[0-9]):[0-5]*[0-9]", ]
# 这里需要输入的是注释内容，规则建立于提取的单条注释中只有一个时间戳的条件，按照规则优先级进行唯一匹配
code = [
    "11:11:59 a.m. +05:30",
    "12:11:59 a.m.",
    "8:11:59 PST",
    "13:11:59 UTC+10",
    "10:11:59 UTC-1",
    "13:11:59 GMT+20",
    "9:11:59 GMT-1",
    "14:11:59:120",
    "15:11:59.120",
    "3:11:59+05:30",
    "4:05:59.120-01:05",
    "5:11:59",
    "2:05 PM",
    "6:05 A.M.",
    "1:05 IST",
    "02:05", ]
# 通过正则匹配得到时区、修改时间
for i in code:
    for j in rules_hour:
        a = re.findall(j, i)
        if len(a):
            match['recordtime_hour'].append(a)
            break
b = None
for i in code:
    for j in rules_timezone:
        b = re.findall(j, i)
        if len(b):
            match['timezone'].append(b)
            break
# 分析主要工作时间，另外由于时区是一个单独的无关联属性，所以不做处理
analyse_mainworktime(match['recordtime_hour'])
print(match)
