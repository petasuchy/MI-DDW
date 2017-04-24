import operator

import networkx as nx
import pprint as pp


def loadInput(inputFile):
    text = None
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
    return graph


def printBasic(graph):
    print("Graph has {} nodes, {} edges and {} components.".format(graph.number_of_nodes(), graph.number_of_edges(),nx.number_connected_components(graph)))
    print("It's density is {}".format(nx.density(graph)))

def printCentralities(graph, full):
    print("\nCentrality:")

    degreeCentrality = nx.degree_centrality(graph)
    eigenvectorCentrality = nx.eigenvector_centrality(graph)
    for actor, centrality in degreeCentrality.items():
        graph.node[actor]["dg_cent"] = centrality
    for actor, centrality in eigenvectorCentrality.items():
        graph.node[actor]["ev_cent"] = centrality
    print("Top5 by degree centrality: {}".format(sorted(degreeCentrality.items(), key=operator.itemgetter(1), reverse=True)[:5]))
    print("Top5 by eigen vector centrality: {}".format(sorted(eigenvectorCentrality.items(), key=operator.itemgetter(1), reverse=True)[:5]))

    if full:
        closenessCentrality = nx.closeness_centrality(graph)
        betweennessCentrality = nx.betweenness_centrality(graph)
        for actor, centrality in closenessCentrality.items():
            graph.node[actor]["cs_cent"] = centrality
        for actor, centrality in betweennessCentrality.items():
            graph.node[actor]["bt_cent"] = centrality
        print("Top5 by closeness centrality: {}".format(sorted(closenessCentrality.items(), key=operator.itemgetter(1), reverse=True)[:5]))
        print("Top5 by betweenness centrality: {}".format(sorted(betweennessCentrality.items(), key=operator.itemgetter(1), reverse=True)[:5]))

def printKevinBacon(graph):
    print("\nKevin Bacon Number to James Stewart:")
    kbnumbers = nx.single_source_shortest_path_length(graph, "James Stewart")
    sum = 0
    actors = 0
    for actor, kbnumber in kbnumbers.items():
        graph.node[actor]["KevinBaconNumber"]=kbnumber
        sum += kbnumber
        actors +=1
    print("Average Kevin Becon number is {}".format(sum/actors))
    print("Lowest (closest) top10: {}".format(sorted(kbnumbers.items(), key=operator.itemgetter(1), reverse=False)[:10]))
    print("Highest (farthest) top10: {}".format(sorted(kbnumbers.items(), key=operator.itemgetter(1), reverse=True)[:10]))

def exportGraph(graph):
    nx.write_gexf(graph, 'graph.gexf')

# MAIN
inputFile = "/home/petr/skola/DDW/ddw-hw4/casts.csv"
graph = loadInput(inputFile)
# printBasic(graph)
# printCentralities(graph, False)
printKevinBacon(graph)
exportGraph(graph)

