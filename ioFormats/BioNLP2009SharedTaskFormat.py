#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os.path
import functools

from libwwnlp.model.nlp_instance import NLPInstance
from ioFormats.CorpusFormat import CorpusFormat
from libwwnlp.model.edge import EdgeRenderType


def check_eof(line):
    if len(line) == 0:
        raise EOFError
    return line


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
