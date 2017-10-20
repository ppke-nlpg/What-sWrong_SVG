#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libwwnlp.model.nlp_instance import NLPInstance, RenderType
from ioFormats.CorpusFormat import CorpusFormat


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

    def load(self, file_name, from_sentence_nr: int, to_sentence_nr: int):
        with open(file_name, encoding='UTF-8') as reader:

            """
             * Skip past the next aligned segment pair in the given reader.
             *
             * @throws EndOfInputException if there was no aligned segment pair to skip because we're
             *         already at the end of the given reader
            """
            # There are three lines per segment pair.
            for _ in range(3*from_sentence_nr):
                try:
                    reader.readline()
                except EOFError:  # TODO: Readline will not throw exception instead returns empty string...
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
                    reader.readline()

                    tokens = []
                    """
                     * a list of one-based {source-token-index, target-token-index} pairs
                    """
                    alignment_edges = []  # List<Pair<Integer, Integer>>

                    # String line;

                    # The second line contains the source segment, tokenized, with no adornment.
                    tokens.append(reader.readline().split())
                    tokens.append([])

                    """
                     The third line contains the tokens of the target segment, starting with the pseudo-token
                     "NULL", with each token followed by a whitespace-delimited list (in curly braces nested
                     in parentheses) of the 1-based indices of the source tokens aligned to it, e.g.:

                     NULL ({ 2 }) customization ({ 1 }) of ({ }) tasks ({ 3 4 })
                    """
                    line = reader.readline()

                    # start from index 1 to skip the NULL token
                    for token_with_aligned_indices in line.split(" }) ")[1:]:
                        # tokenWithAlignedIndices looks something like "tasks ({ 3 4" or "of ({"
                        # don't discard empty trailing strings  # TODO: Why? If from the second element it's not needed?
                        splitted1, splitted2, _ = token_with_aligned_indices.split(" ({")
                        tokens[1].append(splitted1)
                        aligned_index_list_as_string = splitted2.strip()

                        """
                         we need to handle the empty list specially, because the split method on the empty
                         string returns a singleton array containing the empty string, but here an empty
                         array is what we want
                        """
                        for aligned_index_as_string in aligned_index_list_as_string.split(" "):
                            alignment_edges.append((int(aligned_index_as_string), i))

                    # now we're ready to make the NLPInstance
                    instance = NLPInstance(render_type=RenderType.alignment)
                    if self._reverseCheckBox:
                        for token in tokens[1]:
                            instance.add_token().add_property("word", token)
                        # instance.add_split_point(len(instance.tokens))  # TODO: Instance add_splitpoints
                        for token in tokens[0]:
                            instance.add_token().add_property("word", token)
                        for alignmentEdge1, alignmentEdge2 in alignment_edges:
                            from_edge = alignmentEdge2 - 1
                            to_edge = tokens[1].length + alignmentEdge1 - 1
                            instance.add_edge(from_edge, to_edge, "align", "align")
                    else:
                        for token in tokens[0]:
                            instance.add_token().add_property("word", token)
                        # instance.add_split_point(len(instance.tokens))
                        for token in tokens[1]:
                            instance.add_token().add_property("word", token)
                        for alignmentEdge1, alignmentEdge2 in alignment_edges:
                            from_edge = alignmentEdge1 - 1
                            to_edge = tokens[0].length + alignmentEdge2 - 1
                            instance.add_edge(from_edge, to_edge, "align", "align")

                except EOFError:  # TODO: Readline will not throw exception instead returns empty string...
                    break
                result.append(instance)

        return result
