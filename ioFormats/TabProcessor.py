#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This file implements TabFormat and all classes inherited from it: TabFormat, CoNLL2000, CoNLL2002, CoNLL2003,
#  CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, CoNLL2009 CoNLL2009, Malt-TAB and CCG classes...
# TabProcessor interface class is omited...

import sys

from NLPInstance import *
from ioFormats.CorpusFormat import *

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

    def __init__(self, MainWindow):

        self._name = "TAB-separated"
        self._monitor = None
        self._processors = {}

        self.addProcessor(name="CCG", processor=CCG())
        self.addProcessor(name="CoNLL 2009", processor=CoNLL2009())
        self.addProcessor(name="CoNLL 2008", processor=CoNLL2008())
        self.addProcessor(name="CoNLL 2006", processor=CoNLL2006())
        # self.addProcessor(name="CoNLL 2005", processor=CoNLL2005())
        self.addProcessor(name="CoNLL 2004", processor=CoNLL2004())
        self.addProcessor(name="CoNLL 2002", processor=CoNLL2002())
        self.addProcessor(name="CoNLL 2003", processor=CoNLL2003())
        self.addProcessor(name="CoNLL 2000", processor=CoNLL2000())
        self.addProcessor(name="MaltTab", processor=MaltTab())

        # TODO: grafikus rész

        self._accessory = MainWindow
        self._type = MainWindow
        self._open = MainWindow

    @property
    def accessory(self):
        return self._accessory

    @accessory.setter
    def accessory(self, value):
        self._accessory = value  # TODO: JPanel

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

    @property
    def name(self):
        return self._name

    def addProcessor(self, processor, name=None):  # XXX Arguments reversed to be able to use defaults...
        if name is not None:
            self._processors[name] = processor
        else:
            self._processors[str(processor)] = property

    def __str__(self):
        return self._name

    @property
    def longName(self):
        #  TODO: type
        return self._name + "(" + str(self._type.getSelectedItem()) + ")"

    def setMonitor(self, monitor):
        self._monitor = monitor

    def loadProperties(self, properties, prefix):
        yearString = properties.getProperty(prefix + ".tay.type", "CoNLL 2008")
        self._type.setSelectedItem(self._processors[yearString])
        # TODO: grafika

    def saveProperties(self, properties, prefix):
        properties.setProperty(prefix + ".tab.type", str(self._type.getSelectedItem()))

    def load(self, file, From, to):
        processor = self._type.getSelectedItem()  # TODO grafika
        result = self.loadTabs(file, From, to, processor, False)
        if self._open.isSelected():
            filename = file.name[0:file.name.rfind('.')] + ".open"
            openFile = open(filename)
            openCorpus = self.loadTabs(openFile, From, to, processor, True)
            for i in range(0, len(openCorpus)):
                result[i].merge(openCorpus[i])
        return result

    def loadTabs(self, file, From, to, processor, open):
        corpus = []
        rows = []
        instnceNr = 0
        for line in file:
            if instnceNr >= to:
                break
            line = line.strip()
            if line == "" or re.match("<\\s>$", line.split()[0]):
                self._monitor.progressed(instnceNr)
                instnceNr += 1
                if instnceNr <= From:  # Equals because ++instnceNr expression
                    continue
                if open:
                    instance = processor.createOpen(rows)
                else:
                    instance = processor.create(rows)
                corpus.append(instance)
                rows.clear()
            else:
                if instnceNr < From:
                    continue
                rows.append(line.split("\\s+"))  # TODO: rows.add(Arrays.asList(line.split("\\s+")));
        if len(rows) > 0:
            if open:
                corpus.append(processor.createOpen(rows))
            else:
                corpus.append(processor.create(rows))
        return corpus

    @staticmethod
    def extractSpan03(rows, column, type, instance):
        index = 0
        inChunk = False
        begin = 0
        currentChunk = ""
        for row in rows:
            chunk = row[column]
            minus = chunk.find('-')
            if minus != -1:
                bio = chunk[0:minus]
                label = chunk[minus + 1:]
                if inChunk:
                    # start a new chunk and finish old one
                    if "B" == bio or "I" == bio and label != currentChunk:
                        instance.addSpan(begin, index-1, currentChunk, type)
                        begin = index
                        currentChunk = label
                else:
                    inChunk = True
                    begin = index
                    currentChunk = label
            elif inChunk:
                    instance.addSpan(begin, index-1, currentChunk, type)
                    inChunk = False
            index += 1
        if inChunk:
            instance.addSpan(begin, index-1, currentChunk, type)

    @staticmethod
    def extractSpan00(rows, column, type, instance):
        index = 0
        inChunk = False
        begin = 0
        currentChunk = ""
        for row in rows:
            chunk = row[column]
            minus = chunk.find('-')
            if minus != -1:
                bio = chunk[0:minus]
                label = chunk[minus+1:]
                if "B" == bio:
                    if inChunk:
                        instance.addSpan(begin, index-1, currentChunk, type)
                    begin = index
                    currentChunk = label
                    inChunk = True
            elif inChunk:
                    instance.addSpan(begin, index-1, currentChunk, type)
                    inChunk = False
            index += 1

    @staticmethod
    def extractSpan05(rows, column, type, prefix, instance):
        index = 0
        begin = 0
        currentChunk = ""
        for row in rows:
            chunk = row[column]
            if chunk.startswith("("):
                end = chunk.find("*")
                if end == -1:  # In the Java version here comes an exception...
                    raise RuntimeError
                currentChunk = chunk[1:end]
                begin = index
            if chunk.endswith(")"):
                instance.addSpan(begin, index, prefix + currentChunk, type)
            index += 1

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CoNLL 2000 chunk data.
 *
 * @author Sebastian Riedel
