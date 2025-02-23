# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

import retworkx
import numpy as np


class TestDAGAdjacencyMatrix(unittest.TestCase):
    def test_single_neighbor(self):
        dag = retworkx.PyDAG()
        node_a = dag.add_node("a")
        dag.add_child(node_a, "b", {"a": 1})
        dag.add_child(node_a, "c", {"a": 2})
        res = retworkx.digraph_adjacency_matrix(dag, lambda x: 1)
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(
            np.array_equal(
                np.array(
                    [[0.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                    dtype=np.float64,
                ),
                res,
            )
        )

    def test_no_weight_fn(self):
        dag = retworkx.PyDAG()
        node_a = dag.add_node("a")
        dag.add_child(node_a, "b", {"a": 1})
        dag.add_child(node_a, "c", {"a": 2})
        res = retworkx.digraph_adjacency_matrix(dag)
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(
            np.array_equal(
                np.array(
                    [[0.0, 1.0, 1.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                    dtype=np.float64,
                ),
                res,
            )
        )

    def test_default_weight(self):
        dag = retworkx.PyDAG()
        node_a = dag.add_node("a")
        dag.add_child(node_a, "b", {"a": 1})
        dag.add_child(node_a, "c", {"a": 2})
        res = retworkx.digraph_adjacency_matrix(dag, default_weight=4)
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(
            np.array_equal(
                np.array(
                    [[0.0, 4.0, 4.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                    dtype=np.float64,
                ),
                res,
            )
        )

    def test_float_cast_weight_func(self):
        dag = retworkx.PyDAG()
        node_a = dag.add_node("a")
        dag.add_child(node_a, "b", 7.0)
        res = retworkx.digraph_adjacency_matrix(dag, lambda x: float(x))
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(np.array_equal(np.array([[0.0, 7.0], [0.0, 0.0]]), res))

    def test_multigraph_sum_cast_weight_func(self):
        dag = retworkx.PyDAG()
        node_a = dag.add_node("a")
        node_b = dag.add_child(node_a, "b", 7.0)
        dag.add_edge(node_a, node_b, 0.5)
        res = retworkx.digraph_adjacency_matrix(dag, lambda x: float(x))
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(np.array_equal(np.array([[0.0, 7.5], [0.0, 0.0]]), res))

    def test_multigraph_sum_cast_weight_func_non_zero_null(self):
        graph = retworkx.PyDiGraph()
        node_a = graph.add_node("a")
        node_b = graph.add_node("b")
        graph.add_edge(node_a, node_b, 7.0)
        graph.add_edge(node_a, node_b, 0.5)
        res = retworkx.adjacency_matrix(
            graph, lambda x: float(x), null_value=np.inf
        )
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(
            np.array_equal(np.array([[np.inf, 7.5], [np.inf, np.inf]]), res)
        )

    def test_graph_to_digraph_adjacency_matrix(self):
        graph = retworkx.PyGraph()
        self.assertRaises(TypeError, retworkx.digraph_adjacency_matrix, graph)

    def test_no_edge_digraph_adjacency_matrix(self):
        dag = retworkx.PyDAG()
        for i in range(50):
            dag.add_node(i)
        res = retworkx.digraph_adjacency_matrix(dag, lambda x: 1)
        self.assertTrue(np.array_equal(np.zeros([50, 50]), res))

    def test_digraph_with_index_holes(self):
        dag = retworkx.PyDAG()
        node_a = dag.add_node("a")
        node_b = dag.add_child(node_a, "b", 1)
        dag.add_child(node_a, "c", 1)
        dag.remove_node(node_b)
        res = retworkx.digraph_adjacency_matrix(dag, lambda x: 1)
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(np.array_equal(np.array([[0, 1], [0, 0]]), res))

    def test_from_adjacency_matrix(self):
        input_array = np.array(
            [[0.0, 4.0, 0.0], [4.0, 0.0, 4.0], [0.0, 4.0, 0.0]],
            dtype=np.float64,
        )
        graph = retworkx.PyDiGraph.from_adjacency_matrix(input_array)
        out_array = retworkx.digraph_adjacency_matrix(graph, lambda x: x)
        self.assertTrue(np.array_equal(input_array, out_array))

    def test_random_graph_full_path(self):
        graph = retworkx.directed_gnp_random_graph(100, 0.95, seed=42)
        adjacency_matrix = retworkx.digraph_adjacency_matrix(graph)
        new_graph = retworkx.PyDiGraph.from_adjacency_matrix(adjacency_matrix)
        new_adjacency_matrix = retworkx.digraph_adjacency_matrix(new_graph)
        self.assertTrue(np.array_equal(adjacency_matrix, new_adjacency_matrix))

    def test_random_graph_different_dtype(self):
        input_matrix = np.array(
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.int64
        )
        with self.assertRaises(TypeError):
            retworkx.PyDiGraph.from_adjacency_matrix(input_matrix)

    def test_random_graph_different_dtype_astype_no_copy(self):
        input_matrix = np.array(
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.int64
        )
        graph = retworkx.PyDiGraph.from_adjacency_matrix(
            input_matrix.astype(np.float64, copy=False)
        )
        adj_matrix = retworkx.digraph_adjacency_matrix(graph, lambda x: x)
        self.assertTrue(np.array_equal(adj_matrix, input_matrix))

    def test_random_graph_float_dtype(self):
        input_matrix = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=float)
        graph = retworkx.PyDiGraph.from_adjacency_matrix(input_matrix)
        adj_matrix = retworkx.digraph_adjacency_matrix(graph, lambda x: x)
        self.assertTrue(np.array_equal(adj_matrix, input_matrix))

    def test_non_zero_null(self):
        input_matrix = np.array(
            [[np.Inf, 1, np.Inf], [1, np.Inf, 1], [np.Inf, 1, np.Inf]],
            dtype=np.float64,
        )
        graph = retworkx.PyDiGraph.from_adjacency_matrix(
            input_matrix, null_value=np.Inf
        )
        adj_matrix = retworkx.adjacency_matrix(graph, float)
        expected_matrix = np.array(
            [[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
            dtype=np.float64,
        )
        self.assertTrue(np.array_equal(adj_matrix, expected_matrix))

    def test_negative_weight(self):
        input_matrix = np.array(
            [[0, 1, 0], [-1, 0, -1], [0, 1, 0]], dtype=float
        )
        graph = retworkx.PyDiGraph.from_adjacency_matrix(input_matrix)
        adj_matrix = retworkx.digraph_adjacency_matrix(graph, lambda x: x)
        self.assertTrue(np.array_equal(adj_matrix, input_matrix))
        self.assertEqual(
            [(0, 1, 1), (1, 0, -1), (1, 2, -1), (2, 1, 1)],
            graph.weighted_edge_list(),
        )

    def test_nan_null(self):
        input_matrix = np.array(
            [[np.nan, 1, np.nan], [1, np.nan, 1], [np.nan, 1, np.nan]],
            dtype=np.float64,
        )
        graph = retworkx.PyDiGraph.from_adjacency_matrix(
            input_matrix, null_value=np.nan
        )
        adj_matrix = retworkx.adjacency_matrix(graph, float)
        expected_matrix = np.array(
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.float64
        )
        self.assertTrue(np.array_equal(adj_matrix, expected_matrix))


class TestFromComplexAdjacencyMatrix(unittest.TestCase):
    def test_from_adjacency_matrix(self):
        input_array = np.array(
            [[0.0, 4.0, 0.0], [4.0, 0.0, 4.0], [0.0, 4.0, 0.0]],
            dtype=np.complex128,
        )
        graph = retworkx.PyDiGraph.from_complex_adjacency_matrix(input_array)
        expected = [
            (0, 1, 4 + 0j),
            (1, 0, 4 + 0j),
            (1, 2, 4 + 0j),
            (2, 1, 4 + 0j),
        ]
        self.assertEqual(graph.weighted_edge_list(), expected)

    def test_random_graph_different_dtype(self):
        input_matrix = np.array(
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.int64
        )
        with self.assertRaises(TypeError):
            retworkx.PyDiGraph.from_complex_adjacency_matrix(input_matrix)

    def test_random_graph_different_dtype_astype_no_copy(self):
        input_matrix = np.array(
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.int64
        )
        graph = retworkx.PyDiGraph.from_complex_adjacency_matrix(
            input_matrix.astype(np.complex128, copy=False)
        )
        expected = [
            (0, 1, 1 + 0j),
            (1, 0, 1 + 0j),
            (1, 2, 1 + 0j),
            (2, 1, 1 + 0j),
        ]
        self.assertEqual(graph.weighted_edge_list(), expected)

    def test_random_graph_complex_dtype(self):
        input_matrix = np.array(
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=complex
        )
        graph = retworkx.PyDiGraph.from_complex_adjacency_matrix(input_matrix)
        expected = [
            (0, 1, 1 + 0j),
            (1, 0, 1 + 0j),
            (1, 2, 1 + 0j),
            (2, 1, 1 + 0j),
        ]
        self.assertEqual(graph.weighted_edge_list(), expected)

    def test_non_zero_null(self):
        input_matrix = np.array(
            [[np.Inf, 1, np.Inf], [1, np.Inf, 1], [np.Inf, 1, np.Inf]],
            dtype=np.complex128,
        )
        graph = retworkx.PyDiGraph.from_complex_adjacency_matrix(
            input_matrix, null_value=np.Inf
        )
        expected = [
            (0, 1, 1 + 0j),
            (1, 0, 1 + 0j),
            (1, 2, 1 + 0j),
            (2, 1, 1 + 0j),
        ]
        self.assertEqual(graph.weighted_edge_list(), expected)

    def test_negative_weight(self):
        input_matrix = np.array(
            [[0, 1, 0], [-1, 0, -1], [0, 1, 0]], dtype=complex
        )
        graph = retworkx.PyDiGraph.from_complex_adjacency_matrix(input_matrix)
        self.assertEqual(
            [(0, 1, 1), (1, 0, -1), (1, 2, -1), (2, 1, 1)],
            graph.weighted_edge_list(),
        )

    def test_nan_null(self):
        input_matrix = np.array(
            [[np.nan, 1, np.nan], [1, np.nan, 1], [np.nan, 1, np.nan]],
            dtype=np.complex128,
        )
        graph = retworkx.PyDiGraph.from_complex_adjacency_matrix(
            input_matrix, null_value=np.nan
        )
        edge_list = graph.weighted_edge_list()
        self.assertEqual(
            edge_list,
            [(0, 1, 1 + 0j), (1, 0, 1 + 0j), (1, 2, 1 + 0j), (2, 1, 1 + 0j)],
        )
