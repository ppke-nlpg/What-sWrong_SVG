#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

conll2000 = True
conll2002 = True
conll2003 = True
conll2004 = True
conll2005 = False
conll2006 = True
conll2008 = False
conll2009 = True

malt = False
giza = True
gale = True
thebeast = True
bionlp09 = True
lisp_sexpr = True


def test():
    from ioFormats.TabProcessor import CoNLL2000, CoNLL2002, CoNLL2003, CoNLL2004, CoNLL2005, CoNLL2006, CoNLL2008, \
        CoNLL2009, MaltTab
    from ioFormats.OtherFormats import GizaAlignmentFormat, GaleAlignmentFormat, LispSExprFormat,\
        BioNLP2009SharedTaskFormat, TheBeastFormat
    from libwwnlp.model.nlp_instance import RenderType
    from libwwnlp.NLPCanvas import NLPCanvas
    from libwwnlp.model.filter import Filter

    if conll2000:
        print("Testing CoNLL2000", file=sys.stderr)
        factory = CoNLL2000()
        fn = 'test_data/conll00.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.single]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('conll00_output{0}.svg'.format(i))

    if conll2002:
        print("Testing CoNLL2002", file=sys.stderr)
        factory = CoNLL2002()
        fn = 'test_data/conll02.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.single]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('conll02_output{0}.svg'.format(i))

    if conll2003:
        print("Testing CoNLL2003", file=sys.stderr)
        factory = CoNLL2003()
        fn = 'test_data/conll03.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.single]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('conll03_output{0}.svg'.format(i))

    if conll2004:
        print("Testing CoNLL2004", file=sys.stderr)
        factory = CoNLL2004()
        fn = 'test_data/conll04.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.single]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('conll04_output{0}.svg'.format(i))

    if conll2005:
        print("Testing CoNLL2005", file=sys.stderr)
        factory = CoNLL2005()
        fn = 'test_data/conll05.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.single]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('conll05_output{0}.svg'.format(i))

    if conll2006:
        print("Testing CoNLL2006", file=sys.stderr)
        factory = CoNLL2006()
        fn = 'test_data/conll06.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.single]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('conll06_output{0}.svg'.format(i))

    if conll2008:
        print("Testing CoNLL2008", file=sys.stderr)
        factory = CoNLL2008()
        fn = 'test_data/conll08.open'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.single]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('conll08_output{0}.svg'.format(i))

    if conll2009:
        print("Testing CoNLL2009", file=sys.stderr)
        factory = CoNLL2009()
        fn = 'test_data/conll09.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.single]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('conll09_output{0}.svg'.format(i))

    if malt:
        print("Testing MaltTab", file=sys.stderr)
        corpus = []
        factory = MaltTab()
        f = open('test_data/malt.gold', encoding='UTF-8')
        lines = list(f.readlines())
        rows = []
        canvas = NLPCanvas()
        canvas.filter = Filter()
        instance_nr = 0
        for line in lines:
            if instance_nr == 200:
                break
            line = line.strip()
            if line == '':
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
            canvas.render_nlpgraphics('malt_output{0}.svg'.format(i))

    if giza:
        print("Testing Giza Alingment Format", file=sys.stderr)
        factory = GizaAlignmentFormat()
        fn = 'test_data/giza.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.alignment]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 2)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('giza_output{0}.svg'.format(i))

    if gale:
        print("Testing Gale Alingment Format", file=sys.stderr)
        factory = GaleAlignmentFormat()
        fn = 'test_data/gale.gold'
        canvas = NLPCanvas()
        canvas.renderer = canvas.renderers[RenderType.alignment]
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 1)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('gale_output{0}.svg'.format(i))

    if thebeast:
        print("Testing The Beast Format", file=sys.stderr)
        factory = TheBeastFormat()
        fn = 'test_data/thebeast.gold'
        canvas = NLPCanvas()
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 1)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('thebeast_output{0}.svg'.format(i))

    if bionlp09:
        print("Testing BioNLP2009 Shared Task Format", file=sys.stderr)
        factory = BioNLP2009SharedTaskFormat()
        fn = 'test_data/bionlp09'
        canvas = NLPCanvas()
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 1)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('bionlp09_output{0}.svg'.format(i))

    if lisp_sexpr:
        print("Testing Lisp S-expr Format", file=sys.stderr)
        factory = LispSExprFormat()
        fn = 'test_data/lispsexpr.gold'
        canvas = NLPCanvas()
        canvas.filter = Filter()
        corpus = factory.load(fn, 0, 1)
        for i, instance in enumerate(corpus):
            canvas.set_nlp_instance(instance)
            canvas.render_nlpgraphics('lisp_sexpr_output{0}.svg'.format(i))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'TEST':
        test()
        exit(0)
    else:
        from Qt5GUI.GUIMain import main
        main(sys.argv)
