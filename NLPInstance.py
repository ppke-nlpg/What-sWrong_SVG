from Token import *
from Edge import *

from enum import Enum

class NLPInstance(object):
    # todo: this class needs a redesign, in particular with respect to token identities.

    class RenderType(Enum):
        # Show as single sentence with dependencies and spans
        single = 'single',
        # Show two aligned sentences, on top of each other
        alignment = 'alignment'

    # How to render this instance.

    # Returns the render type that controls which renderer to use.
    # @return the render type for this instance.
    @property
    def renderType(self):
        return self._renderType

    # Sets the render type for this instance.
    # @param renderType the render type for this instance
    @renderType.setter
    def renderType(self, value):
        self._renderType = value

    # Contains the edges of this instance.
    @property
    def edges(self):
        return tuple(self._edges)

    # Returns all edges of this instance.

    # @return all edges of this instance as unmodifiable list.
    @edges.setter
    def edges(self, value):
        self._edges = value

    # Contains the tokens of this instance.
    @property
    def tokens(self):
        return tuple(self._tokens)
        #return self._tokens

    @tokens.setter
    def tokens(self, value):
        self._tokens = value

    # Contains a mapping from sentence indices to tokens.
    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, value):
        self._map = value

    # A list of token indices at which the NLP instance is to be split. These indices can refer to sentence boundaries
    # in a document, but they can also indicate that what follows after a split point is an utterance in a different
    # language (for alignment).

    # Returns the list of split points for this instance. A split point is a point at which renderers can split the
    # token list.

    # @return the list of split points.
    @property
    def splitPoints(self):
        return tuple(self._splitPoints)

    @splitPoints.setter
    def splitPoints(self, value):
        self._splitPoints = value

    # Creates an empty NLPInstance without edges or tokens.

    # OR

    # Creates a new NLPInstance with the given tokens and edges. The passed collections will be copied and not
    # changed.

    # @param tokens      the tokens of the sentence.
    # @param edges       the edges of the sentence.
    # @param renderType  the render type for the instance.
    # @param splitPoints the points at which the instance can be split.
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
        self._splitPoints =[]
        if splitPoints is not None:
            self._splitPoints.extend(splitPoints)

    # Creates and adds an edge from the token at the given 'from' index to the token at the given 'to' index with the
    # given label and type. The edge will have the default render type.

    # @param from  index of the token the edge should start at. The token at the given index must already exist in the
    #              sentence.
    # @param to    index of the token edge should end at. The token at the given index must already exist in the
    #              sentence.
    # @param label the label of the edge.
    # @param type  the type of edge.
    # @param renderType the render type of the edge.
    # @param description description of the edge
    # @see com.googlecode.whatswrong.Edge

    # OR

    # Adds an edge.

    # @param edge the edge to add.
    def addEdge(self, edge = None, From = None, to = None, label = None, type = None, renderType = None,
                fromToken = None, toToken = None):
        if edge is not None:
            self._edges.append(Edge(self._map[edge.From.index], self._map[edge.to.index], edge.label, edge.note,
                            edge.type, edge.renderType, edge.description))
        else:
            if fromToken is not None and toToken is not None:
                self._edges.append(Edge(self._map[fromToken.index], self._map[toToken.index], label, type,
                                        renderType))
            else:
                #if self.isInvalidEdge(From, to):  # TODO ez így jó?
                #    pass
                #else:
                if From in self._map and to in self._map:
                    self._edges.append(Edge(self._map[From], self._map[to], label, type, renderType))

    # Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.RenderType#span}

    # @param from  index of the token the edge should start at. The token at the given index must already exist in the
    #              sentence.
    # @param to    index of the token edge should end at. The token at the given index must already exist in the
    #              sentence.
    # @param label the label of the edge.
    # @param type  the type of edge.
    # @param description the description of the span.
    # @see com.googlecode.whatswrong.Edge

    def addSpan(self, From, to, label, type, description = None):
        #if self.isInvalidEdge(From, to):
        #    return
        if From in self._map and to in self._map:
            self._edges.append(Edge(self._map[From], self._map[to], label, type, renderType=Edge.RenderType.span, description=description))