"""


class CoNLL2000:

    """
     * The name of the processor.
    """
    name = "CoNLL 2000"

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CoNLL2000.name

    """
     * @see TabProcessor#create(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):

        instance = NLPInstance()
        index = 0
        for row in rows:
            row = row.strip().split()
            chunk = row[2]
            instance.addToken().\
                addProperty(name="Word", value=row[0]).\
                addProperty(name="Index", value=str(index))
            instance.addSpan(index, index, row[1], "pos")
            instance.addSpan(index, index, chunk, "chunk (BIO)")
            index += 1

        tabformat = TabFormat(object)  # TODO: object = MainWindow?
        tabformat.extractSpan00(rows=rows, column=2, type="chunk", instance=instance)

        return instance

    """
     * @see TabProcessor#createOpen(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen():
        return False

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CoNLL 2002 NER data.
 *
 * @author Sebastian Riedel
"""


class CoNLL2002:

    """
     * The name of this processor.
    """
    name = "CoNLL 2002"

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CoNLL2002.name

    """
     * @see TabProcessor#create(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):

        instance = NLPInstance()
        index = 0
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name="Word", value=row[0]).\
                addProperty(name="Index", value=str(index))
            instance.addSpan(index, index, row[1], "ner (BIO)")
            index += 1

        tabformat = TabFormat(object)  # TODO: object = MainWindow?
        tabformat.extractSpan00(rows=rows, column=1, type="ner", instance=instance)

        return instance

    """
     * @see TabProcessor#createOpen(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen(_):
        return False

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CoNLL 2003 chunk and NER data.
 *
 * @author Sebastian Riedel
"""


class CoNLL2003:

    """
     * The name of the processor.
    """
    name = "CoNLL 2003"

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CoNLL2003.name

    """
     * @see TabProcessor#create(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):
        instance = NLPInstance()
        index = 0
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name="Word", value=row[0]).\
                addProperty(name="Index", value=str(index))

            instance.addSpan(index, index, row[1], "pos")
            instance.addSpan(index, index, row[2], "chunk (BIO")
            instance.addSpan(index, index, row[3], "ner (BIO)")
            index += 1

        tabformat = TabFormat(object)  # TODO: object = MainWindow?
        tabformat.extractSpan03(rows=rows, column=2, type="chunk", instance=instance)
        tabformat.extractSpan03(rows=rows, column=3, type="ner", instance=instance)

        return instance

    """
     * @see TabProcessor#createOpen(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen():
        return False

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CoNLL 2004 SRL data.
 *
 * @author Sebastian Riedel
"""


class CoNLL2004:

    """
     * The name of the processor.
    """
    name = "CoNLL 2004"

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CoNLL2004.name

    """
     * @see TabProcessor#create(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):
        instance = NLPInstance()
        index = 0
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name="Word", value=row[0]).\
                addProperty(name="Index", value=str(index))
            index += 1
        predicateCount = 0
        index = 0
        for row in rows:
            row = row.strip().split()
            if row[1] != "-":
                sense = row[1]
                instance.addSpan(index, index, sense, "sense")

                tabformat = TabFormat(object)  # TODO: object = MainWindow?
                tabformat.extractSpan05(rows, 2+predicateCount, "role", sense+":", instance)

                predicateCount += 1
            index += 1
        return instance

    """
     * @see TabProcessor#createOpen(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen():
        return False

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CoNLL 2005 SRL data.
 *
 * @author Sebastian Riedel
