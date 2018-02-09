#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file implements TabFormat and all classes inherited from it: TabFormat, CoNLL2000, CoNLL2002, CoNLL2003,
#  CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, CoNLL2009 CoNLL2009, Malt-TAB and CCG classes...

import sys

from libwwnlp.model.nlp_instance import NLPInstance
from ioFormats.CorpusFormat import CorpusFormat

"""
 * A TabFormat loads data from text files where token properties are represented as white-space/tab separated values.
 * This includes formats such as the CoNLL shared task formats or the MALT-Tab format. This class represents the generic
 * framework to process such tab separated data. To implement a concrete format clients have to implement the {@link
 * TabProcessor} interface.
 *
 * A TabProcessor takes a table of string values and returns an NLPInstance. This table of string value corresponds to
 * the standard way of representing sentences in the CoNLL shared tasks as well as the MALT-Tab format for
 * dependencies.
 *
 * @author Sebastian Riedel
"""


class TabFormat(CorpusFormat):
    """
     This is a helper class that contain all common features of TabFormats corresponding to the CorpusFormat interface
    """
    def __init__(self):
        """
         * @see TabProcessor#_supports_open()
         * Does this processor support loading of open datasets (as in 'CoNLL Open Track').
         *
         * @return true iff the processor supports loading of open datasets.
        """
        super().__init__()
        self._support_open = False

    def load(self, file_name: str, from_sent_nr: int, to_sent_nr: int):
        result = self._load_tabs(file_name, from_sent_nr, to_sent_nr, self.create)

        if self._support_open:
            file_name_open = file_name[0:file_name.rfind('.')] + '.open'
            open_corpus = self._load_tabs(file_name_open, from_sent_nr, to_sent_nr, self.create_open)
            for i, oc_elem in enumerate(open_corpus):
                result[i].merge(oc_elem)

        return result

    @staticmethod
    def _load_tabs(file_name, from_sent_nr: int, to_sent_nr: int, open_fun):
        corpus = []
        rows = []
        instance_nr = 0
        with open(file_name, encoding='UTF-8') as reader:
            for line in reader:
                if instance_nr >= to_sent_nr:
                    break
                line = line.strip()
                if line == '' or line.split()[0] == '<\s>':
                    instance_nr += 1
                    if instance_nr > from_sent_nr:
                        instance = open_fun(rows)
                        corpus.append(instance)
                        rows.clear()
                else:
                    if instance_nr >= from_sent_nr:
                        rows.append(line.split())

            if len(rows) > 0:
                corpus.append(open_fun(rows))

        return corpus

    @staticmethod
    def create_open(_):
        """
         * @see TabProcessor#create_open(List<? extends List<String>>)
         * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from
         * the open dataset.
         *
         * @param rows the rows that represent the column separated values in Tab format files.
         * @return an NLPInstance that represents the given rows.
        """
        return None

    def create(self, rows):
        """
         * @see TabProcessor#create(List<? extends List<String>>)
         * Create an NLPInstance from the given table (list of rows) of strings.
         *
         * @param rows the rows that represent the column separated values in Tab format files.
         * @return an NLPInstance that represents the given rows.
        """
        raise NotImplementedError


# ----------------------------------------------------------------------------------------------------------------------

