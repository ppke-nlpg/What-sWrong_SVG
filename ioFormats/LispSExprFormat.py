#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.model.nlp_instance import NLPInstance
from ioFormats.CorpusFormat import CorpusFormat


def check_eof(line):
    if len(line) == 0:
        raise EOFError
    return line


class Tree:
    def __init__(self, label: str):
        self.children = []
        self.label = label

    def __str__(self):
        return '{0}{1}'.format(self.label, self.children)

    def write_spans(self, label_type: str, tag_type: str, instance: NLPInstance):
        if self.is_tag():
            span_type = tag_type
        else:
            span_type = label_type
        instance.add_span(self.get_from(), self.get_to(), self.label, span_type)
        for tree in self.children:
            tree.write_spans(label_type, tag_type, instance)

    def write_tokens(self, word_type: str, tag_type: str, instance: NLPInstance):
        for tree in self.children:
            tree.write_tokens(word_type, tag_type, instance)

    # process from "(S ..." to closing "...)"
    @staticmethod
    def consume(tree, sexpr: str):
        stack = [tree]
        token = 0
        i = 0
        while i < len(sexpr):
            if sexpr[i] == '(':
                whitespace = sexpr.find(' ', i + 1)
                open_bracket = sexpr.find('(', i + 1)
                # label_end = whitespace
                # print("whitespace = " + whitespace)
                # print("open_bracket = " + open_bracket)
                if open_bracket != -1 and open_bracket < whitespace:
                    label_end = open_bracket
                else:
                    label_end = whitespace
                label = sexpr[i + 1: label_end]
                parent = Tree(label)
                stack[-1].children.append(parent)
                stack.append(parent)
                i = label_end
                if label_end == whitespace:
                    i += 1
            elif sexpr[i] == ')':
                stack.pop()
                i += 1
            elif sexpr[i] == ' ':
                i += 1
            else:
                word_end = sexpr.find(')', i)
                word = sexpr[i: word_end]
                stack.pop().children.append(Terminal(word, token))
                token += 1
                i = word_end + 1

    def get_from(self):
        return self.children[0].get_from()

    def get_to(self):
        return self.children[len(self.children) - 1].get_to()

    @staticmethod
    def is_terminal():
        return False

    def is_tag(self):
        return self.children[0].is_terminal()


class Terminal(Tree):
    def __init__(self, label: str, index: int):
        super().__init__(label)
        self.index = index

    def is_tag(self):
        return False

    def __str__(self):
        return self.label

    @staticmethod
    def is_terminal():
        return True

    def get_from(self):
        return self.index

    def get_to(self):
        return self.index

    def write_tokens(self, word_type: str, tag_type: str, instance: NLPInstance):
        instance.add_token().add_property(word_type, self.label).add_property("Index", str(self.index))

    def write_spans(self, label_type: str, tag_type: str, instance: NLPInstance):
        pass


class LispSExprFormat(CorpusFormat):
    def __init__(self):
        self._name = "Lisp S-Expression"
        self.word = "Word"    # Word .sexpr.word
        self.tag = "pos"     # Tag .sexpr.tag
        self.phrase = "phrase"  # Phrase .sexpr.phrase

    @property
    def longName(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    def load(self, file_name: str, from_sent_nr, to_sent_nr):

        result = []
        instance_nr = 0
        with open(file_name, encoding='UTF-8') as reader:

            for line in reader:
                line = line.strip()
                if line != "":
                    if instance_nr >= from_sent_nr:
                        tree = Tree("[root]")
                        tree.consume(tree, line)
                        tree = tree.children[0]
                        instance = NLPInstance()
                        tree.write_tokens(self.word, self.tag, instance)
                        tree.write_spans(self.phrase, self.tag, instance)
                        result.append(instance)

                    instance_nr += 1
                    if instance_nr >= to_sent_nr:
                        break

        return result

    def loadProperties(self, properties, prefix):
        pass

    def saveProperties(self, properties, prefix):
        pass

    def setMonitor(self, monitor):
        pass

    def accessory(self):
        pass
