import re

# 这里需要的是没有注释的裸代码
filename = "../code/bob/test2.java"
rules = [r"\-\>", r"\.stream", r"Instant\.", r"LocalDate\.", r"LocalTime\.", r"LocalDateTime\.", r"ZonedDateTime\.", r"Period\.", r"ZoneOffset\.", r"Clock\.", r"Optional\.", r"var", r"copyOf\(", r"ByteArrayOutputStream\(", r"\.transferTo", r"\.isBlank", r"\.strip", r"\.stripTrailing", r"\.stripLeading", r"\.repeat", r"Pack200\.", r"\"\"\"", r"\@\S+\n\@\S+\n"]
code = open(filename, encoding="UTF-8").read()
match = []
for i in rules:
    a = re.findall(i, code)
    if a:
        match.append(a[0])
print(match)