class CoNLL2000(TabFormat):
    """
     * Loads CoNLL 2000 chunk data.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CoNLL 2000'

    def create(self, rows):
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name='Word', value=row[0]).\
                add_property(name='Index', value=str(index))

            instance.add_span(index, index, row[1], 'pos')
            instance.add_span(index, index, row[2], 'chunk (BIO)')

        self._extract_span00_02(rows=rows, column=2, field_type='chunk', instance=instance)

        return instance

    @staticmethod
    def _extract_span00_02(rows: list, column: int, field_type: str, instance: NLPInstance):
        in_chunk = False
        begin = 0
        current_chunk = ''
        for index, row in enumerate(rows):
            chunk = row[column]
            minus = chunk.find('-')
            if minus != -1:
                bio = chunk[0:minus]
                label = chunk[minus+1:]
                if 'B' == bio:
                    if in_chunk:
                        instance.add_span(begin, index - 1, current_chunk, field_type)
                    begin = index
                    current_chunk = label
                    in_chunk = True
            elif in_chunk:
                    instance.add_span(begin, index - 1, current_chunk, field_type)
                    in_chunk = False

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2002(CoNLL2000):
    """
     * Loads CoNLL 2002 NER data.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CoNLL 2002'

    def create(self, rows):
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name='Word', value=row[0]).\
                add_property(name='Index', value=str(index))

            instance.add_span(index, index, row[1], 'ner (BIO)')

        self._extract_span00_02(rows=rows, column=1, field_type='ner', instance=instance)

        return instance

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2003(TabFormat):
    """
     * Loads CoNLL 2003 chunk and NER data.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CoNLL 2003'

    def create(self, rows):
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name='Word', value=row[0]).\
                add_property(name='Index', value=str(index))

            instance.add_span(index, index, row[1], 'pos')
            instance.add_span(index, index, row[2], 'chunk (BIO')
            instance.add_span(index, index, row[3], 'ner (BIO)')

        self._extract_span03(rows=rows, column=2, field_type='chunk', instance=instance)
        self._extract_span03(rows=rows, column=3, field_type='ner', instance=instance)

        return instance

    @staticmethod
    def _extract_span03(rows: list, column: int, field_type: str, instance: NLPInstance):
        in_chunk = False
        begin = 0
        current_chunk = ''
        index = 0
        for index, row in enumerate(rows):
            chunk = row[column]
            minus = chunk.find('-')
            if minus != -1:
                bio = chunk[0:minus]
                label = chunk[minus+1:]
                if in_chunk:
                    # start a new chunk and finish old one
                    if 'B' == bio or 'I' == bio and label != current_chunk:
                        instance.add_span(begin, index - 1, current_chunk, field_type)
                        begin = index
                        current_chunk = label
                else:
                    in_chunk = True
                    begin = index
                    current_chunk = label
            elif in_chunk:
                    instance.add_span(begin, index - 1, current_chunk, field_type)
                    in_chunk = False
        if in_chunk:
            instance.add_span(begin, index - 1, current_chunk, field_type)

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2004(TabFormat):
    """
     * Loads CoNLL 2004 SRL data.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CoNLL 2004'

    def create(self, rows):
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name='Word', value=row[0]).\
                add_property(name='Index', value=str(index))

        predicate_count = 0
        for index, row in enumerate(rows):
            if row[1] != '-':
                sense = row[1]
                instance.add_span(index, index, sense, 'sense')

                self._extract_span04_05(rows, 2 + predicate_count, 'role', sense + ':', instance)

                predicate_count += 1
        return instance

    @staticmethod
    def _extract_span04_05(rows: list, column: int, field_type: str, prefix: str, instance: NLPInstance):
        begin = 0
        current_chunk = ''
        for index, row in enumerate(rows):
            chunk = row[column]
            if chunk.startswith('('):
                end = chunk.index('*')  # To get ValueError when not found instead of find's -1
                current_chunk = chunk[1:end]
                begin = index
            if chunk.endswith(')'):
                instance.add_span(begin, index, prefix + current_chunk, field_type)

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2005(CoNLL2004):
    """
     * Loads CoNLL 2005 SRL data.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CoNLL 2005'

    def create(self, rows):
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name='Word', value=row[0]).\
                add_property(name='Index', value=str(index))

        predicate_count = 0
        for index, row in enumerate(rows):
            try:
                if row[9] != '-':
                    sense = row[10] + '.' + row[9]
                    instance.add_span(index, index, sense, 'sense')

                    self._extract_span04_05(rows, 11 + predicate_count, 'role', sense + ':', instance)

                    predicate_count += 1
            except IndexError:
                print('Can\'t parse file: not enough (10) column in row {0}'.format(row), file=sys.stderr)
                sys.exit(1)

        return instance

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2006(TabFormat):
    """
     * Loads CoNLL 2006 Dependency data.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CoNLL 2006'

    def create(self, rows):
        instance = NLPInstance()
        instance.add_token().add_property('Word', '-Root-')
        for row in rows:
            instance.add_token().\
                add_property(name='Word', value=row[1]).\
                add_property(name='Index', value=row[0]).\
                add_property(name='Lemma', value=row[2]).\
                add_property(name='CPos', value=row[3]).\
                add_property(name='Pos', value=row[4]).\
                add_property(name='Feats', value=row[5])

        for row in rows:
            # dependency
            mod = int(row[0])
            try:
                instance.add_dependency(start=int(row[6]), end=mod, label=row[7], edge_type='dep')
            except (ValueError, IndexError, KeyError):
                print('Can\'t parse dependency', file=sys.stderr)
                instance.tokens[mod].add_property('DepMissing', 'missing')
            # role
        return instance

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2008(TabFormat):
    """
     * Loads CoNLL 2008 Joint SRL and Dependency data.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CoNLL 2008'
        self._supports_open = True

    def create(self, rows):
        instance = NLPInstance()
        instance.add_token().add_property('Word', '-Root-')
        predicates = []  # ArrayList<Integer>()
        for row in rows:
            instance.add_token().\
                add_property(name='Word', value=row[1]).\
                add_property(name='Index', value=row[0]).\
                add_property(name='Lemma', value=row[2]).\
                add_property(name='Pos', value=row[3]).\
                add_property(name='Split Form', value=row[5]).\
                add_property(name='Split Lemma', value=row[6]).\
                add_property(name='Split PoS', value=row[7])
            if row[10] != '_':
                index = int(row[0])
                predicates.append(index)
                instance.add_span(index, index, row[10], 'sense')

        for row in rows:
            # dependency
            if row[8] != '_':
                instance.add_dependency(int(row[8]), int(row[0]), row[9], 'dep')
            # role
            for col in range(11, len(row)):
                label = row[col]
                if label != '_':
                    pred = predicates[col-11]
                    arg = int(row[0])
                    # if arg != pred
                    instance.add_edge(start=pred, end=arg, label=label, edge_type='role')
        return instance

    @staticmethod
    def create_open(rows):
        instance = NLPInstance()
        instance.add_token()
        for row in rows:
            instance.add_token(). \
                add_property('Named Entity', row[0], 10). \
                add_property('NamedEntity BBN', row[1], 11). \
                add_property('WordNet', row[2], 12)

        index = 1
        for index, row in enumerate(rows, start=1):
            # dependency
            instance.add_edge(start=int(row[3]), end=index, label=row[4], edge_type='malt')
        return index

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2009(TabFormat):
    """
     * Loads CoNLL 2009 Joint SRL and Dependency data.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CoNLL 2009'

    def create(self, rows):
        instance = NLPInstance()
        instance.add_token().add_property(name='Word', value='-Root-')
        predicates = []
        for row in rows:
            instance.add_token().\
                add_property(name='Word', value=row[1]).\
                add_property(name='Index', value=row[0]).\
                add_property(name='Lemma', value=row[2]).\
                add_property(name='PLemma', value=row[3]).\
                add_property(name='PoS', value=row[4]).\
                add_property(name='PPoS', value=row[5]).\
                add_property(name='Feat', value=row[6]).\
                add_property(name='PFeat', value=row[7])
            if row[13] != '_':
                index = int(row[0])
                predicates.append(index)
                instance.add_span(index, index, row[13], 'sense')

        for row in rows:
            # dependency
            if row[8] != '_':
                instance.add_dependency(start=int(row[8]), end=int(row[0]), label=row[10], edge_type='dep')
            if row[9] != '_':
                instance.add_dependency(start=int(row[9]), end=int(row[0]), label=row[11], edge_type='pdep')
            # role
            for col in range(14, len(row)):
                label = row[col]
                if label != '_':
                    pred = predicates[col-14]
                    arg = int(row[0])
                    # if arg != pred:
                    instance.add_dependency(start=pred, end=arg, label=label, edge_type='role')
        return instance