"""


class CoNLL2005:

    """
     * The name of the processor.
    """
    name = "CoNLL 2005"

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CoNLL2005.name

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#create(java.util.List<? extends java.util.List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):
        instance = NLPInstance()
        index = 0
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name="Word", value=row[0]).\
                addProperty(name="Index", value=str(index))
            index += 1
        predicateCount = 0
        index = 0
        for row in rows:
            row = row.strip().split()
            if row[9] != "-":  # TODO: nincs 9 szó ebben?
                sense = row[10] + "." + row[9]
                instance.addSpan(index, index, sense, "sense")

                tabformat = TabFormat(object)  # TODO: object = MainWindow?
                tabformat.extractSpan05(rows, 11+predicateCount, "role", sense+":", instance)

                predicateCount += 1
            index += 1
        return instance

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#createOpen(java.util.List<? extends java.util.List
     <String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen():
        return False

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CoNLL 2006 Dependency data.
 *
 * @author Sebastian Riedel
"""


class CoNLL2006:

    """
     * The name of the processor.
    """
    name = "CoNLL 2006"

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CoNLL2006.name

    """
     * @see TabProcessor#create(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):
        instance = NLPInstance()
        instance.addToken().addProperty("Word", "-Root-")
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name="Word", value=row[1]).\
                addProperty(name="Index", value=row[0]).\
                addProperty(name="Lemma", value=row[2]).\
                addProperty(name="CPos", value=row[3]).\
                addProperty(name="Pos", value=row[4]).\
                addProperty(name="Feats", value=row[5])
        for row in rows:
            row = row.strip().split()
            # dependency
            mod = int(row[0])
            try:
                instance.addEdge(From=int(row[6]), to=mod, label=row[7], type="dep")
            except:  # XXX TRACK DOWN POSSIBLE EXCEPTION TYPES!
                print("Can't parse dependency", file=sys.stderr)
                instance.tokens[mod].addProperty("DepMissing", "missing")
            # role
        return instance

    """
     * @see TabProcessor#createOpen(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen():
        return False

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CoNLL 2008 Joint SRL and Dependency data.
 *
 * @author Sebastian Riedel
"""


class CoNLL2008:

    """
     * The name of the processor.
    """
    name = "CoNLL 2008"

    @property
    def ne(self):
        return TokenProperty("Named Entity", 10)

    @property
    def bbn(self):
        return TokenProperty("NamedEntity BBN", 11)

    @property
    def wn(self):
        return TokenProperty("WordNet", 12)

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CoNLL2008.name

    """
     * @see TabProcessor#create(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):
        instance = NLPInstance()
        instance.addToken().addProperty("Word", "-Root-")
        predicates = []
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name="Word", value=row[1]).\
                addProperty(name="Index", value=row[0]).\
                addProperty(name="Lemma", value=row[2]).\
                addProperty(name="Pos", value=row[3]).\
                addProperty(name="Split Form", value=row[5]).\
                addProperty(name="Split Lemma", value=row(6)).\
                addProperty(name="Split PoS", value=row[7])
            if row[10] != "_":
                index = int(row[0])
                predicates.append(index)
                instance.addSpan(index, index, row[10], "sense")
        for row in rows:
            row = row.strip().split()
            # dependency
            if row[8] != "_":
                instance.addEdge(int(row[8]), int(row[0]), row[9], "dep")
            # role
            for col in range(11, len(row)):
                label = row[col]
                if label != "_":
                    pred = predicates[col-11]
                    arg = int(row[0])
                    # if arg != pred
                    instance.addEdge(From=pred, to=arg, label=label, type="role")
        return instance

    """
     * @see TabProcessor#createOpen(List<? extends List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    def createOpen(self, rows):
        instance = NLPInstance()
        instance.addToken()
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name=self.ne, value=row[0]).\
                addProperty(name=self.bbn, value=row[1]).\
                addProperty(name=self.wn, value=row[2])
        index = 1
        for row in rows:
            row = row.strip().split()
            # dependency
            instance.addEdge(From=int(row[3]), to=index, label=row[4], type="malt")
            index += 1
        return index

    """
     * @see TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportsOpen():
        return True

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CoNLL 2009 Joint SRL and Dependency data.
 *
 * @author Sebastian Riedel
