#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file implements TabFormat and all classes inherited from it: TabFormat, CoNLL2000, CoNLL2002, CoNLL2003,
#  CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, CoNLL2009 CoNLL2009, Malt-TAB and CCG classes...
# TabProcessor interface class is omited...

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

# TODO: This class is not used currently


class TabFormat(CorpusFormat):

    def __init__(self, MainWindow):

        self._name = "TAB-separated"
        self._monitor = None
        self._processors = {}  # TreeMap<String, TabProcessor>()

        self.add_processor(name="CCG", processor=CCG())
        self.add_processor(name="CoNLL 2009", processor=CoNLL2009())
        self.add_processor(name="CoNLL 2008", processor=CoNLL2008())
        self.add_processor(name="CoNLL 2006", processor=CoNLL2006())
        self.add_processor(name="CoNLL 2005", processor=CoNLL2005())
        self.add_processor(name="CoNLL 2004", processor=CoNLL2004())
        self.add_processor(name="CoNLL 2002", processor=CoNLL2002())
        self.add_processor(name="CoNLL 2003", processor=CoNLL2003())
        self.add_processor(name="CoNLL 2000", processor=CoNLL2000())
        self.add_processor(name="MaltTab", processor=MaltTab())

        # TODO: grafikus rész

        self._accessory = MainWindow
        self._type = MainWindow
        self._open = MainWindow

    @property
    def accessory(self):
        pass

    @accessory.setter
    def accessory(self, value):
        pass

    @property
    def processors(self):
        return self._processors

    @processors.setter
    def processors(self, value):
        self._processors = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value  # TODO: JComboBox

    @property
    def open(self):
        return self._open

    @open.setter
    def open(self, value):
        self._open = value  # TODO: JCheckBox

    def add_processor(self, processor, name: str=None):
        if name is not None:
            self._processors[name] = processor
        else:
            self._processors[str(processor)] = processor

    @property
    def name(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def longName(self):
        #  TODO: type
        return self._name + "(" + str(self._type.getSelectedItem()) + ")"

    def setMonitor(self, monitor):
        pass

    def loadProperties(self, properties, prefix: str):
        pass

    def saveProperties(self, properties, prefix: str):
        pass

    def load(self, file, start: int, to: int):
        processor = self._type.getSelectedItem()  # TODO grafika
        result = self.load_tabs(file, start, to, processor, False)
        if self._open.isSelected():
            filename = file.name[0:file.name.rfind('.')] + ".open"
            open_file = open(filename)
            open_corpus = self.load_tabs(open_file, start, to, processor, True)
            for i in range(0, len(open_corpus)):
                result[i].merge(open_corpus[i])
        return result

    def load_tabs(self, file, start: int, to: int, processor, can_open: bool):
        corpus = []
        rows = []
        instnce_nr = 0
        for line in file:
            if instnce_nr >= to:
                break
            line = line.strip()
            if line == "" or line.split()[0] == '<\s>':
                self._monitor.progressed(instnce_nr)
                instnce_nr += 1
                if instnce_nr <= start:
                    continue
                if can_open:
                    instance = processor.create_open(rows)
                else:
                    instance = processor.create(rows)
                corpus.append(instance)
                rows.clear()
            else:
                if instnce_nr < start:
                    continue
                rows.append(line.split())
        if len(rows) > 0:
            if can_open:
                corpus.append(processor.create_open(rows))
            else:
                corpus.append(processor.create(rows))
        return corpus

# ----------------------------------------------------------------------------------------------------------------------


class AbstractCoNLLFormat:
    def __init__(self):
        self._name = ""

    def __str__(self):
        """
         * Returns the name of this processor.
         *
         * @return the name of this processor.
        """
        return self._name

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

    @staticmethod
    def support_open():
        """
         * @see TabProcessor#supports_open()
         * Does this processor support loading of open datasets (as in "CoNLL Open Track").
         *
         * @return true iff the processor supports loading of open datasets.
        """
        return False

    def create(self, rows):
        """
         * @see TabProcessor#create(List<? extends List<String>>)
         * Create an NLPInstance from the given table (list of rows) of strings.
         *
         * @param rows the rows that represent the column separated values in Tab format files.
         * @return an NLPInstance that represents the given rows.
        """
        pass


class CoNLL2000(AbstractCoNLLFormat):
    """
     * Loads CoNLL 2000 chunk data.
    """

    def __init__(self):
        super().__init__()
        self._name = "CoNLL 2000"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name="Word", value=row[0]).\
                add_property(name="Index", value=str(index))

            instance.add_span(index, index, row[1], "pos")
            instance.add_span(index, index, row[2], "chunk (BIO)")

        self.extract_span00_02(rows=rows, column=2, field_type="chunk", instance=instance)

        return instance

    @staticmethod
    def extract_span00_02(rows: list, column: int, field_type: str, instance: NLPInstance):
        in_chunk = False
        begin = 0
        current_chunk = ""
        for index, row in enumerate(rows):
            chunk = row[column]
            minus = chunk.find('-')
            if minus != -1:
                bio = chunk[0:minus]
                label = chunk[minus+1:]
                if "B" == bio:
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
        self._name = "CoNLL 2002"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name="Word", value=row[0]).\
                add_property(name="Index", value=str(index))

            instance.add_span(index, index, row[1], "ner (BIO)")

        self.extract_span00_02(rows=rows, column=1, field_type="ner", instance=instance)

        return instance

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2003(AbstractCoNLLFormat):
    """
     * Loads CoNLL 2003 chunk and NER data.
    """

    def __init__(self):
        super().__init__()
        self._name = "CoNLL 2003"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name="Word", value=row[0]).\
                add_property(name="Index", value=str(index))

            instance.add_span(index, index, row[1], "pos")
            instance.add_span(index, index, row[2], "chunk (BIO")
            instance.add_span(index, index, row[3], "ner (BIO)")

        self.extract_span03(rows=rows, column=2, field_type="chunk", instance=instance)
        self.extract_span03(rows=rows, column=3, field_type="ner", instance=instance)

        return instance

    @staticmethod
    def extract_span03(rows: list, column: int, field_type: str, instance: NLPInstance):
        in_chunk = False
        begin = 0
        current_chunk = ""
        index = 0
        for index, row in enumerate(rows):
            chunk = row[column]
            minus = chunk.find('-')
            if minus != -1:
                bio = chunk[0:minus]
                label = chunk[minus+1:]
                if in_chunk:
                    # start a new chunk and finish old one
                    if "B" == bio or "I" == bio and label != current_chunk:
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


