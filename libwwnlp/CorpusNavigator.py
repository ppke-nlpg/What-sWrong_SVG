#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import basename

from ioFormats.TabProcessor import CoNLL2000, CoNLL2002, CoNLL2003, CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, \
    CoNLL2009, MaltTab
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
    def __init__(self, canvas: NLPCanvas):
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
        self._gold_corpora = {}
        self._guess_corpora = {}

        self._selected_gold = None
        self._selected_guess = None

        self.min_length = 0
        self.max_length = 0

        # Not used
        self._cached_instances = {}
        self._diffCorpora = {}

        self._canvas = canvas
        self._instance = None

        # TODO
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
        self.known_corpus_formats = {'CoNLL2000': CoNLL2000(),
                                     'CoNLL2002': CoNLL2002(),
                                     'CoNLL2003': CoNLL2003(),
                                     'CoNLL2004': CoNLL2004(),
                                     'CoNLL2005': CoNLL2005(),
                                     'CoNLL2006': CoNLL2006(),
                                     'CoNLL2008': CoNLL2008(),
                                     'CoNLL2009': CoNLL2009(),
                                     'MaltTab': MaltTab()
                                     }

        self._searchResultDictModel = {}

    def add_corpus(self, corpus_path, corpus_format, corpus_type):
        """Adds the corpus to the corresponding internal set of corpora."""
        if corpus_type == 'gold':
            corp_type_dict = self._gold_corpora
        elif corpus_type == 'guess':
            corp_type_dict = self._guess_corpora
        else:
            raise ValueError
        corpus = self.known_corpus_formats[corpus_format].load(corpus_path, 0, 200)  # Load first 200 sentence
        corp_name = basename(corpus_path)

        if corp_name not in corp_type_dict:
            corp_type_dict[basename(corpus_path)] = corpus
            # indices[corpus] = self.createIndex(corpus)  # TODO

    def remove_corpus(self, corpus_type, corpus_name):
        """Removes the corpus and all diff corpora that compare the given corpus"""
        if corpus_type == 'gold':
            corp_type_dict = self._gold_corpora
            self._selected_gold = None
        elif corpus_type == 'guess':
            corp_type_dict = self._guess_corpora
            self._selected_guess = None
        else:
            raise ValueError

        del corp_type_dict[corpus_name]
        # del self._cached_instances[corpus_name]  # TODO
        # for c in corp_type_dict:
        #     self.remove_diff_corpus(corpus_name, c)

    def select_gold(self, corp_name):
        if corp_name in self._gold_corpora:
            self._selected_gold = corp_name
            self.update_length()
        else:
            raise ValueError

    def select_guess(self, corp_name):
        if corp_name in self._guess_corpora:
            self._selected_guess = corp_name
            self.update_length()
        else:
            raise ValueError

    def update_length(self):
        self.min_length = 0
        self.max_length = 0
        if self._selected_gold is not None:
            gold_length = len(self._gold_corpora[self._selected_gold])
            if self._selected_guess is not None:
                guess_length = len(self._guess_corpora[self._selected_guess])
                self.max_length = min(gold_length, guess_length)
            else:
                self.max_length = gold_length
        if self.max_length > 0:
            self.min_length = 1

    def search_corpus(self, text):
        """Searches the current corpus using the search terms in the search field. (Currently words)"""
        ret = {}
        if len(text) > 0:
            gold = None
            guess = None
            if self._selected_gold is not None:
                gold = self._gold_corpora[self._selected_gold]
            if self._selected_guess is not None:
                guess = self._guess_corpora[self._selected_guess]

            # TODO: Do this properly
            if gold is not None and guess is not None:
                to_search = lambda ind: nlp_diff(gold[ind], guess[ind], 'eval_status_Match',  'eval_status_FN',
                                                 'eval_status_FP')
            elif gold is not None:
                to_search = lambda ind: gold[ind]
            else:
                raise ValueError  # No corpora given

            counter = 1
            ret = {}
            for index in range(self.min_length, self.max_length+1):
                sentence = ' '.join(token.get_property_value('Word') for token in to_search(index).tokens)
                if text in sentence:
                    ret[counter] = index + 1
                    counter += 1
        return ret

    def update_canvas(self, curr_sent_index):
        """ Updates the canvas based on the current state of the navigator."""
        if self._selected_gold is not None:
            if self._selected_guess is None:
                instance = self._gold_corpora[self._selected_gold][curr_sent_index]
            else:
                instance = nlp_diff(self._gold_corpora[self._selected_gold][curr_sent_index],
                                    self._guess_corpora[self._selected_guess][curr_sent_index],
                                    'eval_status_Match',  'eval_status_FN', 'eval_status_FP')
            self._canvas.set_nlp_instance(instance)
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
            self._canvas.filter.allowed_edge_types = set()
            self._canvas.filter.allowed_edge_types.add('dep')
            self._canvas.filter.allowed_edge_types.add('role')
            self._canvas.filter.allowed_edge_types.add('sense')
            self._canvas.filter.allowed_edge_types.add('ner')
            self._canvas.filter.allowed_edge_types.add('chunk')
            self._canvas.filter.allowed_edge_types.add('pos')
            self._canvas.filter.allowed_edge_types.add('align')

            self._canvas.filter.allowed_edge_properties.add('eval_status_FP')
            self._canvas.filter.allowed_edge_properties.add('eval_status_FN')
            self._canvas.filter.allowed_edge_properties.add('eval_status_Match')

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
