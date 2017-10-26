#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from Qt5GUI.GUIMain import main

malt = False
giza = False
gale = False
thebeast = False
bionlp09 = False
lisp_sexpr = True


def test():
    from ioFormats.TabProcessor import CoNLL2000, CoNLL2002, CoNLL2003, CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, \
        CoNLL2009, MaltTab
    from ioFormats.GizaAlignmentFormat import GizaAlignmentFormat
    from ioFormats.GaleAlignmentFormat import GaleAlignmentFormat
    from ioFormats.TheBeastFormat import TheBeastFormat
    from ioFormats.BioNLP2009SharedTaskFormat import BioNLP2009SharedTaskFormat
    from ioFormats.LispSExprFormat import LispSExprFormat
    from libwwnlp.model.nlp_instance import RenderType
    from libwwnlp.render.svg_writer import render_nlpgraphics
    from libwwnlp.NLPCanvas import NLPCanvas
    from libwwnlp.model.filter import Filter

    if malt:
        corpus = []
        factory = MaltTab()
        f = open('test_data/malt.gold')
        lines = list(f.readlines())
        rows = []
        canvas = NLPCanvas()
        canvas.filter = Filter()
        instance_nr = 0
        for line in lines:
            if instance_nr == 200:
                break
            line = line.strip()
            if line == "":
                instance_nr += 1
                instance = factory.create(rows)
                instance.render_type = RenderType.single
                corpus.append(instance)
                del rows[:]
            else:
                rows.append(line)

        if len(rows) > 0:
            instance_nr += 1
            instance = factory.create(rows)
            instance.render_type = RenderType.single
            corpus.append(instance)

        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            render_nlpgraphics(canvas.renderer, canvas.filter_instance(), 'output{0}.svg'.format(i))

    if giza:
        factory = GizaAlignmentFormat()
        fn = 'test_data/giza.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.alignment]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            render_nlpgraphics(canvas.renderer, canvas.filter_instance(), 'output{0}.svg'.format(i))

    if gale:
        factory = GaleAlignmentFormat()
        fn = 'test_data/gale.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.alignment]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 1)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            render_nlpgraphics(canvas.renderer, canvas.filter_instance(), 'output{0}.svg'.format(i))

    if thebeast:
        factory = TheBeastFormat()
        fn = 'test_data/thebeast.gold'
        canvas = NLPCanvas()
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 1)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            render_nlpgraphics(canvas.renderer, canvas.filter_instance(), 'output{0}.svg'.format(i))

    if bionlp09:
        factory = BioNLP2009SharedTaskFormat()
        fn = 'test_data/bionlp09'
        canvas = NLPCanvas()
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 1)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            render_nlpgraphics(canvas.renderer, canvas.filter_instance(), 'output{0}.svg'.format(i))

    if lisp_sexpr:
        factory = LispSExprFormat()
        fn = 'test_data/lispsexpr.gold'
        canvas = NLPCanvas()
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 1)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            render_nlpgraphics(canvas.renderer, canvas.filter_instance(), 'output{0}.svg'.format(i))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "TEST":
        test()
        exit(0)
    main(sys.argv)