class CoNLL2004(AbstractCoNLLFormat):
    """
     * Loads CoNLL 2004 SRL data.
    """

    def __init__(self):
        super().__init__()
        self._name = "CoNLL 2004"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name="Word", value=row[0]).\
                add_property(name="Index", value=str(index))

        predicate_count = 0
        for index, row in enumerate(rows):
            if row[1] != "-":
                sense = row[1]
                instance.add_span(index, index, sense, "sense")

                self.extract_span04_05(rows, 2 + predicate_count, "role", sense + ":", instance)

                predicate_count += 1
        return instance

    @staticmethod
    def extract_span04_05(rows: list, column: int, field_type: str, prefix: str, instance: NLPInstance):
        begin = 0
        current_chunk = ""
        for index, row in enumerate(rows):
            chunk = row[column]
            if chunk.startswith("("):
                end = chunk.index("*")  # To get ValueError when not found instead of find's -1
                current_chunk = chunk[1:end]
                begin = index
            if chunk.endswith(")"):
                instance.add_span(begin, index, prefix + current_chunk, field_type)

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2005(CoNLL2004):
    """
     * Loads CoNLL 2005 SRL data.
    """

    def __init__(self):
        super().__init__()
        self._name = "CoNLL 2005"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        for index, row in enumerate(rows):
            instance.add_token().\
                add_property(name="Word", value=row[0]).\
                add_property(name="Index", value=str(index))

        predicate_count = 0
        for index, row in enumerate(rows):
            try:
                if row[9] != "-":
                    sense = row[10] + "." + row[9]
                    instance.add_span(index, index, sense, "sense")

                    self.extract_span04_05(rows, 11 + predicate_count, "role", sense + ":", instance)

                    predicate_count += 1
            except IndexError:
                print("Can't parse file: not enough (10) column in row {0}".format(row), file=sys.stderr)
                sys.exit(1)

        return instance

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2006(AbstractCoNLLFormat):
    """
     * Loads CoNLL 2006 Dependency data.
    """

    def __init__(self):
        super().__init__()
        self._name = "CoNLL 2006"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        instance.add_token().add_property("Word", "-Root-")
        for row in rows:
            instance.add_token().\
                add_property(name="Word", value=row[1]).\
                add_property(name="Index", value=row[0]).\
                add_property(name="Lemma", value=row[2]).\
                add_property(name="CPos", value=row[3]).\
                add_property(name="Pos", value=row[4]).\
                add_property(name="Feats", value=row[5])

        for row in rows:
            # dependency
            mod = int(row[0])
            try:
                instance.add_dependency(start=int(row[6]), end=mod, label=row[7], edge_type="dep")
            except (ValueError, IndexError, KeyError):
                print("Can't parse dependency", file=sys.stderr)
                instance.tokens[mod].add_property("DepMissing", "missing")
            # role
        return instance

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2008(AbstractCoNLLFormat):
    """
     * Loads CoNLL 2008 Joint SRL and Dependency data.
    """

    def __init__(self):
        super().__init__()
        self._name = "CoNLL 2008"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        instance.add_token().add_property("Word", "-Root-")
        predicates = []  # ArrayList<Integer>()
        for row in rows:
            instance.add_token().\
                add_property(name="Word", value=row[1]).\
                add_property(name="Index", value=row[0]).\
                add_property(name="Lemma", value=row[2]).\
                add_property(name="Pos", value=row[3]).\
                add_property(name="Split Form", value=row[5]).\
                add_property(name="Split Lemma", value=row(6)).\
                add_property(name="Split PoS", value=row[7])
            if row[10] != "_":
                index = int(row[0])
                predicates.append(index)
                instance.add_span(index, index, row[10], "sense")

        for row in rows:
            # dependency
            if row[8] != "_":
                instance.add_dependency(int(row[8]), int(row[0]), row[9], "dep")
            # role
            for col in range(11, len(row)):
                label = row[col]
                if label != "_":
                    pred = predicates[col-11]
                    arg = int(row[0])
                    # if arg != pred
                    instance.add_edge(start=pred, end=arg, label=label, edge_type="role")
        return instance

    @staticmethod
    def create_open(rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        instance.add_token()
        for row in rows:
            instance.add_token(). \
                add_property("Named Entity", row[0], 10). \
                add_property("NamedEntity BBN", row[1], 11). \
                add_property("WordNet", row[2], 12)

        index = 1
        for index, row in enumerate(rows, start=1):
            # dependency
            instance.add_edge(start=int(row[3]), end=index, label=row[4], edge_type="malt")
        return index

    @staticmethod
    def supports_open():
        return True

# ----------------------------------------------------------------------------------------------------------------------


class CoNLL2009(AbstractCoNLLFormat):
    """
     * Loads CoNLL 2009 Joint SRL and Dependency data.
    """

    def __init__(self):
        super().__init__()
        self._name = "CoNLL 2009"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        instance.add_token().add_property(name="Word", value="-Root-")
        predicates = []
        for row in rows:
            instance.add_token().\
                add_property(name="Word", value=row[1]).\
                add_property(name="Index", value=row[0]).\
                add_property(name="Lemma", value=row[2]).\
                add_property(name="PLemma", value=row[3]).\
                add_property(name="PoS", value=row[4]).\
                add_property(name="PPoS", value=row[5]).\
                add_property(name="Feat", value=row[6]).\
                add_property(name="PFeat", value=row[7])
            if row[13] != "_":
                index = int(row[0])
                predicates.append(index)
                instance.add_span(index, index, row[13], "sense")

        for row in rows:
            # dependency
            if row[8] != "_":
                instance.add_dependency(start=int(row[8]), end=int(row[0]), label=row[10], edge_type="dep")
            if row[9] != "_":
                instance.add_dependency(start=int(row[9]), end=int(row[0]), label=row[11], edge_type="pdep")
            # role
            for col in range(14, len(row)):
                label = row[col]
                if label != "_":
                    pred = predicates[col-14]
                    arg = int(row[0])
                    # if arg != pred:
                    instance.add_dependency(start=pred, end=arg, label=label, edge_type="role")
        return instance

# ----------------------------------------------------------------------------------------------------------------------


class MaltTab(AbstractCoNLLFormat):
    """
     * Loads Malt-TAB dependencies.
    """

    def __init__(self):
        super().__init__()
        self._name = "Malt-TAB"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        instance.add_token().add_property(name="Word", value="-Root-")
        for index, row in enumerate(rows, start=1):
            instance.add_token().\
                add_property(name="Word", value=row[0]).\
                add_property(name="Index", value=str(index)).\
                add_property(name="Pos", value=row[1])

        for mod, row in enumerate(rows, start=1):
            # dependency
            try:
                instance.add_dependency(start=int(row[2]), end=mod, label=row[3], edge_type="dep")
            except (ValueError, IndexError, KeyError):
                print("Can't parse dependency", file=sys.stderr)
                instance.tokens[mod].add_property("DepMissing", "missing")  # role
        return instance

# ----------------------------------------------------------------------------------------------------------------------


class CCG(AbstractCoNLLFormat):
    """
     * Loads CCG dependencies.
    """

    def __init__(self):
        super().__init__()
        self._name = "CCG"

    def create(self, rows):
        rows = [row.strip().split() for row in rows]
        instance = NLPInstance()
        sentence = rows[0]
        # Skip <s> and dep count
        for i in range(2, len(sentence)):
            w_t_c = sentence[i].split("|")
            instance.add_token().\
                add_property(name="Word", value=w_t_c[0]).\
                add_property(name="Tag", value=w_t_c[1]).\
                add_property(name="Category", value=w_t_c[2]).\
                add_property(name="Index", value=str(i - 1))
        # instance.add_token().add_property("Word", "-Root-")

        mod = 1
        for row in rows:
            if row[0] != "<s>" and row[0] != '<\s>':
                # dependency
                try:
                    instance.add_dependency(start=int(row[1]), end=int(row[0]), label=row[2] + "_" + row[3],
                                            edge_type="dep")
                except (ValueError, IndexError, KeyError):
                    print("Can't parse dependency", file=sys.stderr)
                    instance.tokens[mod].add_property("DepMissing", "missing")
                mod += 1
        return instance
