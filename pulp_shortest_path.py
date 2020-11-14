#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formulate a shortest path problem as a integer program
Model using PuLP modelling framework

Created on Thu Feb  8 21:16:52 2018
@author: niloy
"""

import networkx as nx
import pulp
import random


def path_sequence(list_of_links, source, target):
    """
    Convert set of tuples representing path in random order to a path
    :param list_of_links: set of tuples representing path
    :param source: source node
    :param target: destination node
    :return: pretty path as sequence of nodes
    """

    pretty_path = []
    nxt = source
    pretty_path.append(source)

    # iterate through list till target is reached
    while (nxt != target):
        for pair in list_of_links:
            if pair[0] == nxt:
                nxt = pair[1]
                pretty_path.append(nxt)
                list_of_links.remove(pair)

    return pretty_path


def ilp_shortest_path(digraph, metric, source, target):
    """
    :param digraph: networkx object representing directed graph
    :param metric: cost metric for shortest path
    :param source: source node
    :param target: destination node
    :param as_sequence: if true, return path as a sequence of nodes. Else, return path as sequence of tuples
    :return: shortest path from source to target
    """

    # input validity checks
    assert isinstance(
        digraph, nx.DiGraph), "Input is not a valid networkx digraph"
    assert 0 <= source <= digraph.number_of_nodes(), "Source not in range"
    assert 0 <= target <= digraph.number_of_nodes(), "Target not in range"

    # get costs
    cost = nx.get_edge_attributes(digraph, metric)
    assert cost, "Cost metric undefined"

    # get links
    links = []
    for i, j in digraph.edges:
        links.append((i, j))

    # instantiate the problem
    prob = pulp.LpProblem("Shortest Path Problem", pulp.LpMinimize)

    # create binary variables to state a link is chosen on shortest path
    var_dict = {}
    for i, j in digraph.edges:
        var = pulp.LpVariable('x_(%s,%s)' % (i, j), cat=pulp.LpBinary)
        var_dict[(i, j)] = var

    # formulate the objective
    prob += pulp.lpSum([cost[(i, j)] * var_dict[(i, j)] for (i, j) in links])

    # formulate the constraints
    for node in g.nodes:
        if node == source and node != target:
            prob += pulp.lpSum([var_dict[(i, j)] for (i, j) in links if i == node]) - \
                pulp.lpSum([var_dict[(j, i)]
                            for (j, i) in links if i == node]) == 1
        elif node == target and node != source:
            prob += pulp.lpSum([var_dict[(i, j)] for (i, j) in links if i == node]) - \
                pulp.lpSum([var_dict[(j, i)]
                            for (j, i) in links if i == node]) == -1
        else:
            prob += pulp.lpSum([var_dict[(i, j)] for (i, j) in links if i == node]) - \
                pulp.lpSum([var_dict[(j, i)]
                            for (j, i) in links if i == node]) == 0

    # solve the optimization problem
    prob.solve()

    # print additional info
    print("Status = {}".format(pulp.LpStatus[prob.status]))
    print("Total path delay = {}".format(pulp.value(prob.objective)))

    # get output links
    ilp_output = []
    for link in links:
        # links are active
        if var_dict[link].value() == 1.0:
            ilp_output.append(link)
    if not ilp_output:
        print("No link selected")

    return path_sequence(ilp_output, source, target)


if __name__ == '__main__':

    topo = nx.barabasi_albert_graph(20, 2)
    g = nx.DiGraph(topo)
    nx.draw(g, with_labels=True)

    dict_d = {}
    for edge in g.edges:
        dict_d[edge] = random.uniform(1.0, 20.0)

    nx.set_edge_attributes(g, dict_d, 'delay')

    shortest_path = ilp_shortest_path(g, metric='delay', source=0, target=5)
    print("The shortest path is {}".format(shortest_path))
