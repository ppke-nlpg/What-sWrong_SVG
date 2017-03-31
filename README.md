# _What's Wrong With My NLP?_ reimplemented in Python 3 (whats-wrong-python)

_What's Wrong With My NLP?_: A visualizer for Natural Language Processing problems.

Original project page and source: https://code.google.com/archive/p/whatswrong/

_What's Wrong With My NLP?_ is rewritten in Python 3 using SVG instead of JAVA canvas.

# Features
- The program can open and diff the following formats:
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
- The program is able to export to SVG PDF and (E)PS formats (only SVG is wired out to the GUI yet)
- Many customising features can be set to the viewed sentence (show/hide features, edges by type, etc.)
- Currently, only one sentence is supported corpus handling is under heavy development.
- More to come...

For planned features see the Development section of this document.

## Demo

There is a demo sentence pair to test for MALT-tab format in the [test_data](https://github.com/ppke-nlpg/whats-wrong-python/tree/master/test_data) directory.

# Installation

At the time of writing the program is under heavy development.
To install the program install all the depencies separately clone the repository and run `whatswrong.py`

## Dependencies

   - Python 3 (the higher version is the better, the program is only tested with the lastest LTS version of Ubuntu)
   - PyQt4 (for GUI)
   - [cairosvg](http://cairosvg.org/) (for (E)PS and PDF export)
 
# Development and contributing

Our plan is to achieve the functionality of the original JAVA program, but in a new, extendable, innovative form.

Our main interests in development:

- __Totally separate GUI__ form the rendering logic creating a library, that would function of a backend of any GUI or WebUI.
- Fix Corpus handling and find a more or less standard API for the formats (to possibly help other projects and maximise the usability)
- Add support for standard, editable and non editable vector image formats enabling to create publication- and web-ready images and animations.
- Implement a WebUI for the library as for modern programs it is a must have.
- Create extensive documentation and the possibility to add new formats as easily as possible. 

## Contributing

### Rules of contributing

Please consult [the general rules of contributing](https://github.com/ppke-nlpg/whats-wrong-python/blob/master/CONTRIBUTING:md) before you start with the following steps:

1. Open an issue and describe the task you want to implement!
2. If accepted fork and implement the task with extensive tests!
3. Make a pull request and reference the issue!
4. Modify the pull request as asked to be accepted!
5. Profit! :)

### We happily accept contributions on the following topics:

- Add test data (we need the format, not the proprietary data) to the following implemened formats (as some of the datasets are not online by now.) 
    - CCG
    - MaltTab (more extensive test data needed)
    - CoNLL 2000
    - CoNLL 2002
    - CoNLL 2003
    - CoNLL 2004
    - CoNLL 2005
    - CoNLL 2006
    - CoNLL 2008
    - CoNLL 2009
- Add the following formats that was implemented in _what's wrong JAVA_ (hopefully with extensive test data):
	- BioNLP2009 (see ioFormats/BioNLP2009SharedTaskFormat.java)
	- GaleAlignment (see ioFormats/GaleAlignmentFormat.java)
	- GizaAlignment (see ioFormats/GizaAlignmentFormat.java)
	- TheBeast (see ioFormats/TheBeastFormat.java)
	- LispSExpr (see ioFormats/LispSExprFormat.java)
- Add more missing formats:
	- CoNLL 1999
	- CoNLL 2001
	- CoNLL 2007
	- CoNLL 2010 and newer (see the [CoNLL shared task website](http://www.conll.org/previous-tasks))
	- Other formats that might be interesting.
- Your really own feature!
- Other specific task to come as the refactoring calms down.

# License

This code is made available under the GNU Lesser General Public License v3.0.
