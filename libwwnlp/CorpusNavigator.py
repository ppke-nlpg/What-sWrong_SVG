#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.NLPCanvas import NLPCanvas
from libwwnlp.model.nlp_instance import NLPInstance, nlp_diff


class CorpusNavigator:
    """
      A CorpusNavigator allows the user to navigate through a corpus (or a diffed corpus) and pick one NLP instance to
      draw (or one difference of two NLPInstance objects in terms of their edges). The CorpusNavigator also allows us to
      search a corpus for keywords by using the Lucene IR engine. The instances that match the user's query are
      presented in a list and one of them can then be picked to be rendered. The CorpusNavigator has also a spinner
      panel that allows to go through this corpus by index. This spinner is not part of the navigator panel and can be
      placed anywhere.
    """
    """
     * The loader for guess instances.
    """
    def __init__(self, canvas: NLPCanvas, gold_loader=None, guess_loader=None, instance_filter=None, spinner=None):
        """
         * Creates a new CorpusNavigator.
         *
         * @param canvas         the canvas to control.
         * @param gold_loader     the gold corpora.
         * @param guess_loader    the guess corpora.
         * @param instance_filter the Filter we need when no corpus is selected and a example sentence is chosen and
                                  passed to the NLPCanvas.
        """

        """
         * Creates an IndexSearcher for the given corpus that allows us to search the corpus efficiently for
         * keywords in the token properties and edges.
         * A Search result consisting of the instance index and a text snippet that indicates the position in the
         * instance where they key terms were found.
        """
        self._indices = {}
        self._diffCorpora = {}

        # TODO: What is the difference in _gold and _gold_corpora ?
        self._gold_corpora = gold_loader  # XXX Should be set
        self._guess_corpora = guess_loader  # XXX Should be set
        self._gold = gold_loader
        self._guess = guess_loader

        self._canvas = canvas
        self._instance_filter = instance_filter
        self._instance = None

        """
        self._canvas.renderer.set_edge_type_order("pos", 0)
        self._canvas.renderer.set_edge_type_order("chunk (BIO)", 1)
        self._canvas.renderer.set_edge_type_order("chunk", 2)
        self._canvas.renderer.set_edge_type_order("ner (BIO)", 2)
        self._canvas.renderer.set_edge_type_order("ner", 3)
        self._canvas.renderer.set_edge_type_order("sense", 4)
        self._canvas.renderer.set_edge_type_order("role", 5)
        self._canvas.renderer.set_edge_type_order("phase", 5)
        """

        self._searchResultDictModel = {}
        self.update_canvas(spinner)

    def corpus_added(self, corpus: [NLPInstance], src: [NLPInstance]):
        """
         * Adds the corpus to the corresponding internal set of corpora.
         *
         * @param corpus the corpus to add.
         * @param src    the source loader.
        """
        if src == self._gold:
            self._gold_corpora.append(corpus)
            # indices[corpus] = self.createIndex(corpus)
        else:
            self._guess_corpora.append(corpus)
            # indices[corpus] = self.createIndex(corpus)

    def corpus_removed(self, corpus: [NLPInstance], src: [NLPInstance]):
        """
         * Removes the corpus and all diff corpora that compare the given corpus
         *
         * @param corpus the corpus to remove.
         * @param src    the loader that removed the corpus.
        """
        if src == self._gold:
            self._gold_corpora.remove(corpus)
            del self._indices[corpus]
            for c in self._guess_corpora:
                self.remove_diff_corpus(corpus, c)
        else:
            self._guess_corpora.remove(corpus)
            del self._indices[corpus]
            for c in self._gold_corpora:
                self.remove_diff_corpus(corpus, c)

    @staticmethod
    def get_diff_corpus(gold: [NLPInstance], guess: [NLPInstance]) -> [NLPInstance]:  # XXX
        """
         * Returns a difference corpus between two corpora. This difference corpus is calculated if it hasn't been
         * calculated before.
         *
         * @param gold  the gold corpus.
         * @param guess the guess corpus.
         * @return the difference corpus.
        """
        # diff_corpus = self._diffCorpora.get((gold, guess))
        diff_corpus = None
        if diff_corpus is None:
            diff_corpus = []
            # self._diffCorpora[(gold, guess)] = diff_corpus
        for i in range(min(len(gold), len(guess))):
            diff_corpus.append(nlp_diff(gold[i], guess[i], 'eval_status_Match',  'eval_status_FN', 'eval_status_FP'))
        # indices.put(diff_corpus, createIndex(diff_corpus))
        return diff_corpus
        # return nlp_diff(gold, guess)  # XX Current Working

    def remove_diff_corpus(self, gold: [NLPInstance], guess: [NLPInstance]):
        """
         * Removes the difference corpus for the given corpus pair.
         *
         * @param gold  the gold corpus.
         * @param guess the guess corpus.
        """
        pair = (gold, guess)
        diff_corpus = self._diffCorpora.get(pair)
        if diff_corpus is not None:
            del self._diffCorpora[pair]
            del self._indices[diff_corpus]

    def search_corpus(self, text, search_result_widget, spinner):

        """
         * Searches the current corpus using the search terms in the search field. (Currently words)
        """
        search_result_widget.clear()
        search_result_widget.clear()
        if text == "":
            return
        counter = 1
        for index in range(spinner.minimum()-1, spinner.maximum()):
            if index not in self._indices:
                if self._gold is not None:
                    if self._guess is None:
                        self._indices[index] = self._gold_corpora[index]
                    else:
                        self._indices[index] = self.get_diff_corpus(self._gold_corpora[index],
                                                                    self._guess_corpora[index])
                elif self._guess is not None:
                    self._indices[index] = self._guess_corpora[index]
                else:
                    raise ValueError  # No corpora given
            instance = self._indices[index]
            sentence = ' '.join(token.get_property_value("Word") for token in instance.tokens)

            if text in sentence:
                self._searchResultDictModel[counter] = index + 1
                search_result_widget.addItem('{0}:{1}'.format(index + 1, sentence))
                counter += 1

    def update_canvas(self, spinner):  # XXX MISSING STUFF HERE!
        """
         * Updates the canvas based on the current state of the navigator and the corpus loaders.
        """
        index = spinner.value() - 1
        if self._gold is not None:
            if self._guess is None:
                if index in self._indices:
                    self._instance = self._indices[index]
                else:
                    self._instance = self._gold_corpora[index]
                    self._indices[index] = self._instance
                # indexSearcher = getIndex(gold.getSelected());
                # canvas.setNLPInstance(gold.getSelected().get(index));
                # canvas.updateNLPGraphics();
            else:
                if index in self._indices:
                    self._instance = self._indices[index]
                else:
                    self._instance = self.get_diff_corpus(self._gold, self._guess)[index]
                    self._indices[index] = self._instance
                self._canvas.set_nlp_instance(self._instance)
        else:

            example = NLPInstance()
            example.add_token().add_property('Word', '[root]').add_property('Index', '0')
            example.add_token().add_property('Word', 'Add').add_property('Index', '1')
            example.add_token().add_property('Word', 'a').add_property('Index', '2')
            example.add_token().add_property('Word', 'gold').add_property('Index', '3')
            example.add_token().add_property('Word', 'corpus').add_property('Index', '4')
            example.add_token().add_property('Word', '!').add_property('Index', '5')
            example.add_dependency(0, 1, 'ROOT', 'dep')
            example.add_dependency(0, 5, 'PUNC', 'dep')
            example.add_dependency(1, 4, 'OBJ', 'dep')
            example.add_dependency(4, 2, 'DET', 'dep')
            example.add_dependency(4, 3, 'MOD', 'dep')
            example.add_dependency(1, 4, 'A1', 'role')
            example.add_dependency(1, 1, 'add.1', 'sense')
            self._canvas.set_nlp_instance(example)
            self._instance_filter.allowed_edge_types = set()
            """
            self._instance_filter.allowed_edge_types.add('dep')
            self._instance_filter.allowed_edge_types.add('role')
            self._instance_filter.allowed_edge_types.add('sense')
            self._instance_filter.allowed_edge_types.add('ner')
            self._instance_filter.allowed_edge_types.add('chunk')
            self._instance_filter.allowed_edge_types.add('pos')
            self._instance_filter.allowed_edge_types.add('align')
            """
            self._instance_filter.allowed_edge_properties.add('eval_status_FP')
            self._instance_filter.allowed_edge_properties.add('eval_status_FN')
            self._instance_filter.allowed_edge_properties.add('eval_status_Match')

            # TODO: Find the actual place of edge_tp
            """
            self._canvas.renderer.set_edge_type_order('pos', 0)
            self._canvas.renderer.set_edge_type_order('chunk (BIO)', 1)
            self._canvas.renderer.set_edge_type_order('chunk', 2)
            self._canvas.renderer.set_edge_type_order('ner (BIO)', 2)
            self._canvas.renderer.set_edge_type_order('ner', 3)
            self._canvas.renderer.set_edge_type_order('sense', 4)
            self._canvas.renderer.set_edge_type_order('role', 5)
            self._canvas.renderer.set_edge_type_order('phrase', 5)
            """

        self._canvas.fire_instance_changed()
        self._canvas.update_nlp_graphics()
