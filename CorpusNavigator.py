#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HIÁNYOS!

from NLPCanvas import NLPCanvas
from CorpusLoader import CorpusLoader
from libwwnlp.model.nlp_instance import NLPInstance, nlp_diff
from libwwnlp.model.token_property import TokenProperty

"""
 * A CorpusNavigator allows the user to navigate through a corpus (or a diffed corpus) and pick one NLP instance to draw
 * (or one difference of two NLPInstance objects in terms of their edges). The CorpusNavigator also allows us to search
 * a corpus for keywords by using the Lucene IR engine. The instances that match the user's query are presented in a
 * list and one of them can then be picked to be rendered. The CorpusNavigator has also a spinner panel that allows to
 * go through this corpus by index. This spinner is not part of the navigator panel and can be placed anywhere.
 *
 * @author Sebastian Riedel
"""

"""
 * A Search result consisting of the instance index and a text snippet that indicates the position in the instance
 * where they key terms were found.
"""


class Result:
    """
     * A text representation of the location in which the key terms were found.
    """

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    """
     * The index of the instance in which the key terms were found.
    """

    @property
    def nr(self) -> int:
        return self._nr

    @nr.setter
    def nr(self, value: int):
        self._nr = value

    """
     * Creates a new Result.
     *
     * @param nr   the index nr.
     * @param text the text snippet.
    """

    def __init__(self, text: str, nr: int):  # XXX Swapped!
        self._text = text
        self._nr = nr

    """
     * Returns the text snippet.
     *
     * @return the text snippet.
    """

    def __str__(self) -> str:
        return self._text


