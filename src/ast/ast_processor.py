import os
import re

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from pprint import pformat


class AstProcessor:

    def __init__(self, logging, listener):
        self.logging = logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.listener = listener
        self.Zhushi = []

    # ★ Point 2
    def execute(self, input_source, target):
        print('1')
        parser = JavaParser(CommonTokenStream(JavaLexer(FileStream(input_source, encoding="utf-8"))))
        print('2')
        walker = ParseTreeWalker()
        print('3')
        walker.walk(self.listener, parser.compilationUnit())
        print('4')
        # analyse_result = pformat(self.listener.ast_info, width=160)
        analyse_result = self.listener.ast_info
        # print('target: ' + input_source)
        if target is not None:
            isExists = os.path.exists('../logs/' + target)
            if not isExists:
                os.mkdir('../logs/' + target)
            basename = os.path.basename(input_source)
            n = basename.rfind(".")
            with open('../logs/' + target + '/' + basename[:n] + '.jan', 'w', encoding='utf-8') as f:
                print(analyse_result, file=f)
            # self.logger.debug('Display all data extracted by AST. \n' + analyse_result)
            return self.listener.ast_info
        if target is None:
            basename = os.path.basename(input_source)
            n = basename.rfind(".")
            with open('../logs/' + '/' + basename[:n] + '.jan', 'w', encoding='utf-8') as f:
                print(analyse_result, file=f)
            # self.logger.debug('Display all data extracted by AST. \n' + analyse_result)
            return self.listener.ast_info

    # 单独提取注释
    def ExtractComment(self, text):
        print("RE:")
        temp = text
        x = re.compile("//[^\n]*", re.S)
        j = x.findall(temp)
        for index1 in j:
            self.Zhushi.append(index1)
        x = re.compile("/\*.*?\*/", re.S)
        j = x.findall(text)
        print(j)
        here = j[1]
        print("Here[-1] is" + here[-3])
        ReRule2 = '".*?' + "//[^\n]*" + '.*?"[^\n]*'
        ReRule = '".*?' + "/\*.*?\*/" + '.*?"'
        x = re.compile(ReRule)
        j1 = x.findall(text)
        RemoveComment = []
        for index in j1:
            zhushi = re.compile("/\*.*?\*/", re.S)
            Removetemp = zhushi.findall(index)
            for temp in Removetemp:
                RemoveComment.append(temp)

        x = re.compile(ReRule2)
        j2 = x.findall(text)
        print("j2:" + str(j2))
        for index in j2:
            zhushi = re.compile("//[^\n]*", re.S)
            Removetemp = zhushi.findall(index)
            for temp in Removetemp:
                RemoveComment.append(temp)
        print("RemoveComment" + str(RemoveComment))
        for index2 in j:
            self.Zhushi.append(index2)
        for index in RemoveComment:
            if index in self.Zhushi:
                self.Zhushi.remove(index)
        print("EndRe")
        return self.Zhushi
