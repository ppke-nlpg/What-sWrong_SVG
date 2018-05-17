#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from ioformats.tab_processor import CoNLL2000, CoNLL2002, CoNLL2003, CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, \
    CoNLL2009, MaltTab
from ioformats.other_formats import GizaAlignmentFormat, GaleAlignmentFormat, LispSExprFormat,\
    BioNLP2009SharedTaskFormat, TheBeastFormat
from libwwnlp.nlp_canvas import NLPCanvas
from libwwnlp.model.nlp_instance import NLPInstance, nlp_diff


class CorpusNavigator:
    """
      A CorpusNavigator allows the user to navigate through a corpus (or a diffed corpus) and pick one NLP instance to
      draw (or one difference of two NLPInstance objects in terms of their edges). The CorpusNavigator also allows us to
      search a corpus for keywords. The instances that match the user's query are presented in a list and one of them
       can then be picked to be rendered.
      The CorpusNavigator handles also a spinner panel that allows to go through this corpus by index.
    """
    def __init__(self, canvas: NLPCanvas=NLPCanvas()):
        """Creates a new CorpusNavigator."""
        self._gold_corpora = {}
        self._guess_corpora = {}

        self._selected_gold = None
        self._selected_guess = None

        self.min_length = 0
        self.max_length = 0

        self.canvas = canvas

        self.canvas.renderer.params['span.orders'] = {'pos': 0, 'chunk (BIO)': 1, 'chunk': 2, 'ner (BIO)': 2, 'ner': 3,
                                                      'sense': 4, 'role': 5, 'phase': 5}
        self.known_corpus_formats = {'CoNLL2000': CoNLL2000(),
                                     'CoNLL2002': CoNLL2002(),
                                     'CoNLL2003': CoNLL2003(),
                                     'CoNLL2004': CoNLL2004(),
                                     'CoNLL2005': CoNLL2005(),
                                     'CoNLL2006': CoNLL2006(),
                                     'CoNLL2008': CoNLL2008(),
                                     'CoNLL2009': CoNLL2009(),
                                     'MaltTab': MaltTab(),
                                     'Giza Alingment Format': GizaAlignmentFormat(),
                                     'Gale Alingment Format': GaleAlignmentFormat(),
                                     'The Beast Format': TheBeastFormat(),
                                     'Lisp S-expr Format': LispSExprFormat(),
                                     'BioNLP2009 Shared Task Format': BioNLP2009SharedTaskFormat()
                                     }

    def add_corpus(self, corpus_path: str, corpus_format: str, corpus_type: str, min_sent=0, max_sent=200):
        """Adds the corpus to the corresponding internal set of corpora."""
        if corpus_type == 'gold':
            corp_type_dict = self._gold_corpora
        elif corpus_type == 'guess':
            corp_type_dict = self._guess_corpora
        else:
            raise ValueError
        corpus = self.known_corpus_formats[corpus_format].load(corpus_path, min_sent, max_sent)
        corp_name = os.path.basename(corpus_path)

        if corp_name not in corp_type_dict:
            corp_type_dict[os.path.basename(corpus_path)] = corpus

    def remove_corpus(self, corpus_type: str, corpus_name: str):
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

    def select_gold(self, corp_name: str):
        if corp_name in self._gold_corpora:
            self._selected_gold = corp_name
            self.update_length()
        else:
            raise ValueError

    def select_guess(self, corp_name: str):
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

    def iter_gold(self):
        if self._selected_gold is not None and self._selected_gold in self._gold_corpora:
            return iter(self._gold_corpora[self._selected_gold])

    def iter_guess(self):
        if self._selected_guess is not None and self._selected_guess in self._guess_corpora:
            return iter(self._guess_corpora[self._selected_guess])

    def search_corpus(self, text: str):
        """Searches the current corpus using the search terms in the search field for
            keywords in the token properties and edges. (Currently words)
            A Search result consisting of the instance index and a text snippet that indicates the position in the
            instance where they key terms were found.
        """
        ret = {}
        if len(text) > 0:
            gold = None
            guess = None
            if self._selected_gold is not None:
                gold = self._gold_corpora[self._selected_gold]
            if self._selected_guess is not None:
                guess = self._guess_corpora[self._selected_guess]

            if gold is not None and guess is not None:
                def to_search(ind):
                    return nlp_diff(gold[ind], guess[ind], 'eval_status_Match', 'eval_status_FN', 'eval_status_FP')
            elif gold is not None:
                def to_search(ind):
                    return gold[ind]
            else:
                raise ValueError  # No gold corpora given

            counter = 1
            ret = {}
            for index in range(self.min_length-1, self.max_length):
                sentence = ' '.join(token.get_property_value('Word') for token in to_search(index).tokens)
                if text in sentence:
                    ret[counter] = (index + 1, sentence)
                    counter += 1
        return ret

    def update_canvas(self, curr_sent_index: int):
        """ Updates the canvas based on the current state of the navigator."""
        if self._selected_gold is not None:
            if self._selected_guess is not None:
                instance = nlp_diff(self._gold_corpora[self._selected_gold][curr_sent_index],
                                    self._guess_corpora[self._selected_guess][curr_sent_index],
                                    'eval_status_Match',  'eval_status_FN', 'eval_status_FP')
            else:
                instance = self._gold_corpora[self._selected_gold][curr_sent_index]
            self.canvas.set_nlp_instance(instance)
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
            self.canvas.set_nlp_instance(example)
            self.canvas.filter.allowed_edge_types = set()
            self.canvas.filter.allowed_edge_types.add('dep')
            self.canvas.filter.allowed_edge_types.add('role')
            self.canvas.filter.allowed_edge_types.add('sense')
            self.canvas.filter.allowed_edge_types.add('ner')
            self.canvas.filter.allowed_edge_types.add('chunk')
            self.canvas.filter.allowed_edge_types.add('pos')
            self.canvas.filter.allowed_edge_types.add('align')

            self.canvas.filter.allowed_edge_properties.add('eval_status_FP')
            self.canvas.filter.allowed_edge_properties.add('eval_status_FN')
            self.canvas.filter.allowed_edge_properties.add('eval_status_Match')

            self.canvas.renderer.params['span.orders'] = {'pos': 0, 'chunk (BIO)': 1, 'chunk': 2, 'ner (BIO)': 2,
                                                          'ner': 3, 'sense': 4, 'role': 5, 'phase': 5}
        self.canvas.fire_instance_changed()
