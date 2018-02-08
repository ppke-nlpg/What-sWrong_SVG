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
    from os.path import basename

    from libwwnlp.model.nlp_instance import RenderType
    from libwwnlp.NLPCanvas import NLPCanvas
    from libwwnlp.CorpusNavigator import CorpusNavigator

    def test_process(corp_format, fname, render_type=RenderType.single, min_sent=0, max_sent=2):
        print('Testing {0}'.format(corp_format), file=sys.stderr)
        nav = CorpusNavigator(NLPCanvas())
        nav.add_corpus(fname, corp_format, 'gold', min_sent, max_sent)
        nav.select_gold(basename(fname))
        nav.canvas.renderer = nav.canvas.renderers[render_type]

        for n, inst in enumerate(nav.iter_gold()):
            nav.canvas.set_nlp_instance(inst)
            nav.canvas.render_nlpgraphics('{0}_output{1}.svg'.format(corp_format, n))

    if conll2000:
        test_process('CoNLL2000', 'test_data/conll00.gold')

    if conll2002:
        test_process('CoNLL2002', 'test_data/conll02.gold')

    if conll2003:
        test_process('CoNLL2003', 'test_data/conll03.gold')

    if conll2004:
        test_process('CoNLL2004', 'test_data/conll04.gold')

    if conll2005:
        test_process('CoNLL2005', 'test_data/conll05.gold')

    if conll2006:
        test_process('CoNLL2006', 'test_data/conll06.gold')

    if conll2008:
        test_process('CoNLL2008', 'test_data/conll08.open')
    # TODO
    """
    if conll2009:
        test_process('CoNLL2008', 'test_data/conll09.gold')
    "" "
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
    """
    if giza:
        test_process('Giza Alingment Format', 'test_data/giza.gold', RenderType.alignment)

    if gale:
        test_process('Gale Alingment Format', 'test_data/gale.gold', RenderType.alignment, max_sent=1)

    if thebeast:
        test_process('The Beast Format', 'test_data/gale.gold', max_sent=1)
    # TODO
    """
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
    """

    if lisp_sexpr:
        test_process('Lisp S-expr Format', 'test_data/lispsexpr.gold', max_sent=1)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'TEST':
        test()
        exit(0)
    else:
        from Qt5GUI.GUIMain import main
        main(sys.argv)
