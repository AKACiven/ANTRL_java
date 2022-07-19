import re

# 由于sdk版本型号过多且不具备普适性，这里我们只分析jdk
# 这里需要的是没有注释的裸代码
filename = "../code/bob/test2.java"
# 这里用配置文件当然更好了，以后再实现吧
jdkusage = {
    'newusage_num': 0,
    'newusage': [],
    'abandonusage_num': 0,
    'abandonusage': [],
    'safety_concern': 0
}
rules = [r"\-\>",
         r"\.stream",
         r"Instant\.",
         r"LocalDate\.",
         r"LocalTime\.",
         r"LocalDateTime\.",
         r"ZonedDateTime\.",
         r"Period\.",
         r"ZoneOffset\.",
         r"Clock\.",
         r"Optional\.",
         r"var",
         r"copyOf\(",
         r"ByteArrayOutputStream\(",
         r"\.transferTo",
         r"\.isBlank",
         r"\.strip",
         r"\.stripTrailing",
         r"\.stripLeading",
         r"\.repeat",
         r"Pack200\.",
         r"\"\"\"",
         r"\@\S+\n\@\S+\n"]
rules_abandon = [
    r"com\.sun\.awt\.AWTUtilities",
    r"sun\.misc\.Unsafe\.defineClass",
    r"Thread\.destroy",
    r"Thread\.stop",
    r"jdk\.snmp"
]
rules_safety = [
    r"public final",
    r"private final",
    r"SecurityManager",
    r"synchronized",
    r"volatile",
    r"ReentrantLock"
]
code_fp = open(filename, encoding="UTF-8")
code = code_fp.read()
# 这里匹配jdk8之后的
match = []
matchtimes = 0
for i in rules:
    a = re.findall(i, code)
    if a:
        matchtimes += 1
        match.append(a[0])
jdkusage['newusage'] = match
jdkusage['newusage_num'] = matchtimes

# 这里匹配jdk8之后被废除的
match = []
matchtimes = 0
for i in rules_abandon:
    a = re.findall(i, code)
    if a:
        matchtimes += 1
        match.append(a[0])
jdkusage['abandonusage'] = match
jdkusage['abandonusage_num'] = matchtimes

# 这里匹配是有安全用法的次数
match = []
matchtimes = 0
for i in rules_safety:
    a = re.findall(i, code)
    if a:
        matchtimes += 1
jdkusage['safety_concern'] = matchtimes
# 这里将java jdk8以及之后的常用版本特性打印
print(jdkusage)
code_fp.close()

