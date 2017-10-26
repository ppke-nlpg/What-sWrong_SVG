#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import glob
import os.path
import sys

from ioFormats.CorpusFormat import CorpusFormat
from libwwnlp.model.edge import EdgeRenderType
from libwwnlp.model.nlp_instance import NLPInstance, RenderType


def check_eof(line):
    if len(line) == 0:
        raise EOFError
    return line


class GizaAlignmentFormat(CorpusFormat):
    def __init__(self):
        self.ROPERTYSUFFIX_REVERSE = ".giza.reverse"

        """"
        If selected, the source segments are treated as the target segments and vice versa.
        To compare a src-to-tgt alignment to a tgt-to-src alignment of the same corpus, one
        or the other (but not both) should be read in in reverse."""
        self._reverseCheckBox = False  # JCheckBox
        self._name = "Giza Alignment"

    def __str__(self):
        return self._name

    @property
    def longName(self):
        ret = self._name
        if self._reverseCheckBox:
            ret += " (reverse)"
        return ret

    @property
    def name(self):
        return self._name

    def load(self, file_name, from_sentence_nr: int, to_sentence_nr: int):
        with open(file_name, encoding='UTF-8') as reader:
            """
             * Skip past the next aligned segment pair in the given reader.
             *
             * @throws EndOfInputException if there was no aligned segment pair to skip because we're
             *         already at the end of the given reader
            """
            # There are three lines per segment pair.
            for _ in range(3 * from_sentence_nr):
                try:
                    check_eof(reader.readline())
                except EOFError:
                    break

            result = []  # ArrayList<NLPInstance>
            for i in range(from_sentence_nr, to_sentence_nr):
                try:
                    """
                     * @return the next aligned segment pair, loaded from the given reader
                     *
                     * @throws EndOfInputException if no aligned segment pair could be loaded because we're already
                     *         at the end of the given reader
                    """
                    """
                     There are three lines per segment pair.

                     The first line gives the segment index, source and target lengths (which we can count
                     ourselves), and an alignment score. Skip this line (or throw an exception if there are no
                     more lines).
                    """
                    check_eof(reader.readline())

                    tokens = []
                    """
                     * a list of one-based {source-token-index, target-token-index} pairs
                    """
                    alignment_edges = []  # [(int, int)]

                    # String line;

                    # The second line contains the source segment, tokenized, with no adornment.
                    tokens.append(check_eof(reader.readline()).strip().split())
                    tokens.append([])

                    """
                     The third line contains the tokens of the target segment, starting with the pseudo-token
                     "NULL", with each token followed by a whitespace-delimited list (in curly braces nested
                     in parentheses) of the 1-based indices of the source tokens aligned to it, e.g.:

                     NULL ({ 2 }) customization ({ 1 }) of ({ }) tasks ({ 3 4 })
                    """
                    # Strip newline and space and reappend space for later regex
                    line = check_eof(reader.readline()).rstrip() + " "

                    # start from index 1 to skip the NULL token and empty string at the EOL
                    for ind, token_with_aligned_indices in enumerate(line.split(" }) ")[1:-1], start=1):
                        splitted1, splitted2 = token_with_aligned_indices.split(" ({")
                        tokens[1].append(splitted1)
                        aligned_index_list_as_string = splitted2.strip()

                        """
                         we need to handle the empty list specially, because the split method on the empty
                         string returns a singleton array containing the empty string, but here an empty
                         array is what we want
                        """
                        aligned_indices_as_strings = []
                        if len(aligned_index_list_as_string) > 0:
                            aligned_indices_as_strings = aligned_index_list_as_string.split(" ")

                        for aligned_index_as_string in aligned_indices_as_strings:
                            alignment_edges.append((int(aligned_index_as_string), ind))

                    # now we're ready to make the NLPInstance
                    instance = NLPInstance(render_type=RenderType.alignment)
                    if self._reverseCheckBox:
                        self.make_instance(instance, tokens[1], tokens[0], ((e2, e1) for e1, e2 in alignment_edges))
                    else:
                        self.make_instance(instance, tokens[0], tokens[1], alignment_edges)

                    result.append(instance)
                except EOFError:
                    break

        return result

    @staticmethod
    def make_instance(instance, tokens1, tokens2, alignment_edges):
        for token in tokens1:
            instance.add_token().add_property("word", token)
        instance.split_points.append(len(instance.tokens))
        for token in tokens2:
            instance.add_token().add_property("word", token)
        for alignmentEdge1, alignmentEdge2 in alignment_edges:
            from_edge = alignmentEdge1 - 1
            to_edge = len(tokens1) + alignmentEdge2 - 1
            instance.add_edge(from_edge, to_edge, "align", "align")

    def loadProperties(self, properties, prefix):
        pass

    def saveProperties(self, properties, prefix):
        pass

    def setMonitor(self, monitor):
        pass

    def accessory(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class GaleAlignmentFormat(CorpusFormat):
    """

     * The GaleAlignmentFormat reads bilingual alignment data in a xml-like format. The source tag element contains the
     * tokenized source sentence, the translation element contains the target tokenized sentence. The matrix element
     * contains a matrix in which the first row and first column indicate which tokens are null-aligned, and the
     * remainder of the matrix is simply the alignment matrix where each column corresponds to a source token, and each
     * row corresponds to a target token. The seg element can contain the id of the sentence, but doesn't have to.
     * It's only important that there is a seg element for each sentence.
     * <pre>
     * <p/>
     * &lt;seg id=1&gt
     * <p/>
     * &lt;source&gt;Ich habe den Fehler in meiner Sprachverarbeitung gefunden
     * .&lt;/source&gt
     * <p/>
     * &lt;translation&gt;I've found the error in my NLP .&lt;/translation&gt
     * <p/>
     * &lt;matrix&gt
     * <p/>
     * 0 0 0 0 0 0 0 0 0 0
     * 0 1 1 0 0 0 0 0 0 0
     * 0 0 0 0 0 0 0 0 1 0
     * 0 0 0 1 0 0 0 0 0 0
     * 0 0 0 0 1 0 0 0 0 0
     * 0 0 0 0 0 1 0 0 0 0
     * 0 0 0 0 0 0 1 0 0 0
     * 0 0 0 0 0 0 0 1 0 0
     * 0 0 0 0 0 0 0 0 0 1
     * &lt;/matrix&gt
     * <p/>
     * &lt;seg id=2&gt
     * ...
     * <p/>
     * </pre>
     *
     * @author Sebastian Riedel
    """

    def __init__(self):
        self._name = "Gale Alignment"

    @property
    def longName(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    def load(self, file_name: str, from_sent_nr, to_sent_nr):
        """
         * Loads a corpus from a file, starting at instance <code>from</code> and ending at instance <code>to</code>
         * (exclusive). This method is required to call
         * {@link com.googlecode.whatswrong.io.CorpusFormat.Monitor#progressed(int)}
         * after each instance that was processed.
         *
         * @param file the file to load the corpus from.
         * @param from the starting instance index.
         * @param to   the end instance index.
         * @return a list of NLP instances loaded from the given file in the given interval.
         * @throws java.io.IOException if I/O goes wrong.
        """
        result = []
        with open(file_name, encoding='UTF-8') as reader:
            instance = None
            source_length = -1
            target_length = -1
            for line in reader:
                line = line.strip()
                if line.startswith("<source>"):
                    content = line.strip()[8: len(line) - 9]
                    for token in content.split():
                        instance.add_token().add_property("word", token)

                    source_length = len(instance.tokens)
                    instance.split_points.append(source_length)
                elif line.startswith("<seg"):
                    instance = NLPInstance(render_type=RenderType.alignment)
                elif line.startswith("<translation>"):
                    content = line.strip()[13: len(line) - 14]
                    for token in content.split():
                        instance.add_token().add_property("word", token)

                    target_length = len(instance.tokens) - source_length
                elif line.startswith("<matrix>"):
                    check_eof(reader.readline())
                    for tgt in range(target_length):
                        line = check_eof(reader.readline()).strip()
                        col = line.split()
                        for src in range(1, len(col)):
                            if col[src] == "1":
                                instance.add_edge(src - 1, tgt + source_length, "align", "align")

                    result.append(instance)

        return result

    def loadProperties(self, properties, prefix):
        pass

    def saveProperties(self, properties, prefix):
        pass

    def setMonitor(self, monitor):
        pass

    def accessory(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class Tree:
    def __init__(self, label: str):
        self.children = []
        self.label = label

    def __str__(self):
        return '{0}{1}'.format(self.label, self.children)

    def write_spans(self, label_type: str, tag_type: str, instance: NLPInstance):
        if self.is_tag():
            span_type = tag_type
        else:
            span_type = label_type
        instance.add_span(self.get_from(), self.get_to(), self.label, span_type)
        for tree in self.children:
            tree.write_spans(label_type, tag_type, instance)

    def write_tokens(self, word_type: str, tag_type: str, instance: NLPInstance):
        for tree in self.children:
            tree.write_tokens(word_type, tag_type, instance)

    # process from "(S ..." to closing "...)"
    @staticmethod
    def consume(tree, sexpr: str):
        stack = [tree]
        token = 0
        i = 0
        while i < len(sexpr):
            if sexpr[i] == '(':
                whitespace = sexpr.find(' ', i + 1)
                open_bracket = sexpr.find('(', i + 1)
                # label_end = whitespace
                # print("whitespace = " + whitespace)
                # print("open_bracket = " + open_bracket)
                if open_bracket != -1 and open_bracket < whitespace:
                    label_end = open_bracket
                else:
                    label_end = whitespace
                label = sexpr[i + 1: label_end]
                parent = Tree(label)
                stack[-1].children.append(parent)
                stack.append(parent)
                i = label_end
                if label_end == whitespace:
                    i += 1
            elif sexpr[i] == ')':
                stack.pop()
                i += 1
            elif sexpr[i] == ' ':
                i += 1
            else:
                word_end = sexpr.find(')', i)
                word = sexpr[i: word_end]
                stack.pop().children.append(Terminal(word, token))
                token += 1
                i = word_end + 1

    def get_from(self):
        return self.children[0].get_from()

    def get_to(self):
        return self.children[len(self.children) - 1].get_to()

    @staticmethod
    def is_terminal():
        return False

    def is_tag(self):
        return self.children[0].is_terminal()


class Terminal(Tree):
    def __init__(self, label: str, index: int):
        super().__init__(label)
        self.index = index

    def is_tag(self):
        return False

    def __str__(self):
        return self.label

    @staticmethod
    def is_terminal():
        return True

    def get_from(self):
        return self.index

    def get_to(self):
        return self.index

    def write_tokens(self, word_type: str, tag_type: str, instance: NLPInstance):
        instance.add_token().add_property(word_type, self.label).add_property("Index", str(self.index))

    def write_spans(self, label_type: str, tag_type: str, instance: NLPInstance):
        pass


class LispSExprFormat(CorpusFormat):
    def __init__(self):
        self._name = "Lisp S-Expression"
        self.word = "Word"    # Word .sexpr.word
        self.tag = "pos"     # Tag .sexpr.tag
        self.phrase = "phrase"  # Phrase .sexpr.phrase

    @property
    def longName(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    def load(self, file_name: str, from_sent_nr, to_sent_nr):

        result = []
        instance_nr = 0
        with open(file_name, encoding='UTF-8') as reader:

            for line in reader:
                line = line.strip()
                if line != "":
                    if instance_nr >= from_sent_nr:
                        tree = Tree("[root]")
                        tree.consume(tree, line)
                        tree = tree.children[0]
                        instance = NLPInstance()
                        tree.write_tokens(self.word, self.tag, instance)
                        tree.write_spans(self.phrase, self.tag, instance)
                        result.append(instance)

                    instance_nr += 1
                    if instance_nr >= to_sent_nr:
                        break

        return result

    def loadProperties(self, properties, prefix):
        pass

    def saveProperties(self, properties, prefix):
        pass

    def setMonitor(self, monitor):
        pass

    def accessory(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class BioNLP2009SharedTaskFormat(CorpusFormat):
    """
     * The BioNLP2009SharedTaskFormat loads files in the format of the BioNLP 2009 Shared Task. It allows users to
     * select a directory and enter the filename extensions for the text files and annotation files.
     * More details on the file format can be found at the
     * <a href="http://www-tsujii.is.s.u-tokyo.ac.jp/GENIA/SharedTask/">shared task website</a>.
     * See examples: http://www.nactem.ac.uk/tsujii/GENIA/SharedTask/detail.shtml#examples
    """
    def __init__(self):
        self.txtExtensionField = "txt"     # Text files .bionlp09.txt
        self.proteinExtensionField = "a1"  # Protein files .bionlp09.protein
        self.eventExtensionField = "a2"    # Event files .bionlp09.event
        self._name = "BioNLP 2009 ST"

    @property
    def longName(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    def load(self, file_name: str, from_sent_nr, to_sent_nr):
        """
         * Loads files from the given directory with the extensions specified by the text fields of the accessory.
         *
         * @param file the directory load the corpus from.
         * @param from the starting instance index.
         * @param to   the end instance index.
         * @return a list of NLP instances loaded from the given file in the given interval.
         * @throws java.io.IOException if I/O goes wrong.
        """
        result = []
        for txt_file_name in glob.glob(os.path.join(file_name, "*." + self.txtExtensionField.strip())):
            filename = os.path.abspath(txt_file_name)
            prefix = filename.rsplit(".", maxsplit=1)[0]
            protein_file_name = "{0}.{1}".format(prefix, self.proteinExtensionField.strip())
            event_file_name = "{0}.{1}".format(prefix, self.eventExtensionField.strip())
            if os.path.exists(protein_file_name) and os.path.exists(event_file_name):
                """
                 * Loads all NLPInstances in the specified files. Creates one instance.
                 *
                 * @param txt_file_name     the text file
                 * @param protein_file_name the file with protein annotations
                 * @param event_file_name   the file with event annotations
                 * @return NLPInstance that represents the given text and annotations
                 * @throws IOException if IO goes wrong.
                """
                char_to_token = {}
                instance = NLPInstance()
                with open(txt_file_name, encoding='UTF-8') as reader:
                    current_token = instance.add_token()
                    current_token_content = ""
                    for current_index, character in enumerate(iter(functools.partial(reader.read, 1), '')):
                        char_to_token[current_index] = current_token
                        if character == ' ' or character == '\n':
                            if len(current_token_content) > 0:
                                current_token.add_property("Word", current_token_content)
                                current_token.add_property("Index", str(len(instance.tokens) - 1))
                                current_token_content = ""
                                current_token = instance.add_token()

                        else:
                            current_token_content += character

                id2token = {}
                with open(protein_file_name, encoding='UTF-8') as reader:
                    for line in reader.readlines():
                        split = line.strip().split()
                        if split[0].startswith("T"):
                            elem_id = split[0]
                            elem_type = split[1]
                            elem_from = int(split[2])
                            elem_to = int(split[3])
                            from_token = char_to_token[elem_from]
                            to_token = char_to_token[elem_to]
                            instance.add_edge(from_token.index, to_token.index, elem_type, "protein",
                                              EdgeRenderType.span)
                            id2token[elem_id] = to_token

                with open(event_file_name, encoding='UTF-8') as reader:
                    # get event mentions and locations etc.
                    for line in reader.readlines():
                        split = line.strip().split()
                        elem_id = split[0]
                        if elem_id.startswith("T"):
                            elem_type = split[1]
                            elem_from = int(split[2])
                            elem_to = int(split[3])
                            from_token = char_to_token[elem_from]
                            to_token = char_to_token[elem_to]
                            if elem_type == "Entity":
                                term_class = "entity"
                            else:
                                term_class = "event"
                            instance.add_edge(from_token.index, to_token.index, elem_type, term_class,
                                              EdgeRenderType.span)
                            id2token[elem_id] = to_token
                        elif elem_id.startswith("E"):
                            type_and_mention_id = split[1].split(":")
                            even_token = id2token[type_and_mention_id[1]]
                            id2token[elem_id] = even_token

                with open(event_file_name, encoding='UTF-8') as reader:
                    # now create the event roles
                    for line in reader.readlines():
                        split = line.split()
                        elem_id = split[0]
                        if elem_id.startswith("E"):
                            even_token = id2token[elem_id]
                            for elem in split[2:]:
                                role_and_id = elem.split(":")
                                arg_token = id2token.get(role_and_id[1])
                                if arg_token is None:
                                    raise RuntimeError(
                                        "There seems to be no mention associated with id {0} for event {1} in"
                                        " file {2}".format(role_and_id[1], elem_id, event_file_name))
                                instance.add_edge(even_token.index, arg_token.index, role_and_id[0], "role",
                                                  EdgeRenderType.dependency, note=elem_id)
                result.append(instance)
        return result

    def loadProperties(self, properties, prefix):
        pass

    def saveProperties(self, properties, prefix):
        pass

    def setMonitor(self, monitor):
        pass

    def accessory(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------


class TheBeastFormat(CorpusFormat):
    """
    Loads markov thebeast data
    This format is invented by Sebastian Reidel, the original author of What's Wrong with My NLP?
    The project homepage: https://code.google.com/archive/p/thebeast/
    There is an example input for the format in:
     https://atrium.lib.uoguelph.ca/xmlui/bitstream/handle/10214/8641/Fairholm_William_201412_Msc.pdf
    As less mentions or examples found, this code is not thoroughly tested.
    """
    def __init__(self):
        self._name = "thebeast"
        self.tokens = ""  # GUI STUFF
        self.deps = ""
        self.spans = ""

    @staticmethod
    def unquote(string):
        return string[1: len(string) - 1]

    @property
    def longName(self):
        return self._name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @staticmethod
    def extract_predicates_from_string(text):
        preds = {}
        for s in text.split(','):
            s = s.strip()
            if len(s) > 0:
                ind = s.find(':')
                if ind == -1:
                    pred, as_rest = s, s
                else:
                    pred, as_rest = s.split(':', maxsplit=1)
                preds[pred] = as_rest

        return preds

    def add_edges(self, instance, rows, token_preds, dep_preds, span_preds):
        for pred in token_preds.values():
            # add_tokens
            for row in rows:
                try:
                    instance.add_token(int(row[0])).add_property(pred, self.unquote(row[1]))
                except ValueError:
                    print("Could not load tokens from row {0} of rows {1}, skipping this row.".format(row, rows),
                          file=sys.stderr)
                    # raise RuntimeError("Could not load tokens from row {0} of rows {1}, skipping this row.".
                    #                    format(row, rows))
        # instance.consistify()
        for pred in dep_preds.values():
            # add_deps
            for row in rows:
                if len(row) == 4:
                    desc = self.unquote(row[3].replace("-BR-", "\n\t"))
                else:
                    desc = None
                instance.add_dependency(int(row[0]), int(row[1]), self.unquote(row[2]), pred, desc)
        for pred in span_preds.values():
            # add_spans
            for row in rows:
                # default len(row) == 3
                token = int(row[1])
                desc = None

                if len(row) == 2:
                    token = int(row[0])
                elif len(row) == 4:
                    desc = self.unquote(row[3].replace("-BR-", "\n\t"))

                instance.add_span(int(row[0]), token, self.unquote(row[2]), pred, desc)

    def load(self, file_name, from_sent_nr, to_sent_nr):
        with open(file_name, encoding='UTF-8') as reader:
            token_preds = self.extract_predicates_from_string(self.tokens)
            dep_preds = self.extract_predicates_from_string(self.deps)
            span_preds = self.extract_predicates_from_string(self.spans)

            instance_nr = 0
            instance = NLPInstance()
            as_token = None
            as_dep = None
            as_span = None
            result = []  # [NLPInstance]
            rows = {}  # {str: [[str]]}

            self.init_rows(rows, token_preds, span_preds, dep_preds)

            while instance_nr < to_sent_nr:
                try:
                    line = check_eof(reader.readline()).strip()
                    if line.startswith(">>"):
                        # monitor.progressed(instanceNr)
                        instance_nr += 1
                        if instance_nr > from_sent_nr and instance_nr > 1:
                            self.add_edges(instance, rows, token_preds, dep_preds, span_preds)

                            result.append(instance)
                            instance = NLPInstance()
                            rows.clear()
                            self.init_rows(rows, token_preds, span_preds, dep_preds)

                    elif line.startswith(">") and instance_nr > from_sent_nr:
                        pred = line[1:]
                        as_token = token_preds.get(pred)
                        as_dep = dep_preds.get(pred)
                        as_span = span_preds.get(pred)
                    else:
                        line = line.strip()
                        if line != "" and instance_nr > from_sent_nr:
                            row = line.split("\t")
                            if as_token is not None:
                                rows[as_token].add(row)
                            if as_dep is not None:
                                rows[as_dep].add(row)
                            if as_span is not None:
                                rows[as_span].add(row)

                except EOFError:
                    break

            self.add_edges(instance, rows, token_preds, dep_preds, span_preds)

            result.append(instance)
            return result

    @staticmethod
    def init_rows(rows, token_preds, span_preds, dep_preds):
        for pred in token_preds.values():
            rows[pred] = []
        for pred in span_preds.values():
            rows[pred] = []
        for pred in dep_preds.values():
            rows[pred] = []

    def loadProperties(self, properties, prefix):
        pass

    def saveProperties(self, properties, prefix):
        pass

    def setMonitor(self, monitor):
        pass

    def accessory(self):
        pass
