import difflib
import json
import os
import re

jsondata = {}

# 这里变动的话还有一个地方需要改
extract_info = {
    'definition': [],
    'english_level': 0.0,
    'words_precision_range': 0.0,
    'english_usage': 0.0
}
# 判读用词准确程度(0~1.0)，这里我们将精准匹配和模糊匹配求比例，考虑到精准匹配要求严格，所以乘以一个系数适度扩大
def analyse_precision(precise, diff):
    range3 = (precise * 1.5) / diff
    if range3 > 1.0:
        range3 = 1
    extract_info['words_precision_range'] = range3

# 判断是否经常接触英语，通过分析模糊匹配成功比例
def analyse_englishusage(use, whole):
    extract_info['english_usage'] = use / whole

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
    range1 = 0
    times1 = 0
    # print(namelist)
    for name in namelist:
        # 大小写敏感匹配
        star = dict.get(name)
        if star is not None and rank[star] > range1:
            times1 += 1
            range1 = rank[star]

    dict_w_fp = open('../resources/engdict_words.txt', 'r', encoding='utf-8')
    dict_w = eval(dict_w_fp.read())
    range2 = 0
    times2 = 0
    for name in namelist:
        # 模糊匹配，此处精确系数设置的较高，且匹配结果只一个
        match = difflib.get_close_matches(name, dict_w, 1, cutoff=0.9)
        if len(match):
            times2 += 1
            star = dict.get(match[0])
            if star is not None and rank[star] > range2:
                range2 = rank[star]
    # print(range2)

    # 此处设置大小写敏感匹配和模糊匹配的权重，rank越高词汇等级越高
    extract_info['english_level'] = range1 * 0.5 + range2 * 0.5
    dict_fp.close()
    dict_w_fp.close()
    # 分析用词精准程度
    analyse_precision(times1, times2)
    # 分析经常使用英语
    analyse_englishusage(times2, len(namelist))

# 提取所有函数、变量的name，并交给analyse_englevel函数分析
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
# append 获取匹配词汇对应的等级（0~5），这里只对能够精确匹配的单词进行分析。因为模糊匹配误差过大，暂时不考虑。只根据最罕见的单词进行评级
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