# ----------------------------------------------------------------------------------------------------------------------


class MaltTab(TabFormat):
    """
     * Loads Malt-TAB dependencies.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Malt-TAB'

    def create(self, rows):
        instance = NLPInstance()
        instance.add_token().add_property(name='Word', value='-Root-')
        for index, row in enumerate(rows, start=1):
            instance.add_token().\
                add_property(name='Word', value=row[0]).\
                add_property(name='Index', value=str(index)).\
                add_property(name='Pos', value=row[1])

        for mod, row in enumerate(rows, start=1):
            # dependency
            try:
                instance.add_dependency(start=int(row[2]), end=mod, label=row[3], edge_type='dep')
            except (ValueError, IndexError, KeyError):
                print('Can\'t parse dependency', file=sys.stderr)
                instance.tokens[mod].add_property('DepMissing', 'missing')  # role
        return instance

# ----------------------------------------------------------------------------------------------------------------------


class CCG(TabFormat):
    """
     * Loads CCG dependencies.
    """

    def __init__(self):
        super().__init__()
        self.name = 'CCG'

    def create(self, rows):
        instance = NLPInstance()
        sentence = rows[0]
        # Skip <s> and dep count
        for i in range(2, len(sentence)):
            w_t_c = sentence[i].split('|')
            instance.add_token().\
                add_property(name='Word', value=w_t_c[0]).\
                add_property(name='Tag', value=w_t_c[1]).\
                add_property(name='Category', value=w_t_c[2]).\
                add_property(name='Index', value=str(i - 1))
        # instance.add_token().add_property('Word', '-Root-')

        mod = 1
        for row in rows:
            if row[0] != '<s>' and row[0] != '<\s>':
                # dependency
                try:
                    instance.add_dependency(start=int(row[1]), end=int(row[0]), label=row[2] + '_' + row[3],
                                            edge_type='dep')
                except (ValueError, IndexError, KeyError):
                    print('Can\'t parse dependency', file=sys.stderr)
                    instance.tokens[mod].add_property('DepMissing', 'missing')
                mod += 1
        return instance
