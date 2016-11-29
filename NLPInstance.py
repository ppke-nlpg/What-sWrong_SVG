#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from Token import *
from Edge import *

from enum import Enum

"""
 * An NLPInstance represents a sentence or any other kind of utterance and some of its (NLP) properties. Properties of
 * sentence are its tokens, that have their own properties, and edges between tokens. Such edges can represent syntactic
 * or semantic dependencies, such as SRL predicate-argument relations, as well as annotated spans (such as NP chunks or
 * NER entities).
 *
 * @author Sebastian Riedel
"""


class NLPInstance:
    # todo: this class needs a redesign, in particular with respect to token identities.

    class RenderType(Enum):
        """
         * Show as single sentence with dependencies and spans
        """
        single = 'single',
        """
         * Show two aligned sentences, on top of each other
        """
        alignment = 'alignment'

    """
     * How to render this instance.
    """
    @property
    def renderType(self):
        return self._renderType

    @renderType.setter
    def renderType(self, value):
        self._renderType = value

    """
     * Contains the edges of this instance.
    """
    # See the getter below...

    """
     * Contains the tokens of this instance.
    """
    @property
    def tokens(self):
        return tuple(self._tokens)
        # return self._tokens

    @tokens.setter
    def tokens(self, value):
        self._tokens = value

    """
     * Contains a mapping from sentence indices to tokens.
    """
    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, value):
        self._map = value

    """
     * A list of token indices at which the NLP instance is to be split. These indices can refer to sentence boundaries
     * in a document, but they can also indicate that what follows after a split point is an utterance in a different
     * language (for alignment).
    """
    @property
    def splitPoints(self):
        return tuple(self._splitPoints)

    @splitPoints.setter
    def splitPoints(self, value):
        self._splitPoints = value

    """
     * Creates an empty NLPInstance without edges or tokens.
    
    OR
    
     * Creates a new NLPInstance with the given tokens and edges. The passed collections will be copied and not
     * changed.
     *
     * @param tokens      the tokens of the sentence.
     * @param edges       the edges of the sentence.
     * @param renderType  the render type for the instance.
     * @param splitPoints the points at which the instance can be split.
    
    """
    def __init__(self, tokens=None, edges=None, renderType=None, splitPoints=None):
        self._tokens = []
        self._map = {}
        if tokens is not None:
            self._tokens.extend(tokens)
            for t in tokens:
                self._map[t.index] = t
        self._edges = []
        if edges is not None:
            self._edges.extend(edges)
        if renderType is not None:
            self._renderType = renderType
        else:
            self._renderType = None
        self._splitPoints = []
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
     * @param renderType the render type for this instance.
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
     * @param renderType the render type of the edge.
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
     * @param renderType the render type of the edge.
     * @see com.googlecode.whatswrong.Edge
    """
    def addEdge(self, edge=None, From=None, to=None, label=None, type=None, renderType=None, fromToken=None,
                toToken=None):
        if edge is not None:
            self._edges.append(edge)
        else:
            if fromToken is not None and toToken is not None:
                From = fromToken.index
                to = toToken.index

            if From is not None and to is not None:
                #if self.isInvalidEdge(From, to):
                #    return
                From = self._map[From]
                to = self._map[to]
                label = label
                type = type
                renderType = renderType
            else:
                From = self._map[From]
                to = self._map[to]

        self._edges.append(Edge(From=From, To=to, label=label, Type=type, renderType=renderType))
    """
    def isInvalidEdge(self, From, to):
        if TokenProperty(From) not in  self._map:
            print('There is no token at index: {0} for tokens {1}'.format(From, self._map))
            fromToken = False
        else:
            fromToken = True
        if TokenProperty(to) not in self._map:
            print('There is no token at index: {0} for tokens {1}'.format(to, self._map))
            toToken = False
        else:
            toToken = True
        return not toToken or not fromToken
    """
    """
     * Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.RenderType#span}
     *
     * @param from  index of the token the edge should start at. The token at the given index must already exist in the
     *              sentence.
     * @param to    index of the token edge should end at. The token at the given index must already exist in the
     *              sentence.
     * @param label the label of the edge.
     * @param type  the type of edge.
     * @see com.googlecode.whatswrong.Edge
     
     OR
     
     * Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.RenderType#span}
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
    def addSpan(self, From, to, label, type, desc=None):
        #if self.isInvalidEdge(From, to):
        #    return
        edge = Edge(self._map[str(From)], self._map[str(to)], label, type, renderType=Edge.RenderType.span, description=desc)
        self._edges.append(edge)

    """
     * Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.RenderType#dependency}
     *
     * @param from  index of the token the edge should start at. The token at the given index must already exist in the
     *              sentence.
     * @param to    index of the token edge should end at. The token at the given index must already exist in the
     *              sentence.
     * @param label the label of the edge.
     * @param type  the type of edge.
     * @see com.googlecode.whatswrong.Edge

     OR

     * Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.RenderType#dependency}
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
    def addDependency(self, From, to, label, type, des=None):
        #if self.isInvalidEdge(From, to):
            #return
        edge = Edge(self._map[From], self._map[to], label, type, renderType=Edge.RenderType.dependency, description=des)
        self._edges.append(edge)

    """
     * Adds the given collection of tokens to this instance.
     *
     * @param tokens the tokens to add.
    """
    def addTokens(self, tokens):
        self._tokens.extend(tokens)
        for t in tokens:
            self._map[t.index] = t

    """
     * Adds the given edges to this instance.
     *
     * @param edges the edges to add.
    """
    def addEdges(self, edges):
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
            self.addEdge(edge.From().index(), edge.to().index(), edge.label(), edge.type(), edge.renderType())

    """
     * Adds token that has the provided properties with default property names.
     *
     * @param properties an vararray of strings.
    """
    def addTokenWithProperties(self, *properties):
        token = Token(len(self._tokens))
        for prop in properties:
            token.addProperty(prop)
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
    def addToken(self, index=None):
        if index is None:
            vertex = Token(str(len(self._tokens)))
            self._tokens.append(vertex)
            self._map[vertex.index] = vertex
        else:
            vertex = self._map[index]
            if vertex is None:
                vertex = Token(str(index))
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
    def addSplitPoint(self, tokenIndex):
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
     * @param renderType the render type of the edges to return.
     * @return all edges of this instance with the given render type. This list can be altered if needed.
    """
    def getEdges(self, renderType=None):
        if renderType is not None:
            result = []
            for e in self._edges:
                if e.renderType == renderType:
                    result.append(e)
        else:
            result = tuple(self._edges)
        return result

    """
     * Returns the token at the given index.
     *
     * @param index the index of the token to return
     * @return the token at the given index.
    """
    def getToken(self, index):
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
