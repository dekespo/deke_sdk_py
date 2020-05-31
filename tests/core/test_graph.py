import unittest

from core.dimensions import Dim2D
from core.graph import Graph
from core.shapes import Shape2D
from core.raw_data_handler import RawDataHandler

from templates.rectangle_world import example_small_random, example_unreachable_positions

# TODO: Add non-blocking (empty) graph
# TODO: Separate test_graph_data_with_blocking into small unittests with setup
class GraphTest(unittest.TestCase):
    def test_graph_data_with_blocking(self):
        raw_data_handler = RawDataHandler(example_small_random())
        graph = Graph(raw_data_handler, Shape2D.Type.RECTANGLE)
        self.assertTrue(str(graph), """
                                    Shape Type: Type.RECTANGLE
                                    Raw data:
                                    0 |1 |0 |1
                                    1 |0 |0 |0
                                    0 |0 |0 |0
                                    """
                        )
        self.assertTrue(graph.raw_data_handler, example_small_random())
        self.assertIsNone(graph.blocking_values)
        self.assertListEqual(graph.blocking_positions, [])
        new_blocking_values = set([1])
        graph.update_blocking_data(new_blocking_values)
        self.assertTrue(graph.blocking_values, set([1]))
        self.assertTrue(graph.blocking_positions, [Dim2D(1, 0), Dim2D(3, 0), Dim2D(1, 1)])
        self.assertTrue(graph.graph_shape.is_inside_boundaries(Dim2D(1, 1)))
        self.assertFalse(graph.graph_shape.is_inside_boundaries(Dim2D(-1, 1)))
        pos = Dim2D(1, 1)
        neighbour_data = Graph.NeighbourData(Graph.NeighbourData.Type.DIAMOND, 2)
        available_poses = graph.get_available_neighbours(pos, neighbour_data)
        self.assertEqual(len(available_poses), 7)
        self.assertTrue(Dim2D(0, 0) in available_poses)
        self.assertTrue(Dim2D(0, 2) in available_poses)
        self.assertTrue(Dim2D(1, 2) in available_poses)
        self.assertTrue(Dim2D(2, 0) in available_poses)
        self.assertTrue(Dim2D(2, 1) in available_poses)
        self.assertTrue(Dim2D(2, 2) in available_poses)
        self.assertTrue(Dim2D(3, 1) in available_poses)
        pos1 = Dim2D(0, 2)
        neighbour_data = Graph.NeighbourData(Graph.NeighbourData.Type.CROSS, 1)
        available_poses = graph.get_available_neighbours(pos1, neighbour_data)
        self.assertEqual(len(available_poses), 1)
        self.assertEqual(available_poses[0], Dim2D(1, 2))
        pos2 = Dim2D(2, 1)
        neighbour_data = Graph.NeighbourData(Graph.NeighbourData.Type.SQUARE)
        available_poses = graph.get_available_neighbours(pos2, neighbour_data)
        self.assertEqual(len(available_poses), 6)
        self.assertTrue(Dim2D(2, 0) in available_poses)
        self.assertTrue(Dim2D(2, 2) in available_poses)
        self.assertTrue(Dim2D(1, 1) in available_poses)
        self.assertTrue(Dim2D(1, 2) in available_poses)
        self.assertTrue(Dim2D(3, 1) in available_poses)
        self.assertTrue(Dim2D(3, 2) in available_poses)

    def test_unreachable_graph_data(self):
        raw_data_handler = RawDataHandler(example_unreachable_positions())
        blocking_set = set([1])
        unreachable_positions_set = set([Dim2D(3, 2)])
        graph = Graph(raw_data_handler,
                      Shape2D.Type.RECTANGLE,
                      blocking_set,
                      unreachable_positions_set
                     )
        self.assertTrue(graph.blocking_values, tuple(blocking_set))
        self.assertTrue(graph.blocking_positions, [Dim2D(2, 1), Dim2D(3, 1), Dim2D(2, 2)])
        self.assertTrue(graph.unreachable_positions, tuple(unreachable_positions_set))
        pos = Dim2D(1, 2)
        neighbour_data = Graph.NeighbourData(Graph.NeighbourData.Type.CROSS, 2)
        available_poses = graph.get_available_neighbours(pos, neighbour_data)
        self.assertEqual(len(available_poses), 3)
        self.assertTrue(Dim2D(1, 0) in available_poses)
        self.assertTrue(Dim2D(1, 1) in available_poses)
        self.assertTrue(Dim2D(0, 2) in available_poses)

    def test_get_neighbours_cross(self):
        pos = Dim2D(1, 1)
        poses = Graph.get_neighbours_cross(pos)
        poses = list(poses)
        self.assertEqual(len(poses), 4)
        self.assertTrue(Dim2D(0, 1) in poses)
        self.assertTrue(Dim2D(1, 2) in poses)
        self.assertTrue(Dim2D(2, 1) in poses)
        self.assertTrue(Dim2D(1, 0) in poses)

    def test_get_neighbours_square(self):
        pos = Dim2D(1, 1)
        poses = Graph.get_neighbours_square(pos)
        poses = list(poses)
        self.assertEqual(len(poses), 8)
        self.assertTrue(Dim2D(0, 1) in poses)
        self.assertTrue(Dim2D(1, 2) in poses)
        self.assertTrue(Dim2D(2, 1) in poses)
        self.assertTrue(Dim2D(1, 0) in poses)
        self.assertTrue(Dim2D(0, 0) in poses)
        self.assertTrue(Dim2D(2, 2) in poses)
        self.assertTrue(Dim2D(0, 2) in poses)
        self.assertTrue(Dim2D(2, 0) in poses)

    def test_get_neighbours_diamond(self):
        pos = Dim2D(1, 1)
        poses = Graph.get_neighbours_diamond(
            pos,
            Graph.NeighbourData(Graph.NeighbourData.Type.DIAMOND, length=2)
        )
        poses = list(poses)
        self.assertEqual(len(poses), 12)
        self.assertTrue(Dim2D(0, 1) in poses)
        self.assertTrue(Dim2D(-1, 1) in poses)
        self.assertTrue(Dim2D(1, 2) in poses)
        self.assertTrue(Dim2D(1, 3) in poses)
        self.assertTrue(Dim2D(2, 1) in poses)
        self.assertTrue(Dim2D(3, 1) in poses)
        self.assertTrue(Dim2D(1, 0) in poses)
        self.assertTrue(Dim2D(1, -1) in poses)
        self.assertTrue(Dim2D(0, 0) in poses)
        self.assertTrue(Dim2D(2, 2) in poses)
        self.assertTrue(Dim2D(0, 2) in poses)
        self.assertTrue(Dim2D(2, 0) in poses)

if __name__ == "__main__":
    unittest.main()
