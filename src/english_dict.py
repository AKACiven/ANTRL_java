import re
filename = "../resources/english_dic.txt"
string = open(filename, encoding="UTF-8").read()
dic_formed = {}
dic_words = []
a = re.findall(r"([a-zA-Z]+)  \[.*?\] (\【[0-9]\】)?(★+)", string)
# print(a)
for i in a:
    # print(i[0])
    axis = {i[0]: i[2]}
    dic_formed.update(axis)
    dic_words.append(i[0])
print(type(dic_formed))
# print(dic_formed['a'])
with open('../resources/engdict_formed.txt', 'w', encoding='utf-8') as f:
    print(dic_formed, file=f)
with open('../resources/engdict_words.txt', 'w', encoding='utf-8') as f1:
    print(dic_words, file=f1)
