import operator
import networkx as nx
import pprint as pp

text = None
inputFile = "/home/petr/skola/DDW/ddw-hw4/casts.csv"
with open(inputFile, 'r') as f:
    text = f.read()

graph = nx.Graph()
casts = dict()

lines = text.splitlines()
for line in lines:
    movie = line.split(";")[1].split("\"")[1]
    actor = line.split(";")[2].split("\"")[1]
    if len(actor) > 5:
        if movie in casts:
            casts[movie].append(actor)
        else:
            casts[movie] = [actor]
# pp.pprint(casts)

for key in casts:
    for actor in casts.get(key):
        graph.add_node(actor)
        for partner in casts.get(key):
            if partner != actor:
                graph.add_edge(actor, partner)
# print(graph.has_edge("Pam Tyson", "Brad Pitt"))

print("Graph has {} nodes and {} edges.".format(graph.number_of_nodes(), graph.number_of_edges()))
print("It's density is {}".format(nx.density(graph)))
