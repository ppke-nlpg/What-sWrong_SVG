# _What's Wrong With My NLP?_ reimplemented in Python 3 (whats-wrong-python)

_What's Wrong With My NLP?_: A visualizer for Natural Language Processing problems.

Original project page and source: https://code.google.com/archive/p/whatswrong/

_What's Wrong With My NLP?_ is rewritten in Python 3 using SVG instead of JAVA canvas.

# Features
- The program can open and diff the following formats (and it is easy to implement others):
    - CCG
    - MaltTab (tested)
    - CoNLL 2000
    - CoNLL 2002
    - CoNLL 2003
    - CoNLL 2004
    - CoNLL 2005
    - CoNLL 2006
    - CoNLL 2008
    - CoNLL 2009
    - BioNLP2009
	- GaleAlignment
	- GizaAlignment
	- TheBeast
	- LispSExpr
- Supports for standard, editable and non editable vector image formats (SVG PDF and (E)PS) enabling to create publication- and web-ready images and animations
- __Totally separate Qt5-based GUI__: has a headless mode with basic CLI interface and can act as a library (eg. to create 3-way diffs, and automatic testing for `git bisect`)
- Many customising features can be set to the viewed sentence interactively (show/hide features, edges by type, etc.)
- The layout can be customised to the roots. Supports dependency, alignment and span layouts, but it is easy to mix and create new ones
- 
For planned features see the Development section of this document.

## Demo

There is a demo sentence pair to test for MALT-tab format in the [test_data](https://github.com/ppke-nlpg/whats-wrong-python/tree/master/test_data) directory.

# Installation

At the time of writing the program is in beta state, and some improvement is still due.
To install the program install all the depencies separately clone the repository and run `whatswrong.py`

## Dependencies

   - Python 3 (the higher version is the better, the program is only tested with the lastest LTS version of Ubuntu)
   - PyQt5 (for GUI)
   - [svgwrite](https://pypi.python.org/pypi/svgwrite/)
   - [cairosvg](http://cairosvg.org/) (for (E)PS and PDF export)
   - Cairo (for font width computation)
 
# Development and contributing

Our plan is to achieve the functionality of the original JAVA program, but in a new, extendable, standards compilant, innovative form

Our main interests in development:

- See the issue tracker and TODOs in the code for details

## Contributing

### Rules of contributing

Please consult [the general rules of contributing](https://github.com/ppke-nlpg/whats-wrong-python/blob/master/CONTRIBUTING:md) before you start with the following steps:

1. Open an issue and describe the task you want to implement!
2. If accepted fork and implement the task with extensive tests!
3. Make a pull request and reference the issue!
4. Modify the pull request as asked to be accepted!
5. Profit! :)

## Style guide

1. We prefer the [Google Style docstring format](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
2. Concerning the code style: what is good for PyCharm or similar linter by default (i.e. no warnings), it's good for us. (It is more relaxed, than the Google Style guide.)    
    - For example Pylint: `pylint3 --disable="missing-docstring,too-many-instance-attributes,too-many-arguments,too-many-nested-blocks,too-many-boolean-expressions,too-many-locals,too-few-public-methods,too-many-statements,too-many-ancestors,no-member" --notes="" --max-line-length=120`
    - For example Pycodestyle: `pycodestyle --max-line-length=120 --exclude="./Qt5GUI/GUI"`

# License

This code is made available under the GNU Lesser General Public License v3.0.

If you use this program please cite the following paper:

Indig, Balázs és Simonyi, András és Ligeti-Nagy, Noémi (2018) What's Wrong, Python? -- A Visual Differ and Graph Library for NLP in Python. In: Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018), 2018.05.07-2018.05.12, Miyazaki.

    @InProceedings{INDIG18.886,
      author = {Balázs Indig and András Simonyi and Noémi Ligeti-Nagy},
      title = "{What's Wrong, Python? -- A Visual Differ and Graph Library for NLP in Python}",
      booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
      year = {2018},
      month = {May 7-12, 2018},
      address = {Miyazaki, Japan},
      editor = {Nicoletta Calzolari (Conference chair) and Khalid Choukri and Christopher Cieri and Thierry Declerck and Sara Goggi and Koiti Hasida and Hitoshi Isahara and Bente Maegaard and Joseph Mariani and Hélène Mazo and Asuncion Moreno and Jan Odijk and Stelios Piperidis and Takenobu Tokunaga},
      publisher = {European Language Resources Association (ELRA)},
      isbn = {979-10-95546-00-9},
      language = {english}
      }
