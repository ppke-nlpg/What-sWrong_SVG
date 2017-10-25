#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from libwwnlp.model.nlp_instance import NLPInstance
from ioFormats.CorpusFormat import CorpusFormat


def check_eof(line):
    if len(line) == 0:
        raise EOFError
    return line


class TheBeastFormat(CorpusFormat):
    """
    Loads markov thebeast data
    This format is invented by Sebastian Reidel, the original author of What's Wrong with My NLP?
    The project homepage: https://code.google.com/archive/p/thebeast/
    There is an example input for the format in:
     https://atrium.lib.uoguelph.ca/xmlui/bitstream/handle/10214/8641/Fairholm_William_201412_Msc.pdf
    As less mentions or examples found, this code is not thoroughly tested.
    """
    def __init__(self):
        self._name = "thebeast"
        self.tokens = ""  # GUI STUFF
        self.deps = ""
        self.spans = ""

    @staticmethod
    def unquote(string):
        return string[1: len(string) - 1]

    @property
    def longName(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @staticmethod
    def extract_predicates_from_string(text):
        preds = {}
        for s in text.split(','):
            s = s.strip()
            if len(s) > 0:
                ind = s.find(':')
                if ind == -1:
                    pred, as_rest = s, s
                else:
                    pred, as_rest = s.split(':', maxsplit=1)
                preds[pred] = as_rest

        return preds

    def add_edges(self, instance, rows, token_preds, dep_preds, span_preds):
        for pred in token_preds.values():
            # add_tokens
            for row in rows:
                try:
                    instance.add_token(int(row[0])).add_property(pred, self.unquote(row[1]))
                except ValueError:
                    print("Could not load tokens from row {0} of rows {1}, skipping this row.".format(row, rows),
                          file=sys.stderr)
                    # raise RuntimeError("Could not load tokens from row {0} of rows {1}, skipping this row.".
                    #                    format(row, rows))
        # instance.consistify()
        for pred in dep_preds.values():
            # add_deps
            for row in rows:
                if len(row) == 4:
                    desc = self.unquote(row[3].replace("-BR-", "\n\t"))
                else:
                    desc = None
                instance.add_dependency(int(row[0]), int(row[1]), self.unquote(row[2]), pred, desc)
        for pred in span_preds.values():
            # add_spans
            for row in rows:
                # default len(row) == 3
                token = int(row[1])
                desc = None

                if len(row) == 2:
                    token = int(row[0])
                elif len(row) == 4:
                    desc = self.unquote(row[3].replace("-BR-", "\n\t"))

                instance.add_span(int(row[0]), token, self.unquote(row[2]), pred, desc)

    def load(self, file_name, from_sent_nr, to_sent_nr):
        with open(file_name, encoding='UTF-8') as reader:
            token_preds = self.extract_predicates_from_string(self.tokens)
            dep_preds = self.extract_predicates_from_string(self.deps)
            span_preds = self.extract_predicates_from_string(self.spans)

            instance_nr = 0
            instance = NLPInstance()
            as_token = None
            as_dep = None
            as_span = None
            result = []  # [NLPInstance]
            rows = {}  # {str: [[str]]}

            self.init_rows(rows, token_preds, span_preds, dep_preds)

            while instance_nr < to_sent_nr:
                try:
                    line = check_eof(reader.readline()).strip()
                    if line.startswith(">>"):
                        # monitor.progressed(instanceNr)
                        instance_nr += 1
                        if instance_nr > from_sent_nr and instance_nr > 1:
                            self.add_edges(instance, rows, token_preds, dep_preds, span_preds)

                            result.append(instance)
                            instance = NLPInstance()
                            rows.clear()
                            self.init_rows(rows, token_preds, span_preds, dep_preds)

                    elif line.startswith(">") and instance_nr > from_sent_nr:
                        pred = line[1:]
                        as_token = token_preds.get(pred)
                        as_dep = dep_preds.get(pred)
                        as_span = span_preds.get(pred)
                    else:
                        line = line.strip()
                        if line != "" and instance_nr > from_sent_nr:
                            row = line.split("\t")
                            if as_token is not None:
                                rows[as_token].add(row)
                            if as_dep is not None:
                                rows[as_dep].add(row)
                            if as_span is not None:
                                rows[as_span].add(row)

                except EOFError:
                    break

            self.add_edges(instance, rows, token_preds, dep_preds, span_preds)

            result.append(instance)
            return result

    @staticmethod
    def init_rows(rows, token_preds, span_preds, dep_preds):
        for pred in token_preds.values():
            rows[pred] = []
        for pred in span_preds.values():
            rows[pred] = []
        for pred in dep_preds.values():
            rows[pred] = []

    def loadProperties(self, properties, prefix):
        pass

    def saveProperties(self, properties, prefix):
        pass

    def setMonitor(self, monitor):
        pass

    def accessory(self):
        pass
