# Tested on python3.6

import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import random
import plotly as py
import plotly.graph_objs as go
import time
import math




class graphx:

    def __init__(self):

        # self.file = "book_readers"
        self.file = "food_pref"
        self.num_nodes = 0

    def create_bipartite_graph(self):

        self.read_file = "data/bipartite_data/"+self.file+".csv"
        self.file_df = pd.read_csv(self.read_file, encoding='ISO-8859-1')

        # This is the set of family members, only for the food_pref example
        first_column = set(self.file_df.iloc[:,0])
        print(type(first_column))
        # This is the set of food types
        second_column = set(self.file_df.iloc[0,:])
        print(first_column)
        print(second_column)



        self.B = nx.Graph()
        self.B.add_nodes_from(first_column, bipartite=0)
        self.B.add_nodes_from(second_column, bipartite=1)
        self.B.add_edges_from(self.file_df.values.tolist())
        print((self.file_df.values))
        print((self.file_df.values.tolist()))

        # Adding random locations for the nodes
        # Put towards center nodes that have the most connections perhaps?

        # Get descending list of nodes
        print('Degrees')
        print(self.B.degree())
        sorted_by_second = sorted(list(self.B.degree()), key=lambda tup: tup[1], reverse=True)
        sorted_nodes_list = []
        for s in sorted_by_second:
            sorted_nodes_list.append(s[0])
        print(sorted_nodes_list)
        print(sorted_nodes_list.__len__())

        interval = 0.5/float(len(self.B))
        print("interval =",interval)

        i = 0

        for node in self.B.nodes(data=True):

            # node[1]['pos'] = [random.uniform(0,1),random.uniform(0,1)]

            # theta = primes[i] * 2 * math.pi / 8
            theta = random.uniform(0.01,2 * math.pi-0.01)
            r = i * interval

            x = r * math.cos(theta) + 0.5
            y = r * math.sin(theta) + 0.5

            print(x,y)

            node[1]['pos'] = [x,y]

            i = i + 1


        # self.plot_graph(self.B,self.file)
        self.plot_graph_2(self.B,'Initial bipartite graph')
        print('initial bipartite graph')
        print(self.B.nodes())
        print(self.B.edges())
        print(bipartite.sets(self.B)[0])

    def projected_graph(self):
        E = bipartite.sets(self.B)[0]
        P = bipartite.projected_graph(self.B, E,multigraph=False)
        # self.plot_graph(P,'projected_gragh')
        self.plot_graph_2(P,'projected_gragh')
        print('projected_graph:number of edges:',P.number_of_edges())
        print(P.edges())
        print(list(P.edges(data=True)))
        print('kkkkkkkkkkkkkkkk')
        print(list(P.nodes()))
        print(P['Goeff'])
        P = bipartite.projected_graph(self.B, E, multigraph=True)
        # self.plot_graph(P, 'projected_gragh_multigraph')
        self.plot_graph_2(P, 'projected_gragh_multigraph')
        print('MMMMMMMMMMMMMMMMMMMMM')
        print(P.nodes())
        print(P.edges())
        # for e in P.edges():
        #     print(e)
        #     print(e['edge'])
        print('NNNNNNNNNNNNNNNNNNNNN')

    def weighted_projected_graph(self):

        # create a projection on one of the nodes
        E = bipartite.sets(self.B)[0]
        print('EEEEEEEEEEEEEEEEEEE')
        print(E)
        P = bipartite.weighted_projected_graph(self.B,E,ratio=True)

        # self.plot_graph(P,'weighted_projected')
        self.plot_graph_2(P,'weighted_projected')
        print('weighted_projected:number of edges:', P.number_of_edges())
        print(P.edges())
        print(list(P.edges(data=True)))
        weights = []
        for i in list(P.edges(data=True)):
            weights.append(i[2]['weight'])
        print(weights)

        P = bipartite.weighted_projected_graph(self.B, E, ratio=False)
        self.plot_graph_2(P, 'weighted_projected_not_ratio')
        print('RRRRRRRRRRRRRRRRRRRRRRRR')
        print(P.edges())
        weights=[]
        for i in list(P.edges(data=True)):
            weights.append(i[2]['weight'])
        print(weights)

    def collaboration_weighted_projected_graph(self):
        E = bipartite.sets(self.B)[0]
        P = bipartite.collaboration_weighted_projected_graph(self.B, E)
        self.plot_graph_2(P,'collaboration_weighted_projected')
        print('collaboration_weighted_projected:number of edges:', P.number_of_edges())
        print(P.edges())
        print(list(P.edges(data=True)))
        weights = []
        for i in list(P.edges(data=True)):
            weights.append(i[2]['weight'])
        print(weights)

    def overlap_weighted_projected_graph(self):
        E = bipartite.sets(self.B)[0]
        P = bipartite.overlap_weighted_projected_graph(self.B, E,jaccard=False)
        self.plot_graph_2(P,'overlap_weighted_projected_graph')
        print('overlap_weighted_projected_graph:number of edges:', P.number_of_edges())
        print(P.edges())
        print(list(P.edges(data=True)))
        weights = []
        for i in list(P.edges(data=True)):
            weights.append(i[2]['weight'])
        print(weights)
        P = bipartite.overlap_weighted_projected_graph(self.B, E, jaccard=True)
        self.plot_graph_2(P, 'overlap_weighted_projected_graph_jaccard_True')
        print('xxxxxxxxxxxxxxxxxxxxxx')
        weights = []
        for i in list(P.edges(data=True)):
            weights.append(i[2]['weight'])
        print(weights)

    def generic_weighted_projected_graph(self):
        E = bipartite.sets(self.B)[0]
        P = bipartite.generic_weighted_projected_graph(self.B, E)
        self.plot_graph_2(P, 'generic_weighted_projected_graph')
        print('generic_weighted_projected_graph:number of edges:', P.number_of_edges())
        print(P.edges())
        print(list(P.edges(data=True)))

    # ===============================================================
    # Assorted utilities and accessor functions
    # ===============================================================


    # helper function to plot graphs
    def plot_graph(self, G, title, weight_name=None):
        '''
        G: a networkx G
        weight_name: name of the attribute for plotting edge weights (if G is weighted)
        '''
        # % matplotlib notebook

        plt.figure()
        plt.title(title)
        pos = nx.spring_layout(G)
        edges = G.edges()
        weights = None

        if weight_name:
            weights = [int(G[u][v][weight_name]) for u, v in edges]
            labels = nx.get_edge_attributes(G, weight_name)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            nx.draw_networkx(G, pos, edges=edges, width=weights)
        else:
            nx.draw_networkx(G, pos, edges=edges)

        plt.show()

    def plot_graph_2(self, G,graph_label):


        edge_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        edge_weight_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            textposition='top center',
            marker=go.Marker(
                opacity=0
            )
        )


        for edge in G.edges(data=True):
            x0, y0 = G.node[edge[0]]['pos']
            x1, y1 = G.node[edge[1]]['pos']
            edge_trace['x'] += [x0, x1, None]
            edge_trace['y'] += [y0, y1, None]

            edge_weight_trace['x'].append((x0+x1)/2)
            edge_weight_trace['y'].append((y0+y1)/2)
            try:
                print('||||||||||||||||||||||||||||||')
                print(edge)
                edge_weight_trace['text'].append(round(edge[2]['weight'],3))
            except:
                print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
                edge_weight_trace['text'].append('')

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            textposition='bottom center'
            )

        for node in G.nodes():
            x, y = G.node[node]['pos']
            node_trace['x'].append(x)
            node_trace['y'].append(y)
            node_trace['text'].append(node)


        layout = go.Layout(
            title='<br>'+graph_label,
            titlefont=dict(size=16),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[dict(
                text='Network graph made for SNet',
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002)],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

        fig = go.Figure(data=[edge_trace, node_trace, edge_weight_trace],layout=layout)


        py.offline.plot(fig, filename=graph_label+'.html')


def sample_data_generation(file_name):

    persons = []
    books = []

    persons_count = 10
    books_count = 7
    books_per_person_count = 7

    for i in range(persons_count):
        persons.append('person_'+str(i))

    for i in range(books_count):
        books.append('book_'+str(i))

    print(persons)
    print(books)

    books_readers_bipartition = []

    for i in persons:
        indices_to_keep = random.sample(books,books_per_person_count)

        for j in indices_to_keep:
            books_readers_bipartition.append([i,j])

    print(books_readers_bipartition)

    print(len(books_readers_bipartition))

    pd.DataFrame(books_readers_bipartition,columns=['person','book']).to_csv('data/bipartite_data/'+file_name,index=False)



def run_create_bipartite_graph():
    bi = graphx()
    bi.create_bipartite_graph()

def run_projected_graph():
    bi = graphx()
    bi.create_bipartite_graph()
    bi.projected_graph()

def run_weighted_projected_graph():
    bi = graphx()
    bi.create_bipartite_graph()
    bi.weighted_projected_graph()

def run_collaboration_weighted_projected_graph():
    bi = graphx()
    bi.create_bipartite_graph()
    bi.collaboration_weighted_projected_graph()

def run_overlap_weighted_projected_graph():
    bi = graphx()
    bi.create_bipartite_graph()
    bi.overlap_weighted_projected_graph()

def run_combined_graphs():
    bi = graphx()
    bi.create_bipartite_graph()
    bi.projected_graph()
    bi.weighted_projected_graph()
    bi.collaboration_weighted_projected_graph()
    bi.overlap_weighted_projected_graph()
    bi.generic_weighted_projected_graph()

def misc_1():

    def jaccard(G, u, v):
        unbrs = set(G[u])

        vnbrs = set(G[v])
        return float(len(unbrs & vnbrs)) / len(unbrs | vnbrs)

    def my_weight(G, u, v, weight='weight'):
        w = 0
        print('@@@@@@@@@@@@@@@@')
        print(G)
        print((G[u]))
        print(type(u))
        print(G.edges())
        print(set(G[u]) & set(G[v]))
        for nbr in set(G[u]) & set(G[v]):
            print('{{{{{{{{{{{{{{{{{{')
            print((nbr))
            # print(G[u][nbr].get(weight, 6))
            # x0, y0 = G.node[edge[0]]['pos']
            w += G[u][nbr][weight] + G[v][nbr][weight]
            print('w=',w)
            # w += G[u][nbr].get(weight, 1) + G[v][nbr].get(weight, 1)
            # w += G.edge[u][nbr].get(weight, 1) + G.edge[v][nbr].get(weight, 1)
        return w

    B = nx.complete_bipartite_graph(2, 2)
    # B = nx.complete_bipartite_graph(3, 3)

    print('iiiiiiiiiiiiiiiiii')
    for edge in B.edges(data=True):
        print(edge)

    j = 1

    for i in B.edges(data=True):
        print('///////////////')
        # B[i[0]][i[1]]['weight'] = 22
        # print(B[i[0]])
        # print(B[i[0]][i[1]])
        i[2]['weight'] = j # B[i[0]][i[1]]['weight'] = 22 does the same thing
        j = j + 1



    for edge in B.edges(data=True):
        print(edge)

    G = bipartite.generic_weighted_projected_graph(B, [0, 1])
    # bi = graphx()
    # bi.plot_graph(B,'complete')
    # bi.plot_graph(G,'complete')
    print(G.edges(data=True))
    for edge in G.edges(data=True):
        # print()
        print(edge)

    G = bipartite.generic_weighted_projected_graph(B, [0, 1], weight_function=my_weight)
    print('Final value')

    print(G.edges(data=True))


__end__ = '__end__'

if __name__ == '__main__':

    # sample_data_generation('book_readers.csv')

    run_combined_graphs()
    # run_overlap_weighted_projected_graph()
    # run_collaboration_weighted_projected_graph()
    # run_weighted_projected_graph()
    # run_projected_graph()
    # run_create_bipartite_graph()
    #
    misc_1()
