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
        parser = JavaParser(CommonTokenStream(JavaLexer(FileStream(input_source, encoding="utf-8"))))
        walker = ParseTreeWalker()
        walker.walk(self.listener, parser.compilationUnit())
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
