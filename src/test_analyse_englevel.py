import difflib

rank = {
        '★': 5,
        '★★': 4,
        '★★★': 3,
        '★★★★': 2,
        '★★★★★': 1,
        None: 0
    }
namelist = ['str', 'hello', 'description', 'main', 'creditCardNumber', 'socialSecurityNumber', 'pi', 'hexBytes', 'hexWords', 'maxLong', 'nybbles', 'bytes', 'lastReceivedMessageId', 'hexDouble1', 'hexDouble2', 'octal', 'hexUpper', 'hexLower', 'x1', 'x2', 'x4', 'x7', 'x9', 'x10', 'x,y,result', 'ok', 'not_ok', 'f', 'args', 'methodCalls', 'strings', 'foo', 'main', 'random', 'args', 'main', 'a', 'b', 'minVal', 'i', 'i', 'i', 'i', 'ch', 'strChars', 'result', 'numbers', 'x', 'numbers', 'numbers2', 'numbers', 'numbers2', 'numbers', 'args', 'inner_class_constructor', 'foo', 'fooBar1', 'fooBar2', 'bar', 'bar', 'go', 'bar', 'a', 'b', 'bar', 'a', 'openStream', 'printReport', 'header', '...', 'doSomething', 'doSomething', 'hello', 'main', 'nc', 'args', 'getDescription', 'getDescription', 'getDescription', 'getDescription', 'getDescription', 'actionSelected', 'action', 'requestReceived', 'dummy', 'listener', 'dummy', 'openOutputStream', 'travelToJupiter', 'add', 'mapper', 'mapper', 'array', 'item', 'contains', 'item', 'arr', 'addItem', 'item', 'addItem', 'item', 'fn1', 'Bar<T>', 'fn2', 'Bar<T>', 'fn3', 'Bar<T>', 'main', 'args']

dict_fp = open('../resources/engdict_formed.txt', 'r', encoding='utf-8')
dict = eval(dict_fp.read())
dict_w_fp = open('../resources/engdict_words.txt', 'r', encoding='utf-8')
dict_w = eval(dict_w_fp.read())
range = 0
times = 0
for name in namelist:
    match = difflib.get_close_matches(name, dict_w, 1, cutoff=0.9)
    if len(match):
        times += 1
        star = dict.get(name)
        range += rank[star]
print(range / times)