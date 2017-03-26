#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# todo: further redesign when all part is implemented eg: merge addDependency and addSpan

from enum import Enum

from .token import Token
from .edge import EdgeRenderType, Edge

"""
 * An NLPInstance represents a sentence or any other kind of utterance and some of its (NLP) properties. Properties of
 * sentence are its tokens, that have their own properties, and edges between tokens. Such edges can represent syntactic
 * or semantic dependencies, such as SRL predicate-argument relations, as well as annotated spans (such as NP chunks or
 * NER entities).
 *
 * @author Sebastian Riedel
"""


class RenderType(Enum):
    """
     * Show as single sentence with dependencies and spans
    """
    single = 'single',
    """
     * Show two aligned sentences, on top of each other
    """
    alignment = 'alignment'


class NLPInstance:
    """
     * How to render this instance.
    """
    @property
    def render_type(self) -> RenderType:
        return self._render_type

    @render_type.setter
    def render_type(self, value: RenderType):
        self._render_type = value

    """
     * Contains the edges of this instance.
    """
    # See the getter below...

    """
     * Contains the tokens of this instance.
    """
    @property
    def tokens(self) -> tuple:
        return tuple(self._tokens)

    @tokens.setter
    def tokens(self, value: list):
        self._tokens = value

    """
     * Contains a mapping from sentence indices to tokens.
    """
    @property
    def map(self) -> dict:
        return self._map

    @map.setter
    def map(self, value: dict):
        self._map = value

    """
     * A list of token indices at which the NLP instance is to be split. These indices can refer to sentence boundaries
     * in a document, but they can also indicate that what follows after a split point is an utterance in a different
     * language (for alignment).
    """
    @property
    def splitPoints(self) -> tuple:
        return tuple(self._splitPoints)

    @splitPoints.setter
    def splitPoints(self, value: list):
        self._splitPoints = value

    """
     * Creates an empty NLPInstance without edges or tokens.

    OR

     * Creates a new NLPInstance with the given tokens and edges. The passed collections will be copied and not
     * changed.
     *
     * @param tokens      the tokens of the sentence.
     * @param edges       the edges of the sentence.
     * @param render_type  the render type for the instance.
     * @param splitPoints the points at which the instance can be split.

    """
    def __init__(self, tokens: tuple or list=None, edges: set or frozenset=None, render_type: RenderType=None,
                 splitPoints: tuple or list=None):
        self._tokens = []  # ArrayList<Token>()
        self._map = {}  # HashMap<Integer, Token>()
        if tokens is not None:
            self._tokens.extend(tokens)
            for t in tokens:
                self._map[t.index] = t
        self._edges = []  # ArrayList<Edge>()
        if edges is not None:
            self._edges.extend(edges)
        if render_type is not None:
            self._render_type = render_type
        else:
            self._render_type = None
        self._splitPoints = []  # ArrayList<Integer>()
        if splitPoints is not None:
            self._splitPoints.extend(splitPoints)

    """
     * Returns the render type that controls which renderer to use.
     *
     * @return the render type for this instance.
    """
    # See the getter above...

    """
     * Sets the render type for this instance.
     *
     * @param render_type the render type for this instance.
    """
    # See the setter above...

    """
     * Creates and adds an edge from the token at the given 'from' index to the token at the given 'to' index with the
     * given label and type. The edge will have the default render type.
     *
     * @param from  index of the token the edge should start at. The token at the given index must already exist in the
     *              sentence.
     * @param to    index of the token edge should end at. The token at the given index must already exist in the
     *              sentence.
     * @param label the label of the edge.
     * @param type  the type of edge.
     * @see com.googlecode.whatswrong.Edge

     OR

     * Creates and adds a new edge with the given properties.
     *
     * @param from       index of the token the edge should start at. The token at the given index must already exist in
     *                   the sentence.
     * @param to         index of the token edge should end at. The token at the given index must already exist in the
     *                   sentence.
     * @param label      the label of the edge.
     * @param type       the type of edge.
     * @param render_type the render type of the edge.
     * @see com.googlecode.whatswrong.Edge

     OR

     * Adds an edge.
     *
     * @param edge the edge to add.

     OR

     * Creates and adds an edge with the given properties. It will have the default render type.
     *
     * @param from  The start token. The created edge will start at the token of this sentence with the same index as
     *              the provided token. This means the start token of created edge does not need to be equal to the
     *              provided token -- they just have to have the same index.
     * @param to    the end token. The created edge will end at the token of this sentence with the same index as the
     *              provided token. This means that the end token of created edge does not need to be equal to the
     *              provided token -- they just have to have the same index.
     * @param label the label of the edge.
     * @param type  the type of edge.
     * @see com.googlecode.whatswrong.Edge

     OR

     * Creates and adds an edge with the given properties. It will have the default render type.
     *
     * @param from       The start token. The created edge will start at the token of this sentence with the same index
     *                   as the provided token. This means the start token of created edge does not need to be equal to
     *                   the provided token -- they just have to have the same index.
     * @param to         the end token. The created edge will end at the token of this sentence with the same index as
     *                   the provided token. This means that the end token of created edge does not need to be equal to
     *                   the provided token -- they just have to have the same index.
     * @param label      the label of the edge.
     * @param type       the type of edge.
     * @param render_type the render type of the edge.
     * @see com.googlecode.whatswrong.Edge
    """
    def addEdge(self, start: int=None, to: int=None, label: str=None, edge_type: str=None,
                render_type: EdgeRenderType=None, desc=None, note: str=None):
        if self.isValidEdge(start, to):
            self._edges.append(Edge(start=self._map[start], end=self._map[to], label=label, edge_type=edge_type,
                                    render_type=render_type, description=desc, note=note))

    def isValidEdge(self, start, to):
        if start not in self._map:
            print('There is no token at index: {0} for tokens {1}'.format(start, self._map))
            fromToken = False
        else:
            fromToken = True
        if to not in self._map:
            print('There is no token at index: {0} for tokens {1}'.format(to, self._map))
            toToken = False
        else:
            toToken = True
        return toToken and fromToken

    """
     * Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.EdgeRenderType#span}
     *
     * @param from  index of the token the edge should start at. The token at the given index must already exist in the
     *              sentence.
     * @param to    index of the token edge should end at. The token at the given index must already exist in the
     *              sentence.
     * @param label the label of the edge.
     * @param type  the type of edge.
     * @see com.googlecode.whatswrong.Edge

     OR

     * Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.EdgeRenderType#span}
     *
     * @param from        index of the token the edge should start at. The token at the given index must already exist
     *                    in the sentence.
     * @param to          index of the token edge should end at. The token at the given index must already exist in the
     *                    sentence.
     * @param label       the label of the edge.
     * @param type        the type of edge.
     * @param description the description of the span.
     * @see com.googlecode.whatswrong.Edge
    """
    def addSpan(self, start: int, to: int, label: str, span_type: str, desc: str=None):
        if self.isValidEdge(start, to):
            self._edges.append(Edge(self._map[start], self._map[to], label, span_type, render_type=EdgeRenderType.span,
                                    description=desc))

    """
     * Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.EdgeRenderType#dependency}
     *
     * @param from  index of the token the edge should start at. The token at the given index must already exist in the
     *              sentence.
     * @param to    index of the token edge should end at. The token at the given index must already exist in the
     *              sentence.
     * @param label the label of the edge.
     * @param type  the type of edge.
     * @see com.googlecode.whatswrong.Edge

     OR

     * Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.EdgeRenderType#dependency}
     *
     * @param from        index of the token the edge should start at. The token at the given index must already exist
     *                    in the sentence.
     * @param to          index of the token edge should end at. The token at the given index must already exist in the
     *                    sentence.
     * @param label       the label of the edge.
     * @param type        the type of edge.
     * @param description description of the edge
     * @see com.googlecode.whatswrong.Edge
    """
    def addDependency(self, start: int, to: int, label, dep_type: str, des: str=None, is_final: bool=True):
        if self.isValidEdge(start, to):
            self._edges.append(Edge(self._map[start], self._map[to], label, dep_type,
                                    render_type=EdgeRenderType.dependency, description=des, is_final=is_final))

    """
     * Adds the given collection of tokens to this instance.
     *
     * @param tokens the tokens to add.
    """
    def addTokens(self, tokens: tuple):
        self._tokens.extend(tokens)
        for t in tokens:
            self._map[t.index] = t

    """
     * Adds the given edges to this instance.
     *
     * @param edges the edges to add.
    """
    def addEdges(self, edges: list):
        self._edges.extend(edges)

    """
     * Merges the given instance with this instance. A merge will add for every token i all properties of the token i of
     * the passed instance <code>nlp</code>. It will also add every edge between i and i in the given instance
     * <code>nlp</code> as an edge between the tokens i and j of this instance, using the same type, label and
     * rendertype as the original edge.
     *
     * @param nlp the instance to merge into this instance.
    """
    def merge(self, nlp):
        for i in range(0, min(len(self._tokens), len(nlp.tokens))):
            self._tokens[i].merge(nlp.tokens(i))
        for edge in nlp.edges():
            self.addEdge(start=edge.start.index, to=edge.to.index, label=edge.label, edge_type=edge.edge_type,
                         render_type=edge.render_type, note=edge.note)

    """
     * Adds token that has the provided properties with default property names.
     *
     * @param properties an vararray of strings.
    """
    def addTokenWithProperties(self, *properties):
        token = Token(len(self._tokens))
        for prop in properties:
            token.add_property(prop)
        self._tokens.append(token)
        self._map[token.index] = token

    """
     * Adds a new token and returns it.
     *
     * @return the token that was added.

    OR

     * Adds a token at a certain index. This method can be used when we don't want to build the sentence in order. Note
     * that if you build the instance using this method you have to call {@link NLPInstance#consistify()} when you are
     * done.
     *
     * @param index the index of the token to add.
     * @return the token that was added.
    """
    def addToken(self, index: int=None, is_actual: bool=False) -> Token:
        if index is None:
            vertex = Token(len(self._tokens), is_actual)
            self._tokens.append(vertex)
            self._map[vertex.index] = vertex
        else:
            vertex = self._map[index]
            if vertex is None:
                vertex = Token(index)
                self._map[vertex.index] = vertex

        return vertex

    """
     * If tokens were added with {@link com.googlecode.whatswrong.NLPInstance#addToken(int)} this method ensures that
     * all internal representations of the token sequence are consistent.
    """
    def consistify(self):
        self._tokens.extend(self._map.values())
        self._tokens.sort()

    """
     * Add a split point token index.
     *
     * @param tokenIndex a token index at which the instance should be split.
    """
    def addSplitPoint(self, tokenIndex: int):
        self._splitPoints.append(tokenIndex)

    """
     * Returns the list of split points for this instance. A split point is a point at which renderers can split the
     * token list.
     *
     * @return the list of split points.
    """
    # See the getter above...

    """
     * Returns all edges of this instance.
     *
     * @return all edges of this instance as unmodifiable list.

     OR

     * Returns all edges of this instance with the given render type.
     *
     * @param render_type the render type of the edges to return.
     * @return all edges of this instance with the given render type. This list can be altered if needed.
    """
    def getEdges(self, render_type: RenderType=None) -> frozenset:  # ArrayList<Edge>(edges.size())
        return frozenset({e for e in self._edges if e.render_type == render_type or render_type is None})

    """
     * Returns the token at the given index.
     *
     * @param index the index of the token to return
     * @return the token at the given index.
    """
    def getToken(self, index: int) -> Token:
        return self._map[index]

    """
     * Returns a list of all tokens in this instance.
     *
     * @return an unmodifiable list of all tokens of this sentence, in the right order.
     """
    # See the getter above...

    """
     * Returns a string representation of this instance. Mostly for debugging purposes.
     *
     * @return a string representation of this instance.
    """
    def __str__(self):
        return "{0}\n{1}\n{2}".format(", ".join(str(token) for token in self._tokens),
                                      ", ".join(str(v) for v in self._map.values()),
                                      ", ".join(str(e) for e in self._edges))
