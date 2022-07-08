import json
import os
import re

jsondata = {'packageName': '', 'className': 'HelloWorld', 'implements': [], 'extends': '', 'imports': [],
            'fields': [{'fieldType': 'var', 'fieldDefinition': 'm'}], 'methods': [
        {'returnType': 'void', 'methodName': 'main', 'params': [{'paramType': 'String[]', 'paramName': 'args'}],
         'callMethods': ['8 19 System.out.println("Hello World")'],
         'methodBody': '{System.out.println("Hello World");vari=1;charkkk=4;intk=2;}',
         'methodvars': [{'varType': 'var', 'varDefinition': 'i'}, {'varType': 'char', 'varDefinition': 'kkk'},
                        {'varType': 'int', 'varDefinition': 'k'}]},
        {'returnType': 'void', 'methodName': 'jjj', 'params': [{'paramType': 'String[]', 'paramName': 'args'}],
         'callMethods': ['14 19 System.out.println("Hello World")'],
         'methodBody': '{System.out.println("Hello World");varl=1;intaaaa=2;}',
         'methodvars': [{'varType': 'var', 'varDefinition': 'l'}, {'varType': 'int', 'varDefinition': 'aaaa'}]}]}

# 这里变动的话还有一个地方需要改
extract_info = {
    'definition': [],
    'english_level': 0.0
}

# 获取匹配词汇对应的等级（0~5.0）
def analyse_englevel(namelist):
    rank = {
        '★': 5,
        '★★': 4,
        '★★★': 3,
        '★★★★': 2,
        '★★★★★': 1,
        None: 0
    }
    dict_fp = open('../resources/engdict_formed.txt', 'r', encoding='utf-8')
    dict = eval(dict_fp.read())
    range = 0
    times = 0
    print(namelist)
    for name in namelist:
        star = dict.get(name)
        if star is not None:
            times += 1
            range += rank[star]
    dict_fp.close()
    if times != 0:
        extract_info['english_level'] = range / times

# 提取所有函数、变量的name，并分析
def analyse_definition(jsondata):
    namelist = []
    fields = jsondata['fields']
    for data in fields:
        namelist.append(data['fieldDefinition'])
    methods = jsondata["methods"]
    for data in methods:
        namelist.append(data['methodName'])
        methodvars = data['methodvars']
        for data2 in methodvars:
            namelist.append(data2['varDefinition'])
        methodvars = data['params']
        for data2 in methodvars:
            namelist.append(data2['paramName'])
    # print(namelist)
    extract_info['definition'] = namelist
    analyse_englevel(namelist)

# 从提取到的代码基础特征，针对需要分析的内容进一步细化提取
# details 每次遍历都会重写分析输出文件
# update 能够对目录下文件进行遍历处理
# append 提取所有函数、变量的name
# append 获取匹配词汇对应的等级（0~5），这里只对能够精确匹配的单词进行分析，模糊匹配误差过大
if __name__ == '__main__':

    fp = r"../logs"  # 目标文件夹
    with os.scandir(fp) as it:
        for i in it:
            print(i.path)
            if i.is_dir():
                print("**** folder " + i.name)
                # 总目录
                fq = r"../logs/" + i.name
                isExists = os.path.exists('../extracts/' + i.name)
                if not isExists:
                    os.mkdir('../extracts/' + i.name)
                with os.scandir(fq) as jt:
                    for j in jt:
                        extract_info = {
                            'definition': [],
                            'english_level': 0.0
                        }

                        print("**** extracting " + j.path)
                        # 清除文本内容
                        file_name = os.path.basename(j.path).split('.')[0]
                        out_file = "../extracts/" + i.name + "/" + file_name + ".ext"
                        in_file = "../logs/" + i.name + "/" + file_name + ".jan"
                        extract_fp = open(out_file, "w", encoding='utf-8')
                        extract_fp.close()

                        extract_fp = open(out_file, "a", encoding='utf-8')
                        in_file_fp = open(in_file, "r")
                        load_json = eval(in_file_fp.read())
                        # print(type(load_json))
                        # print(type(jsondata))

                        # # 先提取所有函数、变量的name，后立即对分析得到的数据判断英语等级
                        analyse_definition(load_json)

                        print("outputfile" + out_file)
                        print(extract_info, file=extract_fp)

                        in_file_fp.close()
                        extract_fp.close()
