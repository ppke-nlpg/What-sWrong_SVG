#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# To be implemented


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
    def selected(self) -> tuple or None:  # List<NLPInstance>
        if self._selected is None:
            return None
        else:
            return tuple(self.selected)

    @selected.setter
    def selected(self, value: list):
        self._selected = value

    """
     * The set of all loaded corpora.
    """
    @property
    def corpora(self) -> list:  # List<List<NLPInstance>>
        return self._corpora

    @corpora.setter
    def corpora(self, value: list):
        self._corpora = value

    """
     * The file names the corpora came from, stored in a list model.
    """
    @property
    def fileNames(self):  # DefaultListModel
        return self._fileNames

    @fileNames.setter
    def fileNames(self, value):
        self._fileNames = value

    """
     * A mapping from names to CorpusFormat objects that will load corpora when the user chooses the corresponding name.
    """
    @property
    def formats(self) -> dict:  # ArrayList<Listener>
        return self._formats

    @formats.setter
    def formats(self, value: dict):
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
    # private JButton remove;

    """
     * The file chooser dialog.
    """
    @property
    def fileChooser(self):  # JFileChooser
        return self._fileChooser

    @fileChooser.setter
    def fileChooser(self, value):
        self._fileChooser = value

    """
     * The id of this loader (used when loading properties from the user configuration file).
    """
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    """
     * The file dialog accessory to define the range of instances.
    """
    @property
    def accessory(self):  # LoadAccessory
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
    def fireAdded(self, corpus: list):  # List<NLPInstance>
        for listener in self._changeListeners:
            listener.corpusAdded(corpus, self)

    """
     * Notifies all listeners that a corpus was removed.
     *
     * @param corpus the removed corpus.
    """
    def fireRemoved(self, corpus):  # List<NLPInstance>
        for listener in self._changeListeners:
            listener.corpusRemoved(corpus, self)

    """
     * Notifies all listeners that a corpus was selected.
     *
     * @param corpus the selected corpus.
    """
    def fireSelected(self, corpus):  # List<NLPInstance>
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
        def filetypeComboBox(self):  # JComboBox
            return self._filetypeComboBox

        @filetypeComboBox.setter
        def filetypeComboBox(self, value):
            self._filetypeComboBox = value
        
        """
         * The spinner to pick the first instance.
        """
        @property
        def start(self):  # JSpinner
            return self._start

        @start.setter
        def start(self, value):
            self._start = value

        """
         * The spinner to pick the last instance.
        """
        @property
        def end(self):  # JSpinner
            return self._end

        @end.setter
        def end(self, value):
            self._end = value

        """
         * The accessories of each format are stored in a card layout of this panel.
        """
        @property
        def accessoryCards(self):  # JPanel
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

            """ GUI STUFF
            setLayout(new GridBagLayout());
            setBorder(new TitledBorder(new EtchedBorder(), "Parameters"));
            int y = 0;
            add(new JLabel("Format:"), new SimpleGridBagConstraints(y, true));

            filetypeComboBox = new JComboBox(new Vector<Object>(formats.values()));
            filetypeComboBox.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    ((CardLayout) accessoryCards.getLayout()).show(accessoryCards,
                        filetypeComboBox.getSelectedItem().toString());
                }
            });
            start = new JSpinner(new SpinnerNumberModel(0, 0, Integer.MAX_VALUE, 1));
            start.setPreferredSize(new Dimension(100, (int) start.getPreferredSize().getHeight()));
            end = new JSpinner(new SpinnerNumberModel(200, 0, Integer.MAX_VALUE, 1));
            end.setPreferredSize(new Dimension(100, (int) start.getPreferredSize().getHeight()));

            accessoryCards = new JPanel(new CardLayout());
            for (CorpusFormat f : formats.values())
                accessoryCards.add(f.getAccessory(), f.toString());
            ((CardLayout) accessoryCards.getLayout()).show(accessoryCards,
             filetypeComboBox.getSelectedItem().toString());

            add(filetypeComboBox, new SimpleGridBagConstraints(y++, false));
            add(new JSeparator(), new SimpleGridBagConstraints(0, y++, 2, 1));
            add(accessoryCards, new SimpleGridBagConstraints(0, y++, 2, 1));
            add(new JSeparator(), new SimpleGridBagConstraints(0, y++, 2, 1));
            add(new JLabel("From:"), new SimpleGridBagConstraints(y, true));
            add(start, new SimpleGridBagConstraints(y++, false));
            add(new JLabel("To:"), new SimpleGridBagConstraints(y, true));
            add(end, new SimpleGridBagConstraints(y, false));
            """

        """
         * Gets the currently chosen format.
         *
         * @return the currently chosen CorpusFormat.
        """
        def getFormat(self):  # Returns CorpusFormat
            pass  # return CorpusFormat(self._filetypeCombobox.getSelectedItem())  # XXX

        """
         * Gets the index of the first instance.
         *
         * @return the index of the first instance.
        """
        def getStart(self) -> int:
            return int(self._start.getModel().getValue())  # XXX

        """
         * Gets the index of the last instance.
         *
         * @return the index of the last instance.
        """
        def getEnd(self) -> int:
            return int(self._end.getModel().getValue())  # XXX

    """
     * Adds a CorpusFormat.
     *
     * @param format the format to add.
    """
    def addFormat(self, corpus_format):  # CorpusFormat
        self._formats[corpus_format.getName()] = corpus_format

    """
     * Sets the directory to use in the file dialog.
     *
     * @param dir the directory of the file dialog.
    """
    def setDirectory(self, directory: str):  # XXX
        pass  # fileChooser.setCurrentDirectory(new File(dir))

    """
     * gets the directory to use in the file dialog.
     *
     * @return the directory of the file dialog.
    """
    def getDirectory(self):  # XXX
        pass  # fileChooser.getCurrentDirectory().getPath()

    """
     * Loads the properties of this loader from the properties object.
     *
     * @param properties the properties to load this loader's properties from.
    """
    def loadProperties(self, properties):  # Properties XXX TODO
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
    def property(self, name: str):
        return self._id + "." + name

    """
     * Saves the properties of this loader to the given Properties object.
     *
     * @param properties the Properties object to store this loader's properties to.
    """
    def saveProperties(self, properties):  # Properties
        properties.setProperty(self.property("dir"), self.getDirectory())
        properties.setProperty(self.property("format"), self.accessory.filetypeComboBox.getSelectedItem().toString())
        for corpus_format in self.formats.values():
            corpus_format.saveProperties(properties, self.id)

    """
     * Creates a new CorpusLoader with the given title. The title is used to derive an id from.
     *
     * @param title the title of this CorpusLoader.
    """
    def __init__(self, title: str):
        self._selected = []
        self._corpora = []
        self._fileNames = []
        self._formats = {}
        self._changeListeners = []
        self._fileChooser = None
        self._accessory = None

        self.id = title.replace(" ", "_").lower()
        # self.setLayout(GridLayout())
        # self.setBorder(EmptyBorder(5, 5, 5, 5))
        # //setBorder(new TitledBorder(new EtchedBorder(), title));
        #        GridBagConstraints c = new GridBagConstraints();
        #        setUpFormats();

        self._corpora = []  # ArrayList<List<NLPInstance>>()
        c = {"gridx": 0, "gridy": 0, "gridwidth": 2}  # GridBagConstraints()
        # self.add  # add(new JLabel(title), c);
        # XXX CORPUS LOADER NOT IMPLEMENTED!
        """
        # file list
        c.gridy = 1;
        c.fill = GridBagConstraints.BOTH;
        c.weightx = 0.5;
        c.weighty = 0.5;
        fileNames = new DefaultListModel();
        final JList files = new JList(fileNames);
        files.addListSelectionListener(new ListSelectionListener() {
            public void valueChanged(ListSelectionEvent e) {
                if (files.getSelectedIndex() == -1) {
                    selected = null;
                    remove.setEnabled(false);
                    fireSelected(null);

                } else {
                    selected = corpora.get(files.getSelectedIndex());
                    remove.setEnabled(true);
                    fireSelected(selected);
                }
            }
        });
        files.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        JScrollPane pane = new JScrollPane(files);
        pane.setPreferredSize(new Dimension(150, 100));
        //pane.setMinimumSize(new Dimension(150, 50));
        add(pane, c);

        //add files
        fileChooser = new JFileChooser();
        fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
        fileChooser.setDialogTitle("Load Corpus");
        accessory = new LoadAccessory();
        fileChooser.setAccessory(accessory);
        c.gridwidth = 1;
        c.gridx = 0;
        c.gridy = 2;
        c.fill = GridBagConstraints.NONE;
        c.weighty = 0;
        JButton add = new JButton("Add");
        add.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                int returnVal = fileChooser.showOpenDialog(CorpusLoader.this);
                if (returnVal == JFileChooser.APPROVE_OPTION) {
                    final ProgressMonitor monitor = new ProgressMonitor(CorpusLoader.this,
                        "Loading data", null, 0, accessory.getEnd() - 1);
                    new Thread(new Runnable() {
                        public void run() {
                            CorpusFormat format = new TheBeastFormat();
                            try {
                                monitor.setProgress(0);
                                setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR));
                                format = accessory.getFormat();
                                format.setMonitor(new CorpusFormat.Monitor() {
                                    public void progressed(int index) {
                                        monitor.setProgress(index);
                                    }
                                });
                                List<NLPInstance> corpus = format.load(fileChooser.getSelectedFile(),
                                    accessory.getStart(), accessory.getEnd());
                                if (corpus.size() == 0)
                                    throw new RuntimeException("No instances in corpus.");
                                monitor.close();
                                setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
                                corpora.add(corpus);
                                fileNames.addElement(fileChooser.getSelectedFile().getName());
                                files.setSelectedIndex(fileNames.size() - 1);
                                fireAdded(corpus);
                            } catch (FileNotFoundException e1) {
                                e1.printStackTrace();
                            } catch (IOException e1) {
                                e1.printStackTrace();
                            } catch (Exception e) {
                                e.printStackTrace();
                                JOptionPane.showMessageDialog(CorpusLoader.this,
                                    "<html>Data could not be loaded with the <br><b>" +
                                        format.getLongName() +
                                        "</b> format.\nThis means that either you chose the wrong " +
                                        "format, \nthe format of file you selected is broken, \nor we " +
                                        "made a terrible mistake.", "Corpus format problem",
                                    JOptionPane.ERROR_MESSAGE);
                            }
                        }
                    }).start();
                }
            }
        });
        add(add, c);
        c.gridx = 1;
        remove = new JButton("Remove");
        remove.setEnabled(false);
        remove.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                int index = files.getSelectedIndex();
                if (index != -1) {
                    fileNames.remove(index);
                    List<NLPInstance> corpus = corpora.remove(index);
                    fireRemoved(corpus);
                    //repaint();
                }
            }
        });
        add(remove, c);

        //setSize(new Dimension(50, 200));
        //setMinimumSize(new Dimension(150, 10));
    }

    private void setUpFormats() {
        TabFormat tabFormat = new TabFormat();
        TheBeastFormat theBeastFormat = new TheBeastFormat();
        addFormat(tabFormat);
        addFormat(theBeastFormat);
        addFormat(new LispSExprFormat());
        addFormat(new GaleAlignmentFormat());
        addFormat(new BioNLP2009SharedTaskFormat());
        addFormat(new BioNLP2009SharedTaskFormat());
        addFormat(new GizaAlignmentFormat());
    }

    """

    def __len__(self):
        return len(self._corpora)
