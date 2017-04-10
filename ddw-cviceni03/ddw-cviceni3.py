import nltk
import networkx
import operator
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt


def _extract_entities(ne_chunked):
    data = {}
    for entity in ne_chunked:
        if isinstance(entity, nltk.tree.Tree):
            text = " ".join([word for word, tag in entity.leaves()])
            ent = entity.label()
            data[text] = ent
        else:
            continue
    return data


def get_entities(tokens):
    tagged = nltk.pos_tag(tokens)

    ne_chunked = nltk.ne_chunk(tagged, binary=True)
    return _extract_entities(ne_chunked)


# input text
text = None
with open('/home/petr/skola/DDW/ddw-cviceni02/1342-0.txt', 'r') as f:
    text = f.read()

sentences = [[t for t in nltk.word_tokenize(sentence)] for sentence in nltk.sent_tokenize(text)]

graph = networkx.Graph()

for sentence in sentences[:500]:
    entities = get_entities(sentence)
    for key, value in entities.items():
        graph.add_node(key)

    for key, value in entities.items():
        for key2, value2 in entities.items():
            graph.add_edge(key, key2)
print("Nodes count: {}, edges count: {}".format(len(graph.nodes()), len(graph.edges())))
print("Density of graph: {}".format(networkx.density(graph)))

print("\nTop 5 by degree\n{}".format(sorted(graph.degree().items(), key=operator.itemgetter(1), reverse=True)[:5]))
print("\nTop 5 by centrality\n{}".format(
    sorted(networkx.closeness_centrality(graph).items(), key=operator.itemgetter(1), reverse=True)[:5]))

sub_graphs = list(networkx.connected_component_subgraphs(graph))
n = len(sub_graphs)
for i in range(n):
    print("Subgraph:", i, "consists of ", sub_graphs[i].nodes())

