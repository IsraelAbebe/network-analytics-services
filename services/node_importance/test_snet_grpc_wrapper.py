import unittest
from node_importance import NodeImportance

import networkx as nx
import numpy as np
from client import ClientTest
from server import *

from service_spec import node_importance_pb2
from service_spec import node_importance_pb2_grpc


class TestNodeImportance(unittest.TestCase):

    def setUp(self):
        self.server = Server()
        self.server.start_server()
        self.client = ClientTest()
        self.stub = self.client.open_grpc_channel()
        self.graph = {
            "nodes": ['1', '2', '3', '4', '5', '6', '7', '8'],
            "edges": [['1', '2'], ['1', '4'], ['2', '3'], ['2', '5'], ['3', '4'], ['3', '6'], ['2', '7'], ['3', '8']],
            "weights": [3, 4, 5, 6, 7, 8, 9, 10]
        }
        self.graph_01 = {
            "edges": [['1', '2'], ['1', '4'], ['2', '3'], ['2', '5'], ['3', '4'], ['3', '6'], ['2', '7'], ['3', '8']],
            "weights": [3, 4, 5, 6, 7, 8, 9, 10]
        }
        self.graph_02 = {
            "nodes": ['1', '2', '3', '4', '5', '6', '7', '8'],
            "weights": [3, 4, 5, 6, 7, 8, 9, 10]
        }
        self.graph_03 = {
            "nodes": ['1', '2', '3', '4', '5', '6', '7', '8'],
            "edges": [['1', '2'], ['1', '4'], ['2', '3'], ['2', '5'], ['3', '4'], ['3', '6'], ['2', '7'], ['3', '8']]
        }
        self.graph_04 = {
            "nodes": ['1', '2', '3', '4', '5', '6', '7', '8'],
            "edges": [['1', '2'], ['1', '4'], ['2', '3'], ['2', '5'], ['3', '4'], ['3', '6'], ['2', '7'], ['3', '8']],
            "weights": [3, 4, 5, 6, 7]
        }

    def test_find_central_nodes(self):
        expected_result = {
            'central_nodes': {'1': 0.5, '2': 0.7, '3': 0.7, '4': 0.5, '5': 0.4375, '6': 0.4375, '7': 0.4375,
                              '8': 0.4375}}
        centalnodes_output_key = []
        centralnodes_output_value = []
        for k, v in expected_result["central_nodes"].items():
            centalnodes_output_key.append(k)
            centralnodes_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=centalnodes_output_key,
                                                output=centralnodes_output_value)

        # Default Test
        result = self.client.find_central(self.stub, self.graph)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # # Non Default Test

        expected_result = {
            'central_nodes': {'1': 0.1}}

        centalnodes_output_key = []
        centralnodes_output_value = []
        for k, v in expected_result["central_nodes"].items():
            centalnodes_output_key.append(k)
            centralnodes_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=centalnodes_output_key,
                                                output=centralnodes_output_value)

        result = self.client.find_central(self.stub, self.graph, u='1', distance='weight', wf_improved=False,
                                          reverse=True)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # # Graph With No Nodes Test
        result = self.client.find_central(self.stub, self.graph_01)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})
        #
        # # Graph With No edges Test
        result = self.client.find_central(self.stub, self.graph_02)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1],
                         "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})
        #
        # # Non Weighted Graph
        expected_result = {
            'central_nodes': {'1': 0.5, '2': 0.7, '3': 0.7, '4': 0.5, '5': 0.4375, '6': 0.4375, '7': 0.4375,
                              '8': 0.4375}}
        centalnodes_output_key = []
        centralnodes_output_value = []
        for k, v in expected_result["central_nodes"].items():
            centalnodes_output_key.append(k)
            centralnodes_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=centalnodes_output_key,
                                                output=centralnodes_output_value)

        result = self.client.find_central(self.stub, self.graph_03)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

    def test_find_Periphery(self):
        expected_result = ['1', '4', '5', '6', '7', '8']
        output_nodes_list = node_importance_pb2.OutputNodesList(output_nodes=expected_result)

        # Default Test
        result = self.client.find_Periphery(self.stub, self.graph)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output_nodes_list)

        # Non Deafault test
        result = self.client.find_Periphery(self.stub, self.graph, usebounds=True)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output_nodes_list)

        # Graph With No Nodes Test
        result = self.client.find_Periphery(self.stub, self.graph_01)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph With No edges Test
        result = self.client.find_Periphery(self.stub, self.graph_02)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # weight less graph test
        result = self.client.find_Periphery(self.stub, self.graph_03)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output_nodes_list)

    def test_find_degree_centrality(self):
        # Out Degree Centrality Test
        expected_output_out = {
            'outdegree_centrality': {'1': 0.2857142857142857, '2': 0.42857142857142855, '3': 0.42857142857142855,
                                     '4': 0.0, '5': 0.0, '6': 0.0, '7': 0.0, '8': 0.0}}

        centrality_output_edges = []
        centrality_output_value = []
        for k, v in expected_output_out["outdegree_centrality"].items():
            centrality_output_edges.append(k)
            centrality_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=centrality_output_edges,
                                                output=centrality_output_value)

        result = self.client.find_degree_centrality(self.stub, self.graph, in_out='out')
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Graph With No Nodes Test
        result = self.client.find_degree_centrality(self.stub, self.graph_01, in_out='out')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})
        # Graph With No edges Test
        result = self.client.find_degree_centrality(self.stub, self.graph_02, in_out='out')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # In Degree Centrality Test
        expected_output_in = {'indegree_centrality': {'1': 0.0, '2': 0.14285714285714285, '3': 0.14285714285714285,
                                                      '4': 0.2857142857142857, '5': 0.14285714285714285,
                                                      '6': 0.14285714285714285,
                                                      '7': 0.14285714285714285, '8': 0.14285714285714285}}

        centrality_output_edges = []
        centrality_output_value = []
        for k, v in expected_output_in["indegree_centrality"].items():
            centrality_output_edges.append(k)
            centrality_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=centrality_output_edges,
                                                output=centrality_output_value)

        result = self.client.find_degree_centrality(self.stub, self.graph, in_out='in')
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Graph With No Nodes Test
        result = self.client.find_degree_centrality(self.stub, self.graph_01, in_out='in')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph With No edges Test
        result = self.client.find_degree_centrality(self.stub, self.graph_02, in_out='in')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # Default Degree Centrality Test
        expected_result = {
            'degree_centrality': {'1': 0.2857142857142857, '2': 0.5714285714285714, '3': 0.5714285714285714,
                                  '4': 0.2857142857142857, '5': 0.14285714285714285, '6': 0.14285714285714285,
                                  '7': 0.14285714285714285, '8': 0.14285714285714285}}
        centrality_output_edges = []
        centrality_output_value = []
        for k, v in expected_result["degree_centrality"].items():
            centrality_output_edges.append(k)
            centrality_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=centrality_output_edges,
                                                output=centrality_output_value)

        result = self.client.find_degree_centrality(self.stub, self.graph)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Graph With No Nodes Test
        result = self.client.find_degree_centrality(self.stub, self.graph_01)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph With No edges Test
        result = self.client.find_degree_centrality(self.stub, self.graph_02)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # Directed Test
        result = self.client.find_degree_centrality(self.stub, self.graph, directed=True)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Weight Less Graph
        result = self.client.find_degree_centrality(self.stub, self.graph_03)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

    def test_find_closeness_centrality(self):
        # Default Test
        result = self.client.find_closeness_centrality(self.stub, self.graph, ['1', '2'])
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(
            ("2" in str(result.output) and "1" in str(result.output) and
             "3" in str(result.output) and "4" in str(result.output) and
             "5" in str(result.output) and "6" in str(result.output) and
             "7" in str(result.output) and "8" in str(result.output)), True)

        self.assertEqual(
            ("0.5714285714285714" in str(result.output) and "0.75" in str(result.output) and
             "0.8571428571428571" in str(result.output) and "1.2" in str(result.output)) and "0.8" in str(
                result.output), True)

        # Graph With No Nodes Test
        result = self.client.find_closeness_centrality(self.stub, self.graph_01, ['1', '2'])
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph With No edges Test
        result = self.client.find_closeness_centrality(self.stub, self.graph_02, ['1', '2'])
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # Directed test
        result = self.client.find_closeness_centrality(self.stub, self.graph, ['1', '2'], directed=True)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(
            ("2" in str(result.output) and "1" in str(result.output) and
             "3" in str(result.output) and "4" in str(result.output) and
             "5" in str(result.output) and "6" in str(result.output) and
             "7" in str(result.output) and "8" in str(result.output)), True)

        self.assertEqual(
            ("0.5714285714285714" in str(result.output) and "0.75" in str(result.output) and
             "0.8571428571428571" in str(result.output) and "1.2" in str(result.output)) and "0.8" in str(
                result.output), True)

    def test_find_betweenness_centrality(self):
        # Default Test
        expected_result = {
            'betweenness_centrality': {'1': 0.07142857142857142, '2': 0.5952380952380952, '3': 0.5952380952380952,
                                       '4': 0.07142857142857142, '5': 0.0, '6': 0.0, '7': 0.0, '8': 0.0}}

        betweenness_output_edges = []
        betweenness_output_value = []
        for k, v in expected_result["betweenness_centrality"].items():
            betweenness_output_edges.append(node_importance_pb2.Edge(edge=k))
            betweenness_output_value.append(v)

        output = node_importance_pb2.BetweennessOutput(edge=betweenness_output_edges,
                                                       output=betweenness_output_value)
        result = self.client.find_betweenness_centrality(self.stub, self.graph)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Non Default Test
        expected_output_arumented = {
            'betweenness_centrality': {'1': 4.0, '2': 14.0, '3': 28.0, '4': 6.0, '5': 4.0, '6': 4.0, '7': 4.0,
                                       '8': 4.0}}

        result = self.client.find_betweenness_centrality(self.stub, self.graph, k=1, normalized=False, weight=True,
                                                         endpoints=True, seed=1)

        betweenness_output_edges = []
        betweenness_output_value = []
        for k, v in expected_output_arumented["betweenness_centrality"].items():
            betweenness_output_edges.append(node_importance_pb2.Edge(edge=k))
            betweenness_output_value.append(v)

        output = node_importance_pb2.BetweennessOutput(edge=betweenness_output_edges,
                                                       output=betweenness_output_value)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Graph With No Nodes Test
        result = self.client.find_betweenness_centrality(self.stub, self.graph_01)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph With No edges Test
        result = self.client.find_betweenness_centrality(self.stub, self.graph_02)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # Directed Test
        result = self.client.find_betweenness_centrality(self.stub, self.graph, k=1, normalized=False,
                                                         weight=True,
                                                         endpoints=True, seed=1, directed=True)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # weight less test
        expected_out = {
            'betweenness_centrality': {'1': 4.0, '2': 14.0, '3': 28.0, '4': 6.0, '5': 4.0, '6': 4.0, '7': 4.0,
                                       '8': 4.0}}

        result = self.client.find_betweenness_centrality(self.stub, self.graph, k=1, normalized=False, weight=True,
                                                         endpoints=True, seed=1)

        betweenness_output_edges = []
        betweenness_output_value = []
        for k, v in expected_out["betweenness_centrality"].items():
            betweenness_output_edges.append(node_importance_pb2.Edge(edge=k))
            betweenness_output_value.append(v)

        output = node_importance_pb2.BetweennessOutput(edge=betweenness_output_edges,
                                                       output=betweenness_output_value)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Non Default Test 2 edge
        expected_output_arumented = {
            'betweenness_centrality': {('1', '2'): 0.25, ('1', '4'): 0.25, ('2', '3'): 1.75, ('2', '5'): 0.5,
                                       ('2', '7'): 0.5, ('3', '4'): 0.75, ('3', '6'): 0.5, ('3', '8'): 0.5}}

        betweenness_output_edges = []
        betweenness_output_value = []

        for k, v in expected_output_arumented["betweenness_centrality"].items():
                    betweenness_output_edges.append(node_importance_pb2.Edge(edge=[k[0], k[1]]))
                    betweenness_output_value.append(v)

        output = node_importance_pb2.BetweennessOutput(edge=betweenness_output_edges,
                                                       output=betweenness_output_value)

        result = self.client.find_betweenness_centrality(self.stub, self.graph, k=1, normalized=False, weight=True,
                                                         type='edge', seed=1)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

    def test_find_pagerank(self):
        # Default Test
        expected_output = {'pagerank': {'1': 0.12113884704299357, '2': 0.23955113750178236, '3': 0.23955113750178236,
                                        '4': 0.12113884704299356, '5': 0.06965500772761204, '6': 0.06965500772761204,
                                        '7': 0.06965500772761204, '8': 0.06965500772761204}}

        pagerank_output_edges = []
        pagerank_output_value = []
        for k, v in expected_output["pagerank"].items():
            pagerank_output_edges.append(k)
            pagerank_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=pagerank_output_edges, output=pagerank_output_value)
        result = self.client.find_pagerank(self.stub, self.graph)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Non Default Test
        expected_output_arg = {'pagerank': {'1': 0.1235330285883424, '2': 0.24675733054250018, '3': 0.24675733054250013,
                                            '4': 0.12353302858834242, '5': 0.06485482043457871,
                                            '6': 0.06485482043457873, '7': 0.06485482043457871,
                                            '8': 0.06485482043457873}}

        pagerank_output_edges = []
        pagerank_output_value = []
        for k, v in expected_output_arg["pagerank"].items():
            pagerank_output_edges.append(k)
            pagerank_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=pagerank_output_edges, output=pagerank_output_value)
        result = self.client.find_pagerank(self.stub, self.graph, alpha=0.95,
                                           personalization={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                            '6': 0.125, '7': 0.125, '8': 0.125}, max_iter=100,
                                           tol=1e-07,
                                           nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1},
                                           weight=True,
                                           dangling={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                     '6': 0.125, '7': 0.125, '8': 0.125})
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Graph With No Nodes Test
        result = self.client.find_pagerank(self.stub, self.graph_01)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph With No edges Test
        result = self.client.find_pagerank(self.stub, self.graph_02)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # Directed Test
        result = self.client.find_pagerank(self.stub, self.graph, alpha=0.95,
                                           personalization={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                            '6': 0.125, '7': 0.125, '8': 0.125}, max_iter=100,
                                           tol=1e-07,
                                           nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1},
                                           weight=True,
                                           dangling={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                     '6': 0.125, '7': 0.125, '8': 0.125}, directed=True)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # weight less test
        expected_output = {'pagerank': {'1': 0.12113884704299357, '2': 0.23955113750178236, '3': 0.23955113750178236,
                                        '4': 0.12113884704299356, '5': 0.06965500772761204, '6': 0.06965500772761204,
                                        '7': 0.06965500772761204, '8': 0.06965500772761204}}
        pagerank_output_edges = []
        pagerank_output_value = []
        for k, v in expected_output["pagerank"].items():
            pagerank_output_edges.append(k)
            pagerank_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=pagerank_output_edges, output=pagerank_output_value)

        result = self.client.find_pagerank(self.stub, self.graph_03)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

    def test_find_eigenvector_centrality(self):
        # Default test
        expected_output = {
            'eigenvector_centrality': {'1': 0.35775018836999806, '2': 0.5298994260311778, '3': 0.5298994260311778,
                                       '4': 0.35775018836999806, '5': 0.2135666184274351, '6': 0.2135666184274351,
                                       '7': 0.2135666184274351, '8': 0.2135666184274351}}

        eigenvector_output_edges = []
        eigenvector_output_value = []
        for k, v in expected_output["eigenvector_centrality"].items():
            eigenvector_output_edges.append(k)
            eigenvector_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=eigenvector_output_edges,
                                                output=eigenvector_output_value)

        result = self.client.find_eigenvector_centrality(self.stub, self.graph, )
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # non Default Test
        expected_output_nstart = {
            'eigenvector_centrality': {'1': 0.35774203080090017, '2': 0.5299019638339402, '3': 0.5299019638339402,
                                       '4': 0.3577420308009002, '5': 0.21357030238703748, '6': 0.21357030238703748,
                                       '7': 0.21357030238703748, '8': 0.21357030238703748}}

        eigenvector_output_edges = []
        eigenvector_output_value = []
        for k, v in expected_output_nstart["eigenvector_centrality"].items():
            eigenvector_output_edges.append(k)
            eigenvector_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=eigenvector_output_edges,
                                                output=eigenvector_output_value)

        result = self.client.find_eigenvector_centrality(self.stub, self.graph, max_iter=110, tol=1e-05,
                                                         nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1,
                                                                 '8': 1}, weight=True, directed=False)
        # print(result)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # Graph With No Nodes Test
        result = self.client.find_eigenvector_centrality(self.stub, self.graph_01)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph With No edges Test
        result = self.client.find_eigenvector_centrality(self.stub, self.graph_02)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # directed Test
        result = self.client.find_eigenvector_centrality(self.stub, self.graph, max_iter=110, tol=1e-05,
                                                         nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1,
                                                                 '8': 1}, weight=True, directed=True)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

        # weight less Test
        expected_out = {
            'eigenvector_centrality': {'1': 0.35775018836999806, '2': 0.5298994260311778, '3': 0.5298994260311778,
                                       '4': 0.35775018836999806, '5': 0.2135666184274351, '6': 0.2135666184274351,
                                       '7': 0.2135666184274351, '8': 0.2135666184274351}}
        eigenvector_output_edges = []
        eigenvector_output_value = []
        for k, v in expected_out["eigenvector_centrality"].items():
            eigenvector_output_edges.append(k)
            eigenvector_output_value.append(v)

        output = node_importance_pb2.DictOutput(edge=eigenvector_output_edges,
                                                output=eigenvector_output_value)

        result = self.client.find_eigenvector_centrality(self.stub, self.graph_03)
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        self.assertEqual(result.output, output)

    def test_find_hits(self):
        # Hub Matrix Hits Test with default node
        hub_matrix_expected_out = {
            'hub_matrix': [[25.0, 0.0, 43.0, 0.0, 18.0, 0.0, 27.0, 0.0], [0.0, 151.0, 0.0, 47.0, 0.0, 40.0, 0.0, 50.0],
                           [43.0, 0.0, 238.0, 0.0, 30.0, 0.0, 45.0, 0.0], [0.0, 47.0, 0.0, 65.0, 0.0, 56.0, 0.0, 70.0],
                           [18.0, 0.0, 30.0, 0.0, 36.0, 0.0, 54.0, 0.0], [0.0, 40.0, 0.0, 56.0, 0.0, 64.0, 0.0, 80.0],
                           [27.0, 0.0, 45.0, 0.0, 54.0, 0.0, 81.0, 0.0], [0.0, 50.0, 0.0, 70.0, 0.0, 80.0, 0.0, 100.0]]}

        hits_list = []
        for i in hub_matrix_expected_out["hub_matrix"]:
            hits_list.append(node_importance_pb2.HitsOutput(hits_out=list(i)))

        result = self.client.find_hits(self.stub, self.graph, nodelist=None, mode='hub_matrix')
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        for i in range(len(result.output)):
            self.assertEqual(result.output[i], hits_list[i])

        # Authority Matrix Hits Test with default node
        authority_matrix_expected_out = {
            'authority_matrix': [[25.0, 0.0, 43.0, 0.0, 18.0, 0.0, 27.0, 0.0],
                                 [0.0, 151.0, 0.0, 47.0, 0.0, 40.0, 0.0, 50.0],
                                 [43.0, 0.0, 238.0, 0.0, 30.0, 0.0, 45.0, 0.0],
                                 [0.0, 47.0, 0.0, 65.0, 0.0, 56.0, 0.0, 70.0],
                                 [18.0, 0.0, 30.0, 0.0, 36.0, 0.0, 54.0, 0.0],
                                 [0.0, 40.0, 0.0, 56.0, 0.0, 64.0, 0.0, 80.0],
                                 [27.0, 0.0, 45.0, 0.0, 54.0, 0.0, 81.0, 0.0],
                                 [0.0, 50.0, 0.0, 70.0, 0.0, 80.0, 0.0, 100.0]]}
        hits_list = []
        for i in authority_matrix_expected_out["authority_matrix"]:
            hits_list.append(node_importance_pb2.HitsOutput(hits_out=list(i)))

        result = self.client.find_hits(self.stub, self.graph, nodelist=None, mode='authority_matrix')
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        for i in range(len(result.output)):
            self.assertEqual(result.output[i], hits_list[i])

        # Hub Matrix Hits Test with  node

        expected_with_node_hub = {'hub_matrix': [[9.0, 0.0], [0.0, 9.0]]}

        result = self.client.find_hits(self.stub, self.graph, nodelist=['1', '2'], mode='hub_matrix')
        hits_list = []
        for i in expected_with_node_hub["hub_matrix"]:
            hits_list.append(node_importance_pb2.HitsOutput(hits_out=list(i)))

        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        for i in range(len(result.output)):
            self.assertEqual(result.output[i], hits_list[i])

        # Authority Matrix Hits Test with  node

        expected_with_node_authority = {'authority_matrix': [[9.0, 0.0], [0.0, 9.0]]}

        result = self.client.find_hits(self.stub, self.graph, nodelist=['1', '2'], mode='authority_matrix')
        hits_list = []
        for i in expected_with_node_authority["authority_matrix"]:
            hits_list.append(node_importance_pb2.HitsOutput(hits_out=list(i)))

        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        for i in range(len(result.output)):
            self.assertEqual(result.output[i], hits_list[i])

        # Graph With No Nodes Test
        result = self.client.find_hits(self.stub, self.graph_01, mode='authority_matrix')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        result = self.client.find_hits(self.stub, self.graph_01, mode='hub_matrix')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph With No edges Test
        result = self.client.find_hits(self.stub, self.graph_02, mode='authority_matrix')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        result = self.client.find_hits(self.stub, self.graph_02, mode='hub_matrix')
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "Parameter to MergeFrom() must be instance of same class: expected Graph got list.")
        self.assertEqual(result[2], {})

        # directed Graph test

        expected_with_node_authority = {'hub_matrix': [[9.0, 0.0], [0.0, 9.0]]}

        result = self.client.find_hits(self.stub, self.graph, nodelist=['1', '2'], directed=True)
        hits_list = []
        for i in expected_with_node_authority["hub_matrix"]:
            hits_list.append(node_importance_pb2.HitsOutput(hits_out=list(i)))

        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        for i in range(len(result.output)):
            self.assertEqual(result.output[i], hits_list[i])

        # weightless test
        expected_result = {'hub_matrix': [[1.0, 0.0], [0.0, 1.0]]}

        hits_list = []
        for i in expected_result["hub_matrix"]:
            hits_list.append(node_importance_pb2.HitsOutput(hits_out=list(i)))

        result = self.client.find_hits(self.stub, self.graph_03, nodelist=['1', '2'])
        self.assertEqual(result.status, True)
        self.assertEqual(result.message, 'success')
        for i in range(len(result.output)):
            self.assertEqual(result.output[i], hits_list[i])

    def test_additional(self):
        # wrong Number of wrights test taking one functionality as example
        result = self.client.find_central(self.stub, self.graph_04)
        self.assertEqual(result.status, False)
        self.assertEqual(result.message, 'weights and edges must be equal')

    def tearDown(self):
        self.server.stop_server()


if __name__ == '__main__':
    suite = unittest.TestSuite()

    unittest.main()
