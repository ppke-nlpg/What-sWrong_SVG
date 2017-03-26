#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# todo: further redesign when all part is implemented eg: merge addDependency and addSpan

from enum import Enum

from .token import Token
from .edge import EdgeRenderType, Edge


class RenderType(Enum):
    """An enum to specify how an instance should be rendered.

    Either a single sentence is shown or two aligned sentences,
    on top of each other.
    """
    single = 'single',
    alignment = 'alignment'


class NLPInstance:
    """An NLPInstance represents a sentence or utterance and some of its (NLP) properties.

    Properties of sentence are its tokens, that have their own properties, and
    edges between tokens. Such edges can represent syntactic or semantic
    dependencies, such as SRL predicate-argument relations, as well as annotated
    spans (such as NP chunks or NER entities).
    
    Attributes:
        tokens (list): The tokens of this instance.
        edges (list): The edges of this instance.
        render_type (RenderType): How to render this instance.
        token_map (dict[int, Token]): A mapping from sentence indices to tokens.
        split_points (list): A list of token indices at which the NLP instance is to
            be split. These indices can refer to sentence boundaries in a
            document, but they can also indicate that what follows after a split
            point is an utterance in a different language (for alignment).
    """

    
    def __init__(self, tokens: tuple or list=None, edges: set or frozenset=None,
                 render_type: RenderType=RenderType.single, split_points: tuple or list=None):
        """Create an NLPInstance with the given tokens and edges.
        
        The passed collections will be copied and not changed.
        
        Args:
            tokens (tuple or list): 
            edges (set or frozenset):
            render_type (RenderType):
            split_points (tuple or list): 
        """
        self.tokens = [] 
        self.token_map = {}
        self.edges = [] 
        self.render_type = render_type
        self.split_points = []
        if tokens is not None:
            self.tokens.extend(tokens)
            for t in tokens:
                self.token_map[t.index] = t
        if edges is not None:
            self.edges.extend(edges)
        if split_points is not None:
            self.split_points.extend(split_points)


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
            self.edges.append(Edge(start=self.token_map[start], end=self.token_map[to], label=label, edge_type=edge_type,
                                    render_type=render_type, description=desc, note=note))

    def isValidEdge(self, start, to):
        if start not in self.token_map:
            print('There is no token at index: {0} for tokens {1}'.format(start, self.token_map))
            fromToken = False
        else:
            fromToken = True
        if to not in self.token_map:
            print('There is no token at index: {0} for tokens {1}'.format(to, self.token_map))
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
            self.edges.append(Edge(self.token_map[start], self.token_map[to], label, span_type, render_type=EdgeRenderType.span,
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
            self.edges.append(Edge(self.token_map[start], self.token_map[to], label, dep_type,
                                    render_type=EdgeRenderType.dependency, description=des, is_final=is_final))

    """
     * Adds the given collection of tokens to this instance.
     *
     * @param tokens the tokens to add.
    """
    def addTokens(self, tokens: tuple):
        self.tokens.extend(tokens)
        for t in tokens:
            self.token_map[t.index] = t

    """
     * Adds the given edges to this instance.
     *
     * @param edges the edges to add.
    """
    def addEdges(self, edges: list):
        self.edges.extend(edges)

    """
     * Merges the given instance with this instance. A merge will add for every token i all properties of the token i of
     * the passed instance <code>nlp</code>. It will also add every edge between i and i in the given instance
     * <code>nlp</code> as an edge between the tokens i and j of this instance, using the same type, label and
     * rendertype as the original edge.
     *
     * @param nlp the instance to merge into this instance.
    """
    def merge(self, nlp):
        for i in range(0, min(len(self.tokens), len(nlp.tokens))):
            self.tokens[i].merge(nlp.tokens(i))
        for edge in nlp.edges():
            self.addEdge(start=edge.start.index, to=edge.to.index, label=edge.label, edge_type=edge.edge_type,
                         render_type=edge.render_type, note=edge.note)

    """
     * Adds token that has the provided properties with default property names.
     *
     * @param properties an vararray of strings.
    """
    def addTokenWithProperties(self, *properties):
        token = Token(len(self.tokens))
        for prop in properties:
            token.add_property(prop)
        self.tokens.append(token)
        self.token_map[token.index] = token

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
            vertex = Token(len(self.tokens), is_actual)
            self.tokens.append(vertex)
            self.token_map[vertex.index] = vertex
        else:
            vertex = self.token_map[index]
            if vertex is None:
                vertex = Token(index)
                self.token_map[vertex.index] = vertex

        return vertex

    """
     * If tokens were added with {@link com.googlecode.whatswrong.NLPInstance#addToken(int)} this method ensures that
     * all internal representations of the token sequence are consistent.
    """
    def consistify(self):
        self.tokens.extend(self.token_map.values())
        self.tokens.sort()

    """
     * Add a split point token index.
     *
     * @param tokenIndex a token index at which the instance should be split.
    """
    def addSplitPoint(self, tokenIndex: int):
        self.split_points.append(tokenIndex)

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
        return frozenset({e for e in self.edges if e.render_type == render_type or render_type is None})

    """
     * Returns the token at the given index.
     *
     * @param index the index of the token to return
     * @return the token at the given index.
    """
    def getToken(self, index: int) -> Token:
        return self.token_map[index]


    """
     * Returns a string representation of this instance. Mostly for debugging purposes.
     *
     * @return a string representation of this instance.
    """
    def __str__(self):
        return "{0}\n{1}\n{2}".format(", ".join(str(token) for token in self.tokens),
                                      ", ".join(str(v) for v in self.token_map.values()),
                                      ", ".join(str(e) for e in self.edges))
