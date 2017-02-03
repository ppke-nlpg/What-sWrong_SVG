#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


"""
 * A CorpusLoader is responsible for loading and managing corpora. A corpus is implemented as a list of NLPInstance
 * objects. Each CorpusLoader maintains a list of such corpora, which can be extended by loading corpora from files. The
 * loader displays the corpora and allows the user to select one such corpus. The selected corpus will then be used by
 * other components (such as the {@link com.googlecode.whatswrong.CorpusNavigator} to pick and render NLPInstance
 * objects from.
 * <p/>
 * <p>A CorpusLoader sends out messages to {@link com.googlecode.whatswrong.CorpusLoader.Listener} objects whenever a
 * new corpus is added, removed or selected.
 * <p/>
 * <p>The CorpusLoader loads files using {@link com.googlecode.whatswrong.io.CorpusFormat} objects. Each such object
 * provides an swing panel that will be used in the file dialog to configure how the particular format needs to be
 * loaded.
 *
 * @author Sebastian Riedel
"""


class CorpusLoader:
    """
     * The current selected corpus.
    """
    @property
    def selected(self):
        if self._selected is None:
            return None
        else:
            return tuple(self.selected)

    @selected.setter
    def selected(self, value):
        self._selected = value

    """
     * The set of all loaded corpora.
    """
    @property
    def corpora(self):
        return self._corpora

    @corpora.setter
    def corpora(self, value):
        self._corpora = value

    """
     * The file names the corpora came from, stored in a list model.
    """
    @property
    def fileNames(self):
        return self._fileNames

    @fileNames.setter
    def fileNames(self, value):
        self._fileNames = value

    """
     * A mapping from names to CorpusFormat objects that will load corpora when the user chooses the corresponding name.
    """
    @property
    def formats(self):
        return self._formats

    @formats.setter
    def formats(self, value):
        self._formats = value

    """
     * The list of listeners of this loader.
    """
    @property
    def changeListeners(self):
        return self._changeListeners

    @changeListeners.setter
    def changeListeners(self, value):
        self._changeListeners = value

    """
     * The button that removes the selected corpus.
    """
    # XXX private JButton remove;

    """
     * The file chooser dialog.
    """
    @property
    def fileChooser(self):
        return self._fileChooser

    @fileChooser.setter
    def fileChooser(self, value):
        self._fileChooser = value

    """
     * The id of this loader (used when loading properties from the user configuration file).
    """
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    """
     * The file dialog accessory to define the range of instances.
    """
    @property
    def accessory(self):
        return self._accessory

    @accessory.setter
    def accessory(self, value):
        self._accessory = value

    """
     * A CorpusLoader.Listener listens to events of this loader.
    """
    class Listener:
        """
         * Called when a new corpus is added.
         *
         * @param corpus the corpus that was added.
         * @param src    the loader which added the corpus.
        """
        def corpusAdded(self, corpus, src):
            pass

        """
         * Called when a corpus is removed.
         *
         * @param corpus the corpus which was removed.
         * @param src    the loader which removed the corpus.
        """
        def corpusRemoved(self, corpus, src):
            pass

        """
         * Called when a corpus is selected.
         *
         * @param corpus the selected corpus.
         * @param src    the loader which selected the corpus.
        """
        def corpusSelected(self, corpus, src):
            pass

    """
     * Adds a listener to this loader.
     *
     * @param changeListener the listener to add.
    """
    def addChangeListener(self, changelistener):
        self._changeListeners.append(changelistener)

    """
     * Notifies all listeners that a corpus was added.
     *
     * @param corpus the added corpus.
    """
    def fireAdded(self, corpus):
        for listener in self._changeListeners:
            listener.corpusAdded(corpus, self)

    """
     * Notifies all listeners that a corpus was removed.
     *
     * @param corpus the removed corpus.
    """
    def fireRemoved(self, corpus):
        for listener in self._changeListeners:
            listener.corpusRemoved(corpus, self)

    """
     * Notifies all listeners that a corpus was selected.
     *
     * @param corpus the selected corpus.
    """
    def fireSelected(self, corpus):
        for listener in self._changeListeners:
            listener.corpusSelected(corpus, self)

    """
     * Returns the currently selected corpus or null if no corpus is selected.
     *
     * @return the currently selected corpus or null if no corpus is selected.
    """
    # See getter above...

    """
     * The LoadAccessory contains fields to define the first and last instance, allows us to select the format to load
      and displays an internal format-specific accessory.
    """
    class LoadAccessory:
        """
         * The combo box to pick the format from.
        """
        @property
        def filetypeComboBox(self):
            return self._filetypeComboBox

        @filetypeComboBox.setter
        def filetypeComboBox(self, value):
            self._filetypeComboBox = value
        
        """
         * The spinner to pick the first instance.
        """
        @property
        def start(self):
            return self._start

        @start.setter
        def start(self, value):
            self._start = value

        """
         * The spinner to pick the last instance.
        """
        @property
        def end(self):
            return self._end

        @end.setter
        def end(self, value):
            self._end = value

        """
         * The accessories of each format are stored in a card layout of this panel.
        """
        @property
        def accessoryCards(self):
            return self._accessoryCards

        @accessoryCards.setter
        def accessoryCards(self, value):
            self._accessoryCards = value

        """
         * Creates a new LoadAccessory.
        """
        def __init__(self):
            self._filetypeComboBox = None
            self._start = None
            self._end = None
            self._accessoryCards = None
            # TODO: QtDesigner
            pass

        """
         * Gets the currently chosen format.
         *
         * @return the currently chosen CorpusFormat.
        """
        def getFormat(self):
            pass
            # self._filetypeCombobox.getSelectedItem()

        """
         * Gets the index of the first instance.
         *
         * @return the index of the first instance.
        """
        # def getStart(self):
        #     return self._start.getModel().getValue()

        """
         * Gets the index of the last instance.
         *
         * @return the index of the last instance.
        """
        def getEnd(self):
            pass
            # return self._end.getModel().getValue();

    """
     * Adds a CorpusFormat.
     *
     * @param format the format to add.
    """
    def addFormat(self, corpus_format):
        self._formats[corpus_format.getName()] = corpus_format

    """
     * Sets the directory to use in the file dialog.
     *
     * @param dir the directory of the file dialog.
    """
    def setDirectory(self, dir):
        pass

    """
     * gets the directory to use in the file dialog.
     *
     * @return the directory of the file dialog.
    """
    def getDirectory(self):
        pass

    """
     * Loads the properties of this loader from the properties object.
     *
     * @param properties the properties to load this loader's properties from.
    """
    def loadProperties(self, properties):
        self.setDirectory(properties.getProperty(self.property("dir"), ""))
        # formatString = properties.getProperty(self.property("format"), "TAB-separated")
        # if formatString == "CoNLL":
        #     formatString = "TAB-separated"
        # accessory.filetypeComboBox.setSelectedItem(formats.get(formatString))
        for corpus_format in self._formats.values():
            corpus_format.loadProperties(properties, self._id)

    """
     * Returns a qualified version of the given name to be used as keys in {@link Properties} objects.
     *
     * @param name the name to qualify.
     * @return a name qualified using the id of this loader.
    """
    def property(self, name):
        return self._id + "." + name

    """
     * Saves the properties of this loader to the given Properties object.
     *
     * @param properties the Properties object to store this loader's properties to.
    """
    def saveProperties(self, properties):
        properties.setProperty(self.property("dir"), self.getDirectory())
        # properties.setProperty(self.property("format"), accessory.filetypeCombobox,getSelectedItem().toString())
        for corpus_format in self.formats.values():
            corpus_format.saveProperties(properties, self.id)

    """
     * Creates a new CorpusLoader with the given title. The title is used to derive an id from.
     *
     * @param title the title of this CorpusLoader.
    """
    def __init__(self, title):
        self._selected = []
        self._corpora = []
        self._fileNames = []
        self._formats = {}
        self._changeListeners = []
        self._fileChooser = None
        self._id = ""
        self._accessory = None

        self.id = title.replaceAll(" ", "_").toLowerCase()
        # self.setLayout(GridLayout)
        # self.setBorder()
        # //setBorder(new TitledBorder(new EtchedBorder(), title));
        #        GridBagConstraints c = new GridBagConstraints();
        #        setUpFormats();

        self._corpora = []  # ArrayList<List<NLPInstance>>()
        c = {}  # GridBagConstraints()
        c.gridx = 0
        c.gridy = 0
        c.gridwidth = 2
        # self.add
        # XXX CORPUS LOADER NOT IMPLEMENTED!

    def __len__(self):
        return len(self._corpora)
