# maven：判断有无文件pom.xml
# idea：判断有无文件夹.idea
# gradle：有无文件build.gradle
# springboot： 文件pom.xml中有无spring-boot-starter-parent
# 这一块可能需要有经验的人士，需要 工具-特征-用途 三个方面的信息（否则水太深把握不住）
import os
import re
from os import path

# 这里粗略判断有无使用项目管理工具
tool_usage = {
    'tools_use': [],
    'tool_pom_avgversion': 0,
}
tools_use = []
matchlist = ['pom.xml', '.idea', 'build.gradle']
pairlist = {
    'pom.xml': 'maven',
    '.idea': 'jetbrain_ide',
    'build.gradle': 'gradle'
}

# 获得pom.xml中平均使用的version,只对大版本进行统计
def analyse_pom(file_content):
    in_tools = re.findall(r"\<version\>([0-9]+)\.", file_content)
    avg_version = 0
    times = len(in_tools)
    for i in in_tools:
        avg_version += int(i)
    avg_version = avg_version / times
    tool_usage['tool_pom_avgversion'] = avg_version

# 对文件名和文件夹名进行分析
def scaner_file(url):
    file = os.listdir(url)
    for f in file:
        dir_file = path.join(url, f)
        # 如果是文件，则输出文件名
        if path.isfile(dir_file):
            for i in matchlist:
                if path.basename(dir_file) == i:
                    tools_use.append(pairlist[i])
            # 下面是匹配到相应文件时的分支，这里需要进行通用化拓展
            if path.basename(dir_file) == 'pom.xml':
                fp = open(dir_file, 'r')
                file_content = fp.read()
                analyse_pom(file_content)
                fp.close()

        # 如果是目录，则是递归调用函数 scaner_file
        elif path.isdir(dir_file):
            for i in matchlist:
                if f == i:
                    tools_use.append(pairlist[i])
            scaner_file(dir_file)
        else:
            pass

# 这里输入项目文件夹
scaner_file("D:\\Dev\\civen_StuManager")
tool_usage['tools_use'] = tools_use
print(tool_usage)