class CorpusNavigator:
    """
     * The loader for guess instances.
    """
    @property
    def guess(self) -> CorpusLoader:
        return self._guess

    @guess.setter
    def guess(self, value: CorpusLoader):
        self._guess = value

    """
     * The loader for gold instances.
    """
    @property
    def gold(self) -> CorpusLoader:
        return self._gold

    @gold.setter
    def gold(self, value: CorpusLoader):
        self._gold = value

    # XXX WHAT IS THIS?
    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value

    """
     * The canvas that renders the instances.
    """
    @property
    def canvas(self) -> NLPCanvas:
        return self._canvas

    @canvas.setter
    def canvas(self, value: NLPCanvas):
        self._canvas = value

    """
     * The spinner that controls the current instance to be rendered by the canvas.
    """
    @property
    def spinner(self):  # JSpinner
        return self._spinner

    @spinner.setter
    def spinner(self, value):
        self._spinner = value

    """
     * The number model that backs the spinner that controls the current instance to render.
    """
    @property
    def numberModel(self):   # SpinnerNumberModel
        return self._numberModel

    @numberModel.setter
    def numberModel(self, value):
        self._numberModel = value

    """
     * A mapping from corpora to index searchers that can be used to search the corpus.
    """
    @property
    def indicies(self) -> dict:  # HashMap<List<NLPInstance>, IndexSearcher>
        return self._indices

    @indicies.setter
    def indicies(self, value: dict):
        self._indices = value

    """
     * A mapping from pairs of corpora to index searchers that can be used to search the differences between the two
     * corpora.
    """
    @property
    def diffCorpora(self) -> dict:  # HashMap<Pair<List<NLPInstance>, List<NLPInstance>>, List<NLPInstance>>
        return self._diffCorpora

    @diffCorpora.setter
    def diffCorpora(self, value: dict):
        self._diffCorpora = value

    """
     * The set of gold corpora.
    """
    @property
    def goldCorpora(self) -> list:  # XXX Should be set HashSet<List<NLPInstance>>
        return self._goldCorpora

    @goldCorpora.setter
    def goldCorpora(self, value: list):  # XXX Should be set
        self._goldCorpora = value

    """
     * The set of guess corpora.
    """
    @property
    def guessCorpora(self) -> list:  # XXX Should be set HashSet<List<NLPInstance>>
        return self._guessCorpora

    @guessCorpora.setter
    def guessCorpora(self, value: list):  # XXX Should be set
        self._guessCorpora = value

    """
     * The current IndexSearcher (for the selected corpus/corpus pair).
    """
    @property
    def indexSearcher(self):  # IndexSearcher
        return self._indexSearcher

    @indexSearcher.setter
    def indexSearcher(self, value):
        self._indexSearcher = value

    """
     * The Analyzer for the search index.
    """
    @property
    def analyzer(self):  # Analyzer
        return self._analyzer

    @analyzer.setter
    def analyzer(self, value):
        self._analyzer = value
    """
     * The search button that triggers the search process.
    """
    # private JButton searchButton;
    """
     * The list of search results.
    """
    # private JList results;
    """
     * The field for the search terms.
    """
    # private JTextField search;
    """
     * The panel that controls the instance index spinner.
    """
    # private JPanel spinnerPanel;
    """
     * The label that shows how many results where found.
    """
    # private JLabel ofHowMany;

    """
     * The EdgeTypeAndLabelFilter that needs to be initialized when the navigator does not have a selected corpus
      and shows an example sentence.
    """
    # private EdgeTypeAndLabelFilter edgeTypeFilter;

    """
     * Adds the corpus to the corresponding internal set of corpora.
     *
     * @param corpus the corpus to add.
     * @param src    the source loader.
    """
    def corpusAdded(self, corpus: [NLPInstance], src: CorpusLoader):
        if src == self._gold:
            self._goldCorpora.append(corpus)
            # indices[corpus] = self.createIndex(corpus)
        else:
            self._guessCorpora.append(corpus)
            # indices[corpus] = self.createIndex(corpus)

    """
     * Returns a difference corpus between two corpora. This difference corpus is calculated if it hasn't been
     * calculated before.
     *
     * @param gold  the gold corpus.
     * @param guess the guess corpus.
     * @return the difference corpus.
    """
    def getDiffCorpus(self, gold: [NLPInstance], guess: [NLPInstance]) -> [NLPInstance]:  # XXX
        # diffCorpus = self._diffCorpora.get((gold, guess))
        diffCorpus = None
        if diffCorpus is None:
            diffCorpus = []  # ArrayList<NLPInstance>(Math.min(gold.size(), guess.size()))
            # self._diffCorpora[(gold, guess)] = diffCorpus
        for i in range(0, min(len(gold), len(guess))):
            diffCorpus.append(nlp_diff(gold[i], guess[i], "eval_status_Match",
                                       "eval_status_FN", "eval_status_FP"))
        # indices.put(diffCorpus, createIndex(diffCorpus))
        return diffCorpus
        # return nlp_diff(gold, guess)  # XX Current Working

    """
     * Removes the difference corpus for the given corpus pair.
     *
     * @param gold  the gold corpus.
     * @param guess the guess corpus.
    """
    def removeDiffCorpus(self, gold: [NLPInstance], guess: [NLPInstance]):
        pair = (gold, guess)
        diffCorpus = self._diffCorpora.get(pair)
        if diffCorpus is not None:
            del self._diffCorpora[pair]
            del self._indices[diffCorpus]

    """
     * Removes the corpus and all diff corpora that compare the given corpus
     *
     * @param corpus the corpus to remove.
     * @param src    the loader that removed the corpus.
    """
    def corpusRemoved(self, corpus: [NLPInstance], src: [NLPInstance]):
        if src == self._gold:
            self._goldCorpora.remove(corpus)
            del self._indices[corpus]
            for c in self._guessCorpora:
                self.removeDiffCorpus(corpus, c)
        else:
            self._guessCorpora.remove(corpus)
            del self._indices[corpus]
            for c in self._goldCorpora:
                self.removeDiffCorpus(corpus, c)

    """
     * Changes the current selected instance to be the one in the new corpus with the same index as the last chosen
     * instance of the old corpus or the last instance if no such instance exist.
     *
     * @param corpus the newly selected corpus.
     * @param src    the loader in which the corpus was selected.
    """
    """
    public synchronized void corpusSelected(final List<NLPInstance> corpus,
                                            final CorpusLoader src) {
        updateCanvas();
        results.setModel(new DefaultListModel());

    }
    """

    """
     * Creates a new CorpusNavigator.
     *
     * @param canvas         the canvas to control.
     * @param goldLoader     the loader of gold corpora.
     * @param guessLoader    the loader of guess corpora.
     * @param edgeTypeFilter the EdgeTypeAndLabelFilter we need when no corpus is selected and a example sentence
                             is chosen and passed to the NLPCanvas.
    """
    def __init__(self,  ui, canvas: NLPCanvas, scene=None, goldLoader: CorpusLoader=None,
                 guessLoader: CorpusLoader=None, edgeTypeFilter=None):
        """
        super(new GridBagLayout());
        this.edgeTypeFilter = edgeTypeFilter;
        this.guess = guessLoader;
        this.gold = goldLoader;
        this.canvas = canvas;
        guessLoader.addChangeListener(this);
        goldLoader.addChangeListener(this);
        setBorder(new EmptyBorder(5, 5, 5, 5));
        //setBorder(new TitledBorder(new EtchedBorder(), "Navigate"));
        """
        self._numberModel = None  # SpinnerNumberModel()
        """
        numberModel.setMinimum(0);
        numberModel.setMaximum(100);
        spinner = new JSpinner(numberModel);
        //spinner.getEditor().set
        spinner.setEnabled(false);
        JSpinner.NumberEditor numberEditor = new JSpinner.NumberEditor(spinner);
        spinner.setEditor(numberEditor);
        spinner.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                updateCanvas();
            }
        });

        final JFormattedTextField editorTextField = numberEditor.getTextField();
        editorTextField.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    spinner.setValue(Integer.valueOf(editorTextField.getText()));
                } catch (NumberFormatException ex) {
                    spinner.setValue(editorTextField.getValue());
                }
            }
        });


        spinnerPanel = new JPanel();
        spinnerPanel.setLayout(new BoxLayout(spinnerPanel, BoxLayout.X_AXIS));
        spinnerPanel.setBorder(BorderFactory.createEmptyBorder(0, 0, 0, 0));
        spinnerPanel.add(spinner);
        ofHowMany = new JLabel(" of 1");
        spinnerPanel.add(ofHowMany);

        search = new JTextField(10);
        search.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                searchCorpus();
            }
        });
        //add(search, new SimpleGridBagConstraints(1, false));

        //search button
        searchButton = new JButton("Search");
        JPanel searchPanel = new JPanel(new BorderLayout());
        searchPanel.add(search, BorderLayout.CENTER);
        searchPanel.add(searchButton, BorderLayout.EAST);
        //add(searchButton, new SimpleGridBagConstraints(2, false, false));
        searchButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                searchCorpus();
            }
        });

        results = new JList();
        results.addListSelectionListener(new ListSelectionListener() {
            public void valueChanged(ListSelectionEvent e) {
                int selectedIndex = results.getSelectedIndex();
                if (selectedIndex != -1) {
                    int nr = ((Result) results.getSelectedValue()).nr;
                    spinner.setValue(nr);
                    repaint();
                }
            }
        });


        add(searchPanel, new SimpleGridBagConstraints(0, 0, 2, 1));
        JScrollPane resultsPane = new JScrollPane(results);
        resultsPane.setMinimumSize(new Dimension(100, 10));
        add(resultsPane, new SimpleGridBagConstraints(0, 1, 2, 2));

        //setPreferredSize((new Dimension(100, (int) getPreferredSize().getHeight())));
        analyzer = new WhitespaceAnalyzer();
        updateCanvas();
        //analyzer.
    }
        """
        self._indices = {}
        self._analyzer = None
        self._diffCorpora = dict()
        self._goldCorpora = goldLoader  # XXX Should be set
        self._guessCorpora = guessLoader  # XXX Should be set
        self._indexSearcher = None

        self._guess = guessLoader
        self._gold = goldLoader
        self._scene = scene
        self._canvas = canvas
        # self._canvas = NLPCanvas(ui)
        self._edgeTypeFilter = edgeTypeFilter

        self._instance = None
        self._ui = ui

        # guessLoader.addChangeListener(this);
        # goldLoader.addChangeListener(this);

        self.canvas.renderer.set_edge_type_order("pos", 0)
        self.canvas.renderer.set_edge_type_order("chunk (BIO)", 1)
        self.canvas.renderer.set_edge_type_order("chunk", 2)
        self.canvas.renderer.set_edge_type_order("ner (BIO)", 2)
        self.canvas.renderer.set_edge_type_order("ner", 3)
        self.canvas.renderer.set_edge_type_order("sense", 4)
        self.canvas.renderer.set_edge_type_order("role", 5)
        self.canvas.renderer.set_edge_type_order("phase", 5)

        # results = []
        self._spinner = ui.spinBox

        def indexChanged():
            self.updateCanvas()
        self._spinner.valueChanged.connect(indexChanged)

        if self._goldCorpora is not None:
            if self._guessCorpora is None:
                index = len(self._goldCorpora)
            else:
                index = min(len(self._goldCorpora), len(self._guessCorpora))
            self._spinner.setMaximum(index)
            self._ui.SpinBoxLabel.setText("of " + str(index))
            self._spinner.setValue(1)
            self._spinner.setMinimum(1)
        else:
            self._spinner.setValue(0)
            self._spinner.setMinimum(0)
            self._ui.SpinBoxLabel.setText("of 0")

        self._search = ui.searchCorpusLineEdit
        self._searchResultDictModel = {}
        self._searchResultListWidget = ui.searchResultLisWidget

        def itemClicked(item):
            i = self._searchResultListWidget.row(item)
            self._spinner.setValue(self._searchResultDictModel[i+1])
        self._searchResultListWidget.itemClicked.connect(itemClicked)

        self._searchButton = ui.searchButton
        self._searchButton.clicked.connect(self.searchCorpus)

        self.updateCanvas()

    """
     * Returns the panel that contains the spinner to set the instance nr.
     *
     * @return the panel that contains the spinner to set the instance nr.
    """
    # public JPanel getSpinnerPanel() {
    #     return spinnerPanel;
    # }

    """
     * Searches the current corpus using the search terms in the search field.
    """
    """ Original version...  check the Python implementation...
    private void searchCorpus() {
        if (search.getText().trim().equals("")) return;
        try {
            indexSearcher = guess.getSelected() != null ?
                getIndex(getDiffCorpus(gold.getSelected(), guess.getSelected())) :
                getIndex(gold.getSelected());
            //System.out.println("Searching...");
            QueryParser parser = new QueryParser("Word", analyzer);
            Query query = parser.parse(search.getText());
            Hits hits = indexSearcher.search(query);
            Highlighter highlighter = new Highlighter(new QueryScorer(query));
            DefaultListModel model = new DefaultListModel();
            for (int i = 0; i < hits.length(); i++) {
                Document hitDoc = hits.doc(i);
                int nr = Integer.parseInt(hitDoc.get("<nr>"));
                //System.out.println(hitDoc.get("<nr>"));
                String best = null;
                for (Object field : hitDoc.getFields()) {
                    Field f = (Field) field;
                    best = highlighter.getBestFragment(analyzer, f.name(), hitDoc.get(f.name()));
                    if (best != null) break;
                }
                if (best != null)
                    model.addElement(new Result(nr, "<html>" + nr + ":" + best + "</html>"));
                //System.out.println(highlighter.getBestFragment(analyzer, "Word", hitDoc.get("Word")));
                //assertEquals("This is the text to be indexed.", hitDoc.get("fieldname"));
            }
            results.setModel(model);
            repaint();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    """
    def searchCorpus(self):  # XXX I'M NOT SURE IF THIS IS GOOD!
        text = self._search.text()
        self._searchResultListWidget.clear()
        self._searchResultDictModel.clear()
        counter = 1
        if text == "":
            self._searchResultListWidget.clear()
            return
        for index in range(self._spinner.minimum()-1, self._spinner.maximum()):
            if index not in self._indices:
                if self._gold is not None:
                    if self._guess is None:
                        self._indices[index] = self._goldCorpora[index]
                    else:
                        self._indices[index] = self.getDiffCorpus(self._goldCorpora[index], self._guessCorpora[index])
            instance = self._indices[index]
            sentence = ""
            for token in instance.tokens:
                word = token.get_property(TokenProperty("Word"))
                if sentence == "":
                    sentence += " " + word
                else:
                    sentence += " " + word
            if text in sentence:
                self._searchResultDictModel[counter] = index+1
                self._searchResultListWidget.addItem(str(index+1) + ":" + sentence)
                counter += 1

    """
     * Returns an IndexSearcher for the given corpus. A new one is created if not yet existent.
     *
     * @param corpus the corpus to get an IndexSearcher for.
     * @return the IndexSearcher for the given corpus.
    """
    def getIndex(self, corpus: [NLPInstance]):
        index = self._indices.get(corpus)
        if index is None:
            index = self.createIndex(corpus)
            self._indices[corpus] = index
        return index

    """
     * Creates an IndexSearcher for the given corpus that allows us to search the corpus efficiently for keywords in the
     * token properties and edges.
     *
     * @param corpus the corpus to create the IndexSearcher for.
     * @return An IndexSearcher for the given corpus.
    """
    def createIndex(self, corpus: [NLPInstance]):
        """
        try {
            System.err.println("Creating Index");
            RAMDirectory directory = new RAMDirectory();
            IndexWriter iwriter;
            iwriter = new IndexWriter(directory, analyzer, true);
            iwriter.setMaxFieldLength(25000);

            int nr = 0;
            for (NLPInstance instance : corpus) {
                Document doc = new Document();
                HashMap<TokenProperty, StringBuffer>
                    sentences = new LinkedHashMap<TokenProperty, StringBuffer>();
                for (Token token : instance.getTokens()) {
                    for (TokenProperty p : token.getPropertyTypes()) {
                        StringBuffer buffer = sentences.get(p);
                        if (buffer == null) {
                            buffer = new StringBuffer();
                            sentences.put(p, buffer);
                        }
                        if (token.getIndex() > 0) buffer.append(" ");
                        buffer.append(token.getProperty(p));
                    }
                }
                for (TokenProperty p : sentences.keySet()) {
                    doc.add(new Field(p.getName(), sentences.get(p).toString(),
                        Field.Store.YES, Field.Index.TOKENIZED));
                }

                //edges
                HashMap<String, StringBuffer> edges = new HashMap<String, StringBuffer>();
                StringBuffer types = new StringBuffer();
                for (Edge e : instance.getEdges()) {
                    String prefix = e.getTypePrefix();
                    StringBuffer prefixBuffer = edges.get(prefix);
                    types.append(prefix).append(" ");
                    if (prefixBuffer == null) {
                        prefixBuffer = new StringBuffer();
                        edges.put(prefix, prefixBuffer);
                    }
                    prefixBuffer.append(e.getLabel()).append(" ");
                    String postfix = e.getTypePostfix();
                    if (postfix != null) {
                        types.append(postfix).append(" ");
                        StringBuffer postfixBuffer = edges.get(postfix);
                        if (postfixBuffer == null) {
                            postfixBuffer = new StringBuffer();
                            edges.put(postfix, postfixBuffer);
                        }
                        postfixBuffer.append(e.getLabel()).append(" ");
                    }
                }

                doc.add(new Field("types", types.toString(), Field.Store.YES, Field.Index.TOKENIZED));

                for (String type : edges.keySet()) {
                    doc.add(new Field(type, edges.get(type).toString(), Field.Store.YES, Field.Index.TOKENIZED));
                }

                //for (DependencyEdge e : instance.getTokens())
                doc.add(new Field("<nr>", String.valueOf(nr), Field.Store.YES, Field.Index.UN_TOKENIZED));

                System.err.print(".");
                iwriter.addDocument(doc);
                nr++;
            }
            System.err.println();
            iwriter.optimize();
            iwriter.close();
            return new IndexSearcher(directory);
        } catch (IOException e) {
            throw new RuntimeException("Couldn't build the index");
        }

    }
    """
        return self, corpus

    """
     * Updates the canvas based on the current state of the navigator and the corpus loaders.
    """
    def updateCanvas(self):  # XXX MISSING STUFF HERE!
        index = self._spinner.value() - 1
        if self._gold is not None:
            # searchButton.setEnabled(true);
            # search.setEnabled(true);
            # spinner.setEnabled(true);
            # results.setEnabled(true);
            if self._guess is None:
                if index in self._indices:
                    self._instance = self._indices[index]
                else:
                    self._instance = self._goldCorpora[index]
                    self._indices[index] = self._instance
                # indexSearcher = getIndex(gold.getSelected());
                # canvas.setNLPInstance(gold.getSelected().get(index));
                # canvas.updateNLPGraphics();
            else:
                if index in self._indices:
                    self._instance = self._indices[index]
                else:
                    self._instance = self.getDiffCorpus(self._gold, self._guess)[index]
                    self._indices[index] = self._instance
                self._canvas.renderer.set_edge_type_color("FN", (000, 000, 255))  # Blue
                self._canvas.renderer.set_edge_type_color("FP", (255, 000, 000))  # Red
                self._canvas.set_nlp_instance(self._instance)
                self._canvas.update_nlp_graphics()
        else:
            """
            searchButton.setEnabled(false);
            search.setEnabled(false);
            spinner.setEnabled(false);
            spinner.setValue(0);
            searchButton.setEnabled(false);
            results.setEnabled(false);
            ofHowMany.setText(" of 1");
            """

            example = NLPInstance()
            example.add_token().add_named_prop("Word", "[root]").add_named_prop("Index", "0")
            example.add_token().add_named_prop("Word", "Add").add_named_prop("Index", "1")
            example.add_token().add_named_prop("Word", "a").add_named_prop("Index", "2")
            example.add_token().add_named_prop("Word", "gold").add_named_prop("Index", "3")
            example.add_token().add_named_prop("Word", "corpus").add_named_prop("Index", "4")
            example.add_token().add_named_prop("Word", "!").add_named_prop("Index", "5")
            example.add_dependency(0, 1, "ROOT", "dep")
            example.add_dependency(0, 5, "PUNC", "dep")
            example.add_dependency(1, 4, "OBJ", "dep")
            example.add_dependency(4, 2, "DET", "dep")
            example.add_dependency(4, 3, "MOD", "dep")
            example.add_dependency(1, 4, "A1", "role")
            example.add_span(1, 1, "add.1", "sense")
            self._canvas.set_nlp_instance(example)
            self._edgeTypeFilter.add_allowed_edge_type("dep")
            self._edgeTypeFilter.add_allowed_edge_type("role")
            self._edgeTypeFilter.add_allowed_edge_type("sense")
            self._edgeTypeFilter.add_allowed_edge_type("ner")
            self._edgeTypeFilter.add_allowed_edge_type("chunk")
            self._edgeTypeFilter.add_allowed_edge_type("pos")
            self._edgeTypeFilter.add_allowed_edge_type("align")
            self._edgeTypeFilter.add_allowed_edge_property('eval_status_FP')
            self._edgeTypeFilter.add_allowed_edge_property('eval_status_FN')
            self._edgeTypeFilter.add_allowed_edge_property('eval_status_Match')

            self._canvas.renderer.set_edge_type_order("pos", 0)
            self._canvas.renderer.set_edge_type_order("chunk (BIO)", 1)
            self._canvas.renderer.set_edge_type_order("chunk", 2)
            self._canvas.renderer.set_edge_type_order("ner (BIO)", 2)
            self._canvas.renderer.set_edge_type_order("ner", 3)
            self._canvas.renderer.set_edge_type_order("sense", 4)
            self._canvas.renderer.set_edge_type_order("role", 5)
            self._canvas.renderer.set_edge_type_order("phrase", 5)
            self._canvas.update_nlp_graphics()