"""


class CoNLL2009:

    """
     * The name of the processor.
    """
    name = "CoNLL 2009"

    @property
    def ne(self):
        return TokenProperty("Named Entity", 10)

    @property
    def bbn(self):
        return TokenProperty("NamedEntity BBN", 11)

    @property
    def wn(self):
        return TokenProperty("WordNet", 12)

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CoNLL2009.name

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#create(java.util.List<? extends java.util.List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):
        instance = NLPInstance()
        instance.addToken().addProperty(name="Word", value="-Root-")
        predicates = []
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name="Word", value=row[1]).\
                addProperty(name="Index", value=row[0]).\
                addProperty(name="Lemma", value=row[2]).\
                addProperty(name="PLemma", value=row[3]).\
                addProperty(name="PoS", value=row[4]).\
                addProperty(name="PPoS", value=row[5]).\
                addProperty(name="Feat", value=row[6]).\
                addProperty(name="PFeat", value=row[7])
            if row[13] != "_":
                index = int(row[0])
                predicates.append(index)
                instance.addSpan(index, index, row[13], "sense")
        for row in rows:
            row = row.strip().split()
            # dependency
            if row[8] != "_":
                instance.addDependency(From=int(row[8]), to=int(row[0]), label=row[10], type="dep")
            if row[9] != "_":
                instance.addDependency(From=int(row[9]), to=int(row[0]), label=row[11], type="pdep")
            # role
            for col in range(14, len(row)):
                label = row[col]
                if label != "_":
                    pred = predicates[col-14]
                    arg = int(row[0])
                    # if arg != pred:
                    instance.addEdge(From=pred, to=arg, label=label, type="role")
        return instance

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#createOpen(java.util.List<? extends java.util.List
     <String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen():
        return False

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads Malt-TAB dependencies.
 *
 * @author Sebastian Riedel
"""


class MaltTab:

    """
     * The name of the processor.
    """
    name = "Malt-TAB"

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return MaltTab.name

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#create(java.util.List<? extends java.util.List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):
        instance = NLPInstance()
        instance.addToken().addProperty(name="Word", value="-Root-")
        index = 1
        for row in rows:
            row = row.strip().split()
            instance.addToken().\
                addProperty(name="Word", value=row[0]).\
                addProperty(name="Index", value=str(index)).\
                addProperty(name="Pos", value=row[1])
            index += 1
        mod = 1
        for row in rows:
            row = row.strip().split()
            # dependency
            try:  # XXX Why not Edge? Str int conversion possibly wrong...
                # instance.addEdge(From=int(row[2]), to=mod, label=row[3], type="dep")
                instance.addDependency(From=row[2], to=str(mod), label=row[3], type="dep")
            except:  # XXX TRACK DOWN POSSIBLE EXCEPTION TYPES!
                print("Can't parse dependency", file=sys.stderr)
                instance.tokens[mod].addProperty("DepMissing", "missing")
            # role
            mod += 1
        return instance

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#createOpen(java.util.List<? extends java.util.List
     <String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen():
        return False

# ----------------------------------------------------------------------------------------------------------------------

"""
 * Loads CCG dependencies.
 *
 * @author Yonatan Bisk
"""


class CCG:

    """
     * The name of the processor.
    """
    name = "CCG"

    """
     * Returns the name of this processor.
     *
     * @return the name of this processor.
    """
    def __str__(self):
        return CCG.name

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#create(java.util.List<? extends java.util.List<String>>)
     * Create an NLPInstance from the given table (list of rows) of strings.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod  # XXX Currently static but maybe later it will be changed...
    def create(rows):
        instance = NLPInstance()
        sentence = rows[0]
        # Skip <s> and dep count
        for i in range(2, len(sentence)):
            w_t_c = sentence[i].split("|")  # In Python this is not regex
            instance.addToken().\
                addProperty(name="Word", value=w_t_c[0]).\
                addProperty(name="Tag", value=w_t_c[1]).\
                addProperty(name="Category", value=w_t_c[2]).\
                addProperty(name="Index", value=str(i-1))
        # instance.addToken().addProperty("Word", "-Root-")

        mod = 1
        for row in rows:
            row = row.strip().split()
            if row[0] != "<s>" and not re.match("<\\s>$", row[0]):
                # dependency
                try:
                    instance.addEdge(From=int(row[1]), to=int(row[0]), label=row[2] + "_" + row[3], type="dep")
                except:  # XXX TRACK DOWN POSSIBLE EXCEPTION TYPES!
                    print("Can't parse dependency", file=sys.stderr)
                    instance.tokens[mod].addProperty("DepMissing", "missing")
                mod += 1
        return instance

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#createOpen(java.util.List<? extends java.util.List
     <String>>)
     * Create an NLPInstance from the given table (list of rows) of strings, assuming that the passed rows are from the
     * open dataset.
     *
     * @param rows the rows that represent the column separated values in Tab format files.
     * @return an NLPInstance that represents the given rows.
    """
    @staticmethod
    def createOpen(_):
        return None

    """
     * @see com.googlecode.whatswrong.ioFormats.TabProcessor#supportsOpen()
     * Does this processor support loading of open datasets (as in "CoNLL Open Track").
     *
     * @return true iff the processor supports loading of open datasets.
    """
    @staticmethod
    def supportOpen():
        return False