#    def isInvalidEdge(self, From, to):
#        fromToken = self._map[From]
#        toToken = self._map[to]
#        if fromToken is None:
#            print('There is no token at index: ' + str(From) + ' for tokens ' + str(self._map))
#        if toToken is None:
#            print('There is no token at index: ' + str(to) + ' for tokens ' + str(self._map))
#        return toToken is None or fromToken is None

    # Creates and adds an edge with rendertype {@link com.googlecode.whatswrong.Edge.RenderType#dependency}
    #
    # @param from  index of the token the edge should start at. The token at the given index must already exist in the
    #              sentence.
    # @param to    index of the token edge should end at. The token at the given index must already exist in the
    #              sentence.
    # @param label the label of the edge.
    # @param type  the type of edge.
    # @param description description of the edge
    # @see com.googlecode.whatswrong.Edge

    def addDependency(self, From, to, label, type, description = None):
        #if self.isInvalidEdge(From, to):
        #    return
        fromToken = self._map[From]
        toToken = self._map[to]
        edge = Edge(fromToken, toToken, label, type, renderType=Edge.RenderType.dependency)
        if description is not None:
            edge.description = description
        self._edges.append(edge)

    # Adds the given collection of tokens to this instance.

    # @param tokens the tokens to add.
    def addTokens(self, tokens):
        self._tokens.extend(tokens)
        for t in tokens:
            self._map[t.index] = t

    # Adds the given edges to this instance.

    # @param edges the edges to add.
    def addEdges(self, edges):
        self._edges.extend(edges)

    # Merges the given instance with this instance. A merge will add for every token i all properties of the token i of
    # the passed instance <code>nlp</code>. It will also add every edge between i and i in the given instance
    # <code>nlp</code> as an edge between the tokens i and j of thxis instance, using the same type, label and
    # rendertype as the original edge.

    # @param nlp the instance to merge into this instance.
    def merge(self, nlp):
        for i in range(0, min(len(self._tokens), len(nlp.tokens))):
            self._tokens[i].merge(nlp.tokens(i))
        for edge in nlp.edges():
            self.addEdge(edge.From().index(), edge.to().index(), edge.label(), edge.type(), edge.renderType())

    # Adds token that has the provided properties with default property names.

    # @param properties an vararray of strings.
    def addTokenWithProperties(self, *properties):
        token = Token(len(self._tokens))
        for prop in properties:
            token.addProperty(prop)
        self._tokens.append(token)
        self._map[token.index] = token

    # Adds a new token and returns it.

    # @return the token that was added.
    def addToken(self, index = None):
        if index is None:
            vertex = Token(str(len(self._tokens)))
        else:
            vertex = self._map[index]
            if vertex is None:
                return None
        self._tokens.append(vertex)
        self._map[vertex.index] = vertex
        return vertex

    # If tokesn were added with {@link com.googlecode.whatswrong.NLPInstance#addToken(int)} this method ensures that
    # all internal representations of the token sequence are consistent.
    def consistify(self):
        self._tokens.extend(self._map.values())

    # Add a split point token index.

    # @param tokenIndex a token index at which the instance should be split.
    def addSplitPoint(self, tokenIndex):
        self._splitPoints.append(tokenIndex)

    # Returns all edges of this instance with the given render type.

    # @param renderType the render type of the edges to return.
    # @return all edges of this instance with the given render type. This list can be altered if needed.
    def getEdges(self, renderType = None):
        result = []
        if renderType is not None:
            for e in self._edges:
                if e.renderType == renderType:
                    result.append(e)
        return result

    # Returns the token at the given index.

    # @param index the index of the token to return
    # @return the token at the given index.
    def getToken(self, index):
        return self._map[index]

    def __str__(self):
        value = ""
        for token in self._tokens:
            value += str(token) + ", "
        value += '\n'
        for v in self._map.values():
            value +=  str(v) + ", "
        value += '\n'
        for e in self._edges:
            value += str(e) + ", "
        return value




