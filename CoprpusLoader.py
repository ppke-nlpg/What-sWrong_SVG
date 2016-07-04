#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


class CorpusLoader:

    @property
    def selected(self):
        if self._selected is None:
            return None
        else:
            return tuple(self.selected)

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def corpora(self):
        return self._corpora

    @corpora.setter
    def corpora(self, value):
        self._corpora = value

    @property
    def fileNames(self):
        return self._fileNames

    @fileNames.setter
    def fileNames(self, value):
        self._fileNames = value

    @property
    def formats(self):
        return self._formats

    @formats.setter
    def formats(self, value):
        self._formats = value

    @property
    def changeListeners(self):
        return self._changeListeners

    @changeListeners.setter
    def changeListeners(self, value):
        self._changeListeners = value

    @property
    def fileChooser(self):
        return self._fileChooser

    @fileChooser.setter
    def fileChooser(self, value):
        self._fileChooser = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def accessory(self):
        return self._accessory

    @accessory.setter
    def accessory(self, value):
        self._accessory = value

    class Listener:
        def corpusAdded(self, corpus, src):
            pass

        def corpusRemoved(self, corpus, src):
            pass

        def corpusSelected(self, corpus, src):
            pass

    def addChangeListener(self, changelistener):
        self._changeListeners.append(changelistener)

    def fireAdded(self, corpus):
        for listener in self._changeListeners:
            listener.corpusAdded(corpus, self)

    def fireRemoved(self, corpus):
        for listener in self._changeListeners:
            listener.corpusRemoved(corpus, self)

    def fireSelected(self, corpus):
        for listener in self._changeListeners:
            listener.corpusSelected(corpus, self)

    class LoadAccessory:
        @property
        def filetypeComboBox(self):
            return self._filetypeComboBox

        @filetypeComboBox.setter
        def filetypeComboBox(self, value):
            self._filetypeComboBox = value

        @property
        def start(self):
            return self._start

        @start.setter
        def start(self, value):
            self._start = value

        @property
        def end(self):
            return self._end

        @end.setter
        def end(self, value):
            self._end = value

        @property
        def accessoryCards(self):
            return self._accessoryCards

        @accessoryCards.setter
        def accessoryCards(self, value):
            self._accessoryCards = value

        def __init__(self):
            # TODO: QtDesigner
            pass

    def getFormat(self):
        pass
        # self._filetypeCombobox.getSelectedItem()

    def setDirectory(self, dir):
        pass

    def getDirectory(self):
        pass

    def property(self, name):
        return self._id + "." + name

    def loadProperties(self, properties):
        self.setDirectory(properties.getProperty(self.property("dir"), ""))
        formatString = properties.getProperty(self.property("forat"), "TAB-separated")
        if formatString == "CoNLL":
            formatString = "TAB-separated"
        # accessory.filetypeComboBox.setSelectedItem(formats.get(formatString))
        for format in self._formats.values():
            format.loadProperties(properties, self._id)

    def saveProperties(self, properties):
        properties.setProperty(self.property("dir"), self.getDirectory())
        # properties.setProperty(self.property("format"), accessory.filetypeCombobox,getSelectedItem().toString())
        for format in self.formats.values():
            format.saveProperties(properties, self.id)

    def __init__(self, title):
        self.id = title.replaceAll(" ", "_").toLowerCase()
        # self.setLayout(GridLayout)
        # self.setBorder()
        #        GridBagConstraints c = new GridBagConstraints();
        #        setUpFormats();

        self._corpora = []
        c = {}
        c.gridx = 0
        c.gridy = 0
        c.gridwidth = 2
        # self.add
