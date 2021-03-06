import unittest
from node_importance import NodeImportance
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import check_graph_validity


class TestNodeImportance(unittest.TestCase):

    def setUp(self):
        self.N = NodeImportance()
        self.cv = check_graph_validity.Graphs()
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
        # Default Test
        result = self.N.find_central_nodes(self.graph)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'central_nodes': {'1': 0.5, '2': 0.7, '3': 0.7, '4': 0.5, '5': 0.4375, '6': 0.4375, '7': 0.4375,
                              '8': 0.4375}})

        # Non Default Test
        result = self.N.find_central_nodes(self.graph, u='1', distance='weight', wf_improved=False, reverse=True)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {'central_nodes': 0.1})

        # # Non weighted Test
        result = self.N.find_central_nodes(self.graph_03)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'central_nodes': {'1': 0.5, '2': 0.7, '3': 0.7, '4': 0.5, '5': 0.4375, '6': 0.4375, '7': 0.4375,
                              '8': 0.4375}})

    def test_find_Periphery(self):
        # Default Test
        result = self.N.find_Periphery(self.graph)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {'periphery': ['1', '4', '5', '6', '7', '8']})

        # Non Default Test
        result = self.N.find_Periphery(self.graph, usebounds=True)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {'periphery': ['1', '4', '5', '6', '7', '8']})

        # Non weighted Test
        result = self.N.find_Periphery(self.graph_03)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {'periphery': ['1', '4', '5', '6', '7', '8']})

    def test_find_degree_centrality(self):
        # Default Test
        result = self.N.find_degree_centrality(self.graph)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'degree_centrality': {'1': 0.2857142857142857, '2': 0.5714285714285714, '3': 0.5714285714285714,
                                  '4': 0.2857142857142857, '5': 0.14285714285714285, '6': 0.14285714285714285,
                                  '7': 0.14285714285714285, '8': 0.14285714285714285}})

        # Non Default Test 1
        result = self.N.find_degree_centrality(self.graph, in_out='out')
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'outdegree_centrality': {'1': 0.2857142857142857, '2': 0.42857142857142855,
                                     '3': 0.42857142857142855, '4': 0.0,
                                     '5': 0.0, '6': 0.0, '7': 0.0, '8': 0.0}})

        # Non Default Test 2
        result = self.N.find_degree_centrality(self.graph, in_out='in')
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'indegree_centrality': {'1': 0.0, '2': 0.14285714285714285, '3': 0.14285714285714285,
                                    '4': 0.2857142857142857,
                                    '5': 0.14285714285714285, '6': 0.14285714285714285,
                                    '7': 0.14285714285714285,
                                    '8': 0.14285714285714285}})

        # Non Default Test 3
        result = self.N.find_degree_centrality(self.graph, in_out='in', directed=True)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'indegree_centrality': {'1': 0.0, '2': 0.14285714285714285, '3': 0.14285714285714285,
                                    '4': 0.2857142857142857,
                                    '5': 0.14285714285714285, '6': 0.14285714285714285,
                                    '7': 0.14285714285714285,
                                    '8': 0.14285714285714285}})

        # Non Weighted Test
        result = self.N.find_degree_centrality(self.graph)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'degree_centrality': {'1': 0.2857142857142857, '2': 0.5714285714285714, '3': 0.5714285714285714,
                                  '4': 0.2857142857142857, '5': 0.14285714285714285, '6': 0.14285714285714285,
                                  '7': 0.14285714285714285, '8': 0.14285714285714285}}
                         )

    def test_find_closeness_centrality(self):
        # Default Test
        result = self.N.find_closeness_centrality(self.graph, ['8', '8'])
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2].get('closeness_centrality').get('8'), 0.4375)
        self.assertEqual(result[2].get('closeness_centrality').get('7'), 0.8125)
        self.assertEqual(result[2].get('closeness_centrality').get('6'), 0.8125)
        self.assertEqual(result[2].get('closeness_centrality').get('5'), 0.8125)
        self.assertEqual(result[2].get('closeness_centrality').get('4'), 0.9285714285714286)
        self.assertEqual(result[2].get('closeness_centrality').get('3'), 1.3)
        self.assertEqual(result[2].get('closeness_centrality').get('2'), 1.3)
        self.assertEqual(result[2].get('closeness_centrality').get('1'), 0.9285714285714286)

        # Non Default Test
        result = self.N.find_closeness_centrality(self.graph, nodes=['8', '8'], normalized=False)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2].get('closeness_centrality').get('8'), 0.4375)
        self.assertEqual(result[2].get('closeness_centrality').get('7'), 0.8125)
        self.assertEqual(result[2].get('closeness_centrality').get('6'), 0.8125)
        self.assertEqual(result[2].get('closeness_centrality').get('5'), 0.8125)
        self.assertEqual(result[2].get('closeness_centrality').get('4'), 0.9285714285714286)
        self.assertEqual(result[2].get('closeness_centrality').get('3'), 1.3)
        self.assertEqual(result[2].get('closeness_centrality').get('2'), 1.3)
        self.assertEqual(result[2].get('closeness_centrality').get('1'), 0.9285714285714286)

        # Non Default Test 2
        result = self.N.find_closeness_centrality(self.graph, nodes=['8', '8'], normalized=False, directed=True)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2].get('closeness_centrality').get('3'), 4.333333333333333)
        self.assertEqual(result[2].get('closeness_centrality').get('2'), 1.4444444444444444)
        self.assertEqual(result[2].get('closeness_centrality').get('1'), 0.9285714285714286)

    def test_find_betweenness_centrality(self):
        # Default Test
        result = self.N.find_betweenness_centrality(self.graph)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {'betweenness_centrality': {'1': 0.07142857142857142, '2': 0.5952380952380952,
                                                                '3': 0.5952380952380952, '4': 0.07142857142857142,
                                                                '5': 0.0, '6': 0.0, '7': 0.0, '8': 0.0}})

        # Non Default test
        result = self.N.find_betweenness_centrality(self.graph, type='edge')
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'betweenness_centrality': {('1', '2'): 0.21428571428571427, ('1', '4'): 0.14285714285714285,
                                       ('2', '3'): 0.42857142857142855, ('2', '5'): 0.25, ('2', '7'): 0.25,
                                       ('3', '4'): 0.21428571428571427, ('3', '6'): 0.25, ('3', '8'): 0.25}})
        # Non Default Test 1
        result = self.N.find_betweenness_centrality(self.graph, k=1, normalized=False, weight=True, endpoints=True,
                                                    seed=1)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'betweenness_centrality': {'1': 4.0, '2': 14.0, '3': 28.0, '4': 6.0, '5': 4.0, '6': 4.0, '7': 4.0,
                                       '8': 4.0}})

        # Non weighted Test 1
        result = self.N.find_betweenness_centrality(self.graph_03, k=1, normalized=False, weight=True, endpoints=True,
                                                    seed=1)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'betweenness_centrality': {'1': 4.0, '2': 14.0, '3': 28.0, '4': 6.0, '5': 4.0, '6': 4.0, '7': 4.0,
                                       '8': 4.0}})

        # Non Default Test 2
        result = self.N.find_betweenness_centrality(self.graph_03, k=1, normalized=False, weight=True, endpoints=True,
                                                    seed=1, directed=True)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'betweenness_centrality': {'1': 0.0, '2': 0.0, '3': 3.0, '4': 1.0, '5': 0.0, '6': 1.0, '7': 0.0, '8': 1.0}}
                         )

    def test_find_pagerank(self):
        # Default Test
        result = self.N.find_pagerank(self.graph)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'pagerank': {'1': 0.12113884655309373, '2': 0.23955113566709454, '3': 0.23955113566709454,
                         '4': 0.12113884655309375, '5': 0.06965500888990583, '6': 0.06965500888990583,
                         '7': 0.06965500888990583, '8': 0.06965500888990583}})

        # Non Default Test
        result = self.N.find_pagerank(self.graph, alpha=0.95,
                                      personalization={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                       '6': 0.125, '7': 0.125, '8': 0.125}, max_iter=100,
                                      tol=1e-07,
                                      nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1},
                                      weight=True,
                                      dangling={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                '6': 0.125, '7': 0.125, '8': 0.125})
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2],
                         {'pagerank': {'1': 0.12353302891578935, '2': 0.24675733134387767, '3': 0.2467573313438777,
                                       '4': 0.12353302891578932, '5': 0.06485481987016649, '6': 0.06485481987016647,
                                       '7': 0.06485481987016649, '8': 0.06485481987016647}})

        # Non weighted Test
        result = self.N.find_pagerank(self.graph_03, alpha=0.95,
                                      personalization={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                       '6': 0.125, '7': 0.125, '8': 0.125}, max_iter=100,
                                      tol=1e-07,
                                      nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1},
                                      weight=True,
                                      dangling={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                '6': 0.125, '7': 0.125, '8': 0.125})
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2],
                         {'pagerank': {'1': 0.12353302891578935, '2': 0.24675733134387767, '3': 0.2467573313438777,
                                       '4': 0.12353302891578932, '5': 0.06485481987016649, '6': 0.06485481987016647,
                                       '7': 0.06485481987016649, '8': 0.06485481987016647}})

        # Non default Test 2
        result = self.N.find_pagerank(self.graph_03, alpha=0.95,
                                      personalization={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                       '6': 0.125, '7': 0.125, '8': 0.125}, max_iter=100,
                                      tol=1e-07,
                                      nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1},
                                      weight=True,
                                      dangling={'1': 0.125, '2': 0.125, '3': 0.125, '4': 0.125, '5': 0.125,
                                                '6': 0.125, '7': 0.125, '8': 0.125}, directed=True)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2],
                         {'pagerank': {'1': 0.08514279383409741, '2': 0.1255854995423924, '3': 0.12491155064890427,
                                       '4': 0.16514082203112918, '5': 0.12491155064890427, '6': 0.12469811632283417,
                                       '7': 0.12491155064890427, '8': 0.12469811632283417}})

    def test_find_eigenvector_centrality(self):
        # Default Test
        result = self.N.find_eigenvector_centrality(self.graph)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {'eigenvector_centrality': {'1': 0.35775018836999806, '2': 0.5298994260311778,
                                                                '3': 0.5298994260311778, '4': 0.35775018836999806,
                                                                '5': 0.2135666184274351, '6': 0.2135666184274351,
                                                                '7': 0.2135666184274351, '8': 0.2135666184274351}})

        # Non Default Test
        result = self.N.find_eigenvector_centrality(self.graph, max_iter=110, tol=1e-05,
                                                    nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1,
                                                            '8': 1}, weight=True, directed=False)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'eigenvector_centrality': {'1': 0.35774203080090017, '2': 0.5299019638339402, '3': 0.5299019638339402,
                                       '4': 0.3577420308009002, '5': 0.21357030238703748, '6': 0.21357030238703748,
                                       '7': 0.21357030238703748, '8': 0.21357030238703748}})

        # Non weighted Test
        result = self.N.find_eigenvector_centrality(self.graph, max_iter=500, tol=1e-05,
                                                    nstart={'1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1,
                                                            '8': 1}, weight=True, directed=True)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {'eigenvector_centrality': {'1': 1.9935012399077745e-07, '2': 5.183103223760218e-05,
                                                                '3': 0.0067123180248934745, '4': 0.5773456687445266,
                                                                '5': 0.0067123180248934745, '6': 0.5772940370624132,
                                                                '7': 0.0067123180248934745, '8': 0.5772940370624132}})

    def test_find_hits(self):
        # Default Test
        result = self.N.find_hits(self.graph, mode='hub_matrix')
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'hub_matrix': [[25.0, 0.0, 43.0, 0.0, 18.0, 0.0, 27.0, 0.0],
                           [0.0, 151.0, 0.0, 47.0, 0.0, 40.0, 0.0, 50.0],
                           [43.0, 0.0, 238.0, 0.0, 30.0, 0.0, 45.0, 0.0],
                           [0.0, 47.0, 0.0, 65.0, 0.0, 56.0, 0.0, 70.0],
                           [18.0, 0.0, 30.0, 0.0, 36.0, 0.0, 54.0, 0.0],
                           [0.0, 40.0, 0.0, 56.0, 0.0, 64.0, 0.0, 80.0],
                           [27.0, 0.0, 45.0, 0.0, 54.0, 0.0, 81.0, 0.0],
                           [0.0, 50.0, 0.0, 70.0, 0.0, 80.0, 0.0, 100.0]]})

        # Non Default Test
        result = self.N.find_hits(self.graph, mode='authority_matrix')
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {'authority_matrix': [[25.0, 0.0, 43.0, 0.0, 18.0, 0.0, 27.0, 0.0],
                                                          [0.0, 151.0, 0.0, 47.0, 0.0, 40.0, 0.0, 50.0],
                                                          [43.0, 0.0, 238.0, 0.0, 30.0, 0.0, 45.0, 0.0],
                                                          [0.0, 47.0, 0.0, 65.0, 0.0, 56.0, 0.0, 70.0],
                                                          [18.0, 0.0, 30.0, 0.0, 36.0, 0.0, 54.0, 0.0],
                                                          [0.0, 40.0, 0.0, 56.0, 0.0, 64.0, 0.0, 80.0],
                                                          [27.0, 0.0, 45.0, 0.0, 54.0, 0.0, 81.0, 0.0],
                                                          [0.0, 50.0, 0.0, 70.0, 0.0, 80.0, 0.0, 100.0]]})

        # Non weighted Test
        result = self.N.find_hits(self.graph_03, mode='authority_matrix')
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'authority_matrix': [[2.0, 0.0, 2.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 4.0, 0.0, 2.0, 0.0, 1.0, 0.0, 1.0],
                                 [2.0, 0.0, 4.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 2.0, 0.0, 2.0, 0.0, 1.0, 0.0, 1.0],
                                 [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
                                 [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0],
                                 [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0]]})

        # Non default Test 2
        result = self.N.find_hits(self.graph, mode='authority_matrix', directed=True)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 'success')
        self.assertEqual(result[2], {
            'authority_matrix': [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                 [0.0, 9.0, 0.0, 12.0, 0.0, 0.0, 0.0, 0.0],
                                 [0.0, 0.0, 25.0, 0.0, 30.0, 0.0, 45.0, 0.0],
                                 [0.0, 12.0, 0.0, 65.0, 0.0, 56.0, 0.0, 70.0],
                                 [0.0, 0.0, 30.0, 0.0, 36.0, 0.0, 54.0, 0.0],
                                 [0.0, 0.0, 0.0, 56.0, 0.0, 64.0, 0.0, 80.0],
                                 [0.0, 0.0, 45.0, 0.0, 54.0, 0.0, 81.0, 0.0],
                                 [0.0, 0.0, 0.0, 70.0, 0.0, 80.0, 0.0, 100.0]]})

    def test_construct_graph(self):
        # Default Test
        result = self.N.construct_graph(self.graph)
        self.assertEqual(str(result.edges(data=True)),
                         "[('1', '2', {'weight': 3}), ('1', '4', {'weight': 4}), ('2', '3', {'weight': 5}),"
                         " ('2', '5', {'weight': 6}), ('2', '7', {'weight': 9}), ('3', '4', {'weight': 7}), "
                         "('3', '6', {'weight': 8}), ('3', '8', {'weight': 10})]")

        # Graph without nodes Test
        result = self.N.construct_graph(self.graph_01)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'nodes'")
        self.assertEqual(result[2], {})

        # Graph without edges Test
        result = self.N.construct_graph(self.graph_02)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], "'edges'")
        self.assertEqual(result[2], {})

    def test_check_graph_validity(self):
        # Graph without wrong number of weights
        result = self.cv.is_valid_graph(self.graph_04)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], 'weights and edges must be equal')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    unittest.main()